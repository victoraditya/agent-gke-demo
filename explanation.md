# Implementation and Deployment Guide

This guide explains how the Agentic AI system is implemented and how to deploy it to Google Kubernetes Engine (GKE).

## 1. Code Structure

-   **`main.py`**: The entry point. It sets up a Flask server. When you send a POST request to `/run-agents`, it initializes the agents and runs them using the **Google ADK** `InMemoryRunner`.
-   **`agents.py`**: Defines the `researcher` and `writer` agents using the **Google ADK** (`google-adk`) library. They use the `Agent` class and `gemini-2.0-flash-exp` model.
-   **`Dockerfile`**: Instructions to build the Docker image. It uses a lightweight Python base image, installs dependencies (including `google-adk`), and runs the Flask app.

## 2. Prerequisites for Deployment

Before you can deploy, you need to set up the following on Google Cloud Platform (GCP) and GitHub:

1.  **GCP Project**: Create a project and enable the **Vertex AI API**, **Kubernetes Engine API**, **Artifact Registry API**, and **Cloud Resource Manager API**.
2.  **GKE Cluster**: Create a **Standard** cost-optimized cluster using Spot instances and Workload Identity.
    ```bash
    gcloud container clusters create agent-cluster \
      --zone us-central1-a \
      --machine-type e2-small \
      --num-nodes 1 \
      --spot \
      --disk-size=30GB \
      --enable-autoscaling --min-nodes 1 --max-nodes 3 \
      --workload-pool=PROJECT_ID.svc.id.goog
    ```
3.  **Service Account**: Create a service account with permissions to:
    -   Push to Artifact Registry (`Artifact Registry Admin`).
    -   Deploy to GKE (`Kubernetes Engine Developer`).
    -   Use Vertex AI (`Vertex AI User`).
    -   Store logs (`Storage Admin`).
4.  **GitHub Secrets**: Go to your repository settings -> Secrets and variables -> Actions, and add:
    -   `GCP_PROJECT_ID`: Your Google Cloud Project ID.
    -   `GKE_CLUSTER`: The name of your GKE cluster (e.g., `agent-cluster`).
    -   `GKE_ZONE`: The zone of your cluster (e.g., `us-central1-a`).
    *Note: `GCP_SA_KEY` is NO LONGER REQUIRED due to Workload Identity Federation.*

## 3. Deployment Process

The deployment is automated using GitHub Actions (`.github/workflows/deploy.yaml`).

1.  **Trigger**: When you push code to the `main` branch.
2.  **Authenticate**: The workflow uses **Workload Identity Federation** to securely authenticate with Google Cloud without long-lived keys.
3.  **Build**: The workflow builds the Docker image from the `Dockerfile`.
4.  **Publish**: It pushes the image to **Google Artifact Registry** (`us-central1-docker.pkg.dev`).
5.  **Deploy**: It uses `kubectl` to apply the Kubernetes manifests:
    -   Updates the `deployment.yaml` with the new image tag.
    -   Applies `deployment.yaml` to update the pods.
    -   Applies `service.yaml` to ensure the LoadBalancer is active.

## 4. How to Run Locally (Mac Guide)

For local development on macOS, it is best to use `brew` for system tools and `pip` (within a virtual environment) for Python packages.

1.  **Install System Tools (via Homebrew)**:
    ```bash
    # Install Python, Git, and Google Cloud SDK if not present
    brew install python3 git google-cloud-sdk kubernetes-cli
    ```

2.  **Set up Python Environment**:
    It is best practice to use a virtual environment so you don't mess up your system Python.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies (via pip)**:
    Now use `pip` to install the project libraries.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Authenticate**:
    You have two options:
    *   **Option A (Standard)**: `gcloud auth application-default login`
    *   **Option B (Service Account)**:
        1.  Download a service account key (JSON).
        2.  `export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/key.json`

5.  **Run App**:
    ```bash
    # Enable Vertex AI for ADK
    export GOOGLE_GENAI_USE_VERTEXAI=true
    export GOOGLE_CLOUD_PROJECT=your-project-id
    export GOOGLE_CLOUD_LOCATION=us-central1
    
    python main.py
    ```

## 5. Workload Identity (Security)

We use **Workload Identity** in two places:

1.  **GKE Pods**: Allows the running application to access Vertex AI.
    *   **Kubernetes Service Account (`agent-sa`)** bound to **Google Service Account (`local-dev-sa`)**.
    *   This is why we added the `--workload-pool` flag when creating the cluster.

2.  **GitHub Actions (CI/CD)**: Allows the deployment workflow to push images and update the cluster.
    *   **Workload Identity Pool (`github-pool`)** trusts tokens from your GitHub repository.
    *   This eliminates the need for `GCP_SA_KEY` secrets.

> **Troubleshooting**: If you still get 403 errors, ensure your Node Pool is configured to use the GKE Metadata Server:
> ```bash
> gcloud container node-pools update default-pool --cluster agent-cluster --zone us-central1-a --workload-metadata=GKE_METADATA
> ```
