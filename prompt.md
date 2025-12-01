# Master Prompt for Agentic AI Platform Replication

**Role**: You are a Senior Staff Software Engineer and Cloud Architect at Google.

**Objective**: Build a production-ready, enterprise-grade **Agentic AI Platform** from scratch. The system must orchestrate AI agents to perform complex tasks (Research + Writing) using **Google Vertex AI** and **Google ADK (Agent Development Kit)**. It must be deployed on **GKE (Google Kubernetes Engine)** with a secure, keyless CI/CD pipeline using **GitHub Actions** and **Workload Identity Federation**.

---

## 1. Technology Stack 🛠️

*   **Language**: Python 3.12+
*   **Web Framework**: FastAPI (Async, Pydantic validation)
*   **AI Framework**: `google-adk` (Google Agent Development Kit)
*   **AI Model**: `gemini-2.0-flash-exp` (via Vertex AI)
*   **Containerization**: Docker (Multi-stage build, non-root user)
*   **Orchestration**: Kubernetes (GKE Standard/Autopilot)
*   **CI/CD**: GitHub Actions
*   **Security**: Workload Identity Federation (No Service Account Keys!)

---

## 2. Project Structure 📂

Enforce this exact modular structure:

```text
agent-gke-demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI Entrypoint & Orchestration Logic
│   └── agents/              # Individual Agent Definitions
│       ├── __init__.py
│       ├── researcher.py    # Researcher Agent (ADK)
│       └── writer.py        # Writer Agent (ADK)
├── k8s/                     # Kubernetes Manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── serviceaccount.yaml  # With Workload Identity Annotation
├── .github/workflows/
│   └── deploy.yaml          # CI/CD Pipeline
├── docs/                    # Documentation
├── Dockerfile               # Production-grade Dockerfile
├── requirements.txt         # Python Dependencies
└── .gitignore
```

---

## 3. Implementation Details 💻

### A. The Agents (`app/agents/`)
Create two agents using `google.adk.agents.llm_agent.Agent`:
1.  **Researcher**:
    *   **Model**: `gemini-2.0-flash-exp`
    *   **Role**: "You are a generic Researcher. Research the topic thoroughly."
2.  **Writer**:
    *   **Model**: `gemini-2.0-flash-exp`
    *   **Role**: "You are a creative Writer. Write a blog post based on the research."

### B. The API (`app/main.py`)
*   Use **FastAPI**.
*   Initialize `InMemoryRunner` for both agents.
*   **Endpoint**: `POST /run-agents`
    *   **Input**: `{"topic": "str"}`
    *   **Flow**:
        1.  Call Researcher Runner with topic.
        2.  Pass Researcher output to Writer Runner.
        3.  Return JSON: `{"research": "...", "blog": "..."}`.
*   **Async**: Use `async def` and `await runner.run_async()`.

### C. Dockerfile
*   Use `python:3.12-slim` as base.
*   Install dependencies from `requirements.txt`.
*   Create a non-root user `appuser`.
*   **CMD**: `exec uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### D. Kubernetes Manifests (`k8s/`)
1.  **ServiceAccount**: Name `agent-sa`. Annotation: `iam.gke.io/gcp-service-account: agent-sa@{PROJECT_ID}.iam.gserviceaccount.com`.
2.  **Deployment**:
    *   Replicas: 1
    *   Image: `us-central1-docker.pkg.dev/{PROJECT_ID}/agent-repo/agent-image:latest`
    *   ServiceAccountName: `agent-sa`
    *   Resources: Requests (CPU 500m, Mem 512Mi), Limits (CPU 1000m, Mem 1Gi).
3.  **Service**: Type `LoadBalancer`, Port 80 -> TargetPort 8080.

### E. CI/CD (`.github/workflows/deploy.yaml`)
*   **Trigger**: Push to `main`.
*   **Permissions**: `id-token: write`, `contents: read`.
*   **Steps**:
    1.  Checkout code.
    2.  **Auth**: `google-github-actions/auth` using `workload_identity_provider`.
    3.  **Build & Push**: `docker build` and push to Artifact Registry.
    4.  **Deploy**: `google-github-actions/deploy-gke`.

---

## 4. Infrastructure Setup Instructions (Bash Script) 🏗️

Provide the exact `gcloud` commands to set this up:

1.  **Variables**: Set `PROJECT_ID`, `REGION=us-central1`.
2.  **APIs**: Enable `container`, `artifactregistry`, `iamcredentials`, `aiplatform`.
3.  **Artifact Registry**: Create `agent-repo`.
4.  **GKE Cluster**: Create `agent-cluster` with **Workload Identity** enabled and **Spot Instances** (for cost).
5.  **IAM Binding**: Bind the Kubernetes Service Account (`agent-sa`) to the Google Service Account (`agent-sa`) using `roles/iam.workloadIdentityUser`.
6.  **GitHub Auth**: Create Workload Identity Pool `github-pool` and Provider `github-provider`. Grant `roles/iam.workloadIdentityUser` to the GitHub repo principal.

---

## 5. Definition of Done ✅

The output must include:
1.  All source code files.
2.  All configuration files (K8s, Docker, GitHub).
3.  A `README.md` explaining how to run it locally (`uvicorn`) and deploy it (git push).

**Generate the complete project now.**
