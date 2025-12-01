# Part 3: Deployment & CI/CD

We use **GitHub Actions** to automatically build and deploy our agents to GKE. We use **Workload Identity Federation** for security, meaning we **do not** store any secrets or keys in GitHub.

## 1. Configure Workload Identity (One Time Setup)

This connects your GitHub Repository to Google Cloud permissions.

### A. Create the Pool & Provider
```bash
# Create Pool
gcloud iam workload-identity-pools create "github-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Pool"

# Create Provider
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Actions Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

### B. Grant Permissions
Allow your specific GitHub repository to impersonate your Service Account.

*Replace `victoraditya/agent-gke-demo` with your `username/repo`.*

```bash
# Get your Service Account email (created by GKE or manually)
export SA_EMAIL=local-dev-sa@${PROJECT_ID}.iam.gserviceaccount.com

# Grant Access
gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/github-pool/attribute.repository/victoraditya/agent-gke-demo"
```

## 2. Configure GitHub Secrets

Go to your **GitHub Repo > Settings > Secrets and variables > Actions**.
Add these Repository Secrets:

| Secret Name | Value |
| :--- | :--- |
| `GCP_PROJECT_ID` | `agent-gke-demo` (Your Project ID) |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider` |
| `GCP_SERVICE_ACCOUNT` | `local-dev-sa@agent-gke-demo.iam.gserviceaccount.com` |

*To get the long Provider string:*
```bash
gcloud iam workload-identity-pools providers describe github-provider \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --format="value(name)"
```

## 3. Deploy

1.  **Push your code** to the `main` branch.
2.  Go to the **Actions** tab in GitHub.
3.  Watch the **Build and Deploy** workflow.

## 4. Verify Live Deployment

Once the workflow is green, get your Load Balancer IP:

```bash
kubectl get service agent-gke-demo
```

Test it live:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"topic": "Cloud Security"}' \
  http://<EXTERNAL-IP>:80/run-agents
```

---

**🎉 Success!** Your agents are live in production. Move on to **[Part 4: Advanced Concepts](04_architecture_and_concepts.md)**.
