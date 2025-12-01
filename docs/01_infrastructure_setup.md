# Part 1: Infrastructure Setup

This guide will help you set up the Google Cloud infrastructure required to run the agents. We use **Google Kubernetes Engine (GKE)** for compute and **Artifact Registry** to store our Docker images.

## Prerequisites

1.  **Google Cloud Account**: You need an active GCP project with billing enabled.
2.  **gcloud CLI**: Installed and authenticated (`gcloud auth login`).
3.  **kubectl**: Installed (`gcloud components install kubectl`).

---

## Step 1: Initialize Environment

Open your terminal and set your Project ID variable.
*Replace `agent-gke-demo` with your actual Project ID.*

```bash
export PROJECT_ID=agent-gke-demo
gcloud config set project $PROJECT_ID
```

## Step 2: Enable APIs

We need to enable the services we will use.

```bash
gcloud services enable \
    container.googleapis.com \
    artifactregistry.googleapis.com \
    iamcredentials.googleapis.com \
    aiplatform.googleapis.com \
    cloudbuild.googleapis.com
```

## Step 3: Create Artifact Registry

This is where your Docker images will live.

```bash
gcloud artifacts repositories create agent-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for Agent GKE Demo"
```

## Step 4: Create GKE Cluster

We will create a cost-effective cluster using **Spot Instances** and **Workload Identity**.

*   **Workload Identity**: Allows our code to authenticate securely without keys.
*   **Spot Instances**: Saves ~60-90% on compute costs.

```bash
gcloud container clusters create agent-cluster \
  --zone us-central1-a \
  --machine-type e2-small \
  --num-nodes 1 \
  --spot \
  --disk-size=30GB \
  --enable-autoscaling --min-nodes 1 --max-nodes 3 \
  --workload-pool=${PROJECT_ID}.svc.id.goog
```

## Step 5: Connect kubectl

Configure your local `kubectl` tool to talk to the new cluster.

```bash
gcloud container clusters get-credentials agent-cluster --zone us-central1-a
```

Verify the connection:
```bash
kubectl get nodes
```
*You should see one node with status `Ready`.*

---

**🎉 Success!** Your infrastructure is ready. Move on to **[Part 2: Local Development](02_local_development.md)**.

---

## 6. Cost Management (Cleanup & Restart) 💸

**⚠️ Important**: GKE clusters cost money even when idle. If you are done for the day, delete the cluster to avoid charges.

### How to Delete (Stop Billing)
Run these commands to delete the expensive resources:

```bash
# 1. Delete the GKE Cluster (Stops Compute Charges)
gcloud container clusters delete agent-cluster --zone us-central1-a --quiet

# 2. (Optional) Delete Artifact Registry (Stops Storage Charges)
# Only do this if you want to delete your Docker images too.
gcloud artifacts repositories delete agent-repo --location=us-central1 --quiet
```

### How to Restart (Start Everything Again)
When you want to work again, just re-run **Step 3** (if you deleted the repo) and **Step 4** (Cluster creation) from this guide.

1.  **Create Cluster**:
    ```bash
    gcloud container clusters create agent-cluster \
      --zone us-central1-a \
      --machine-type e2-small \
      --num-nodes 1 \
      --spot \
      --disk-size=30GB \
      --enable-autoscaling --min-nodes 1 --max-nodes 3 \
      --workload-pool=${PROJECT_ID}.svc.id.goog
    ```
2.  **Reconnect**:
    ```bash
    gcloud container clusters get-credentials agent-cluster --zone us-central1-a
    ```
3.  **Deploy**: Push your code to GitHub again, or trigger the workflow manually to re-deploy your app.
