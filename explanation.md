# Implementation and Deployment Guide

This guide explains how the Agentic AI system is implemented and how to deploy it to Google Kubernetes Engine (GKE).

## 1. Code Structure

-   **`main.py`**: The entry point. It sets up a Flask server. When you send a POST request to `/run-agents`, it initializes the agents and runs them in sequence.
-   **`agents.py`**: Defines the `ResearcherAgent` and `WriterAgent` classes. They inherit from a base `Agent` class and use LangChain's `VertexAI` wrapper to interact with Google's Gemini models.
-   **`Dockerfile`**: Instructions to build the Docker image. It uses a lightweight Python base image, installs dependencies, and runs the Flask app.

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
    -   `GCP_SA_KEY`: The JSON key of the service account you created.
    -   `GKE_CLUSTER`: The name of your GKE cluster (e.g., `agent-cluster`).
    -   `GKE_ZONE`: The zone of your cluster (e.g., `us-central1-a`).

## 3. Deployment Process

The deployment is automated using GitHub Actions (`.github/workflows/deploy.yaml`).

1.  **Trigger**: When you push code to the `main` branch.
2.  **Build**: The workflow builds the Docker image from the `Dockerfile`.
3.  **Publish**: It pushes the image to **Google Artifact Registry** (`us-central1-docker.pkg.dev`).
4.  **Deploy**: It uses `kubectl` to apply the Kubernetes manifests:
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
    *   **Option B (Service Account - Recommended)**:
        1.  Download a service account key (JSON).
        2.  `export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/key.json`

5.  **Run App**:
    ```bash
    python main.py
    ```

## 5. Workload Identity (Security)

We use **Workload Identity** to securely allow your GKE Pods to access Google Cloud APIs (like Vertex AI) without storing long-lived keys in the container.

*   **Kubernetes Service Account (`agent-sa`)**: This is an account inside the cluster.
*   **Google Service Account (`local-dev-sa`)**: This is an account in GCP with permissions.
*   **Binding**: We "bind" them together so `agent-sa` can "act as" `local-dev-sa`.

This is why we added the `--workload-pool` flag when creating the cluster and the `iam.gke.io/gcp-service-account` annotation in `k8s/serviceaccount.yaml`.
