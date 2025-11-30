# Step-by-Step Guide: From Local to GKE

Follow these exact steps to push your project to GitHub and automatically deploy it to your Google Kubernetes Engine (GKE) cluster.

## Prerequisites

1.  **GCP Project**: You have a Google Cloud Project ID.
2.  **GKE Cluster**: You have created the cluster using the command in `gkeprerequisite.md` (with Workload Identity).
3.  **Service Account Key**: You have the JSON key for a service account with permissions (`Kubernetes Engine Developer`, `Artifact Registry Admin`, `Vertex AI User`, `Storage Admin`).

## Step 1: Create a GitHub Repository

1.  Go to [GitHub.com/new](https://github.com/new).
2.  Name your repository (e.g., `agent-gke-demo`).
3.  Do **not** initialize with README, .gitignore, or License (we already have them locally).
4.  Click **Create repository**.
5.  Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/agent-gke-demo.git`).

## Step 2: Configure GitHub Secrets

The automated deployment needs access to your GCP project.

1.  In your new GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
2.  Click **New repository secret**.
3.  Add the following secrets one by one:

| Secret Name | Value |
| :--- | :--- |
| `GCP_PROJECT_ID` | Your Google Cloud Project ID (e.g., `my-agent-project-123`). |
| `GKE_CLUSTER` | `agent-cluster` (or whatever you named it). |
| `GKE_ZONE` | `us-central1-a` (or the zone you chose). |

## Step 3: Push Your Code

Open your terminal in the project directory and run these commands:

```bash
# 1. Initialize Git (if not already done)
git init

# 2. Add all files to staging
git add .

# 3. Commit the files
git commit -m "Initial commit: Agentic AI on GKE"

# 4. Rename branch to main
git branch -M main

# 5. Link your local repo to GitHub (Replace URL with yours!)
git remote add origin https://github.com/YOUR_USERNAME/agent-gke-demo.git

# 6. Push to GitHub
git push -u origin main
```

## Step 4: Watch the Deployment

1.  Go to the **Actions** tab in your GitHub repository.
2.  You should see a workflow run named **"Build and Deploy to GKE"** starting up.
3.  Click on it to watch the progress. It will:
    *   Build your Docker image.
    *   Push it to Google Artifact Registry.
    *   Deploy it to your GKE cluster.

## Step 5: Verify Live App

Once the Action is green (Success):

1.  **Get the External IP**:
    *   If you have `kubectl`: `kubectl get services`
    *   **Or go to GCP Console**: Kubernetes Engine > Services & Ingress > Copy the Endpoint IP.

2.  **Test your live agent**:
    ```bash
    curl -X POST http://<EXTERNAL-IP>:80/run-agents \
      -H "Content-Type: application/json" \
      -d '{"topic": "The Future of Space Travel"}'
    ```
