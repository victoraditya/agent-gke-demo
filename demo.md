# Demo Runbook: Recreating the Environment

Use this guide to quickly bring your Agentic AI demo back to life after you have deleted the cluster to save money.

## Phase 1: Rehydrate Infrastructure (10-15 mins)

Since you deleted the cluster, you need to recreate it.

### 1. Recreate the GKE Cluster
Run this command to create a cost-optimized cluster with **Workload Identity** enabled (Critical!).

```bash
gcloud container clusters create agent-cluster \
  --zone us-central1-a \
  --machine-type e2-small \
  --num-nodes 1 \
  --spot \
  --disk-size=30GB \
  --enable-autoscaling --min-nodes 1 --max-nodes 3 \
  --workload-pool=agent-gke-demo.svc.id.goog
```
*(Replace `agent-gke-demo` with your Project ID if different)*

### 2. Recreate Artifact Registry (If deleted)
If you also deleted the image repository, recreate it:

```bash
gcloud artifacts repositories create agent-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for Agent GKE Demo"
```

---

## Phase 2: Trigger Deployment (2 mins)

Since your code is already on GitHub, you just need to trigger the Action to deploy to the new cluster.

1.  Go to your **GitHub Repository** > **Actions**.
2.  Select the **"Build and Deploy to GKE"** workflow on the left.
3.  Click **Run workflow** (button on the right) > **Run workflow**.

*Alternatively, you can make a small change to `README.md` and push it to trigger a build.*

---

## Phase 3: The Demo (1 min)

Once the GitHub Action finishes successfully:

### 1. Get the IP
```bash
# Get credentials for the new cluster
gcloud container clusters get-credentials agent-cluster --zone us-central1-a

# Find the IP
kubectl get service agent-gke-demo
```
*(Copy the `EXTERNAL-IP`)*

### 2. Run the Agent
Show this command to your audience:

```bash
curl -X POST http://<EXTERNAL-IP>:80/run-agents \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Future of Artificial Intelligence"}'
```

### 3. Show the Logs (Optional "Wow" Factor)
To show the agent "thinking" in real-time:

```bash
kubectl logs -f deployment/agent-gke-demo
```

---

## Phase 4: Teardown (Save Money!)

Don't forget to delete the cluster immediately after the demo.

```bash
gcloud container clusters delete agent-cluster --zone us-central1-a
```
