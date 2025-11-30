# Google Cloud Platform (GCP) Prerequisites Guide

This guide provides detailed, beginner-friendly steps to set up your Google Cloud environment for the Agentic AI project.

## Step 1: Create a Google Cloud Project

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Sign in with your Google account.
3.  Click the **Select a project** dropdown at the top left of the page.
4.  Click **New Project** (top right of the popup).
5.  **Project Name**: Enter a name (e.g., `agent-gke-demo`).
6.  **Billing Account**: You must link a billing account. If you are a new user, you might have free credits.
7.  Click **Create**.
8.  Wait a moment, then select your new project from the notification bell or the project dropdown.

## Step 2: Enable Required APIs

We need to tell Google Cloud which services we want to use.

1.  Open the **Navigation Menu** (three lines at top left) > **APIs & Services** > **Library**.
2.  Search for and **Enable** the following APIs one by one:
    *   **Vertex AI API** (for the AI models)
    *   **Kubernetes Engine API** (for the cluster)
    *   **Artifact Registry API** (to store Docker images)
    *   **Cloud Resource Manager API** (required for some permission changes)
    *   **Cloud Build API** (optional, but good to have)

## Step 3: Create a Service Account

This is like a "robot user" that GitHub Actions will use to deploy your code.

1.  Go to **IAM & Admin** > **Service Accounts**.
2.  Click **+ CREATE SERVICE ACCOUNT**.
3.  **Service account name**: `github-deployer` (or similar).
4.  Click **Create and Continue**.
5.  **Grant this service account access to project**: Add these roles:
    *   **Kubernetes Engine Developer** (to deploy to GKE)
    *   **Artifact Registry Admin** (to create/push images)
    *   **Vertex AI User** (to use the AI models)
    *   **Service Account User**
    *   **Storage Admin** (often needed for build logs)
6.  Click **Continue**, then **Done**.

## Step 4: Generate a Key (Optional / Local Dev Only)
 
 **Note**: For CI/CD, we now use **Workload Identity Federation**, so you do **NOT** need this key for GitHub Actions. You might still want it for local testing if `gcloud auth` doesn't work.
 
 1.  In the Service Accounts list, click on the email address of the account you just created.
 2.  Go to the **KEYS** tab (top bar).
 3.  Click **ADD KEY** > **Create new key**.
 4.  Select **JSON**.
 5.  Click **Create**.
 6.  A file will automatically download to your computer. **Keep this safe!**

## Step 5: Install Google Cloud CLI (gcloud)

If you haven't already:

1.  Download and install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) for your OS.
2.  Open your terminal and run:
    ```bash
    gcloud init
    ```
3.  Follow the prompts to log in and select the project you created in Step 1.

## Step 6: Create Artifact Registry Repository

We need a place to store your Docker images. Google is replacing "Container Registry" with "Artifact Registry".

```bash
gcloud artifacts repositories create agent-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for Agent GKE Demo"
```

## Step 7: Create the GKE Cluster (With Workload Identity)

Now we create the "computer" that will run your code. We will create a **Standard** cluster using **Spot instances** and enable **Workload Identity** (Crucial for security and AI model access).

1.  Open your terminal.
2.  Copy and run this exact command (replace `PROJECT_ID` with your actual project ID):

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

    *   **`--workload-pool`**: Enables Workload Identity. **Replace `PROJECT_ID` with your actual ID (e.g., `agent-gke-demo`).**
    *   **`--spot`**: Uses spare capacity for ~60-90% discount.
    *   **`--machine-type e2-small`**: A small, cheap machine type.

    > **Important**: If you encounter "403 Permission Denied" errors later, run this command to ensure the nodes are using the GKE Metadata Server:
    > ```bash
    > gcloud container node-pools update default-pool --cluster agent-cluster --zone us-central1-a --workload-metadata=GKE_METADATA
    > ```

3.  Wait for a few minutes. When it finishes, you will see a success message.

**You are now ready to proceed to `step.md`!**
