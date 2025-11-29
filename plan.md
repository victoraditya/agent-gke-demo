# How to Build Your Own AI Agent Using This Project

This repository is designed to be a **production-ready template** for deploying Agentic AI applications on Google Cloud. You can use it as a baseline to build completely different agents (e.g., a Customer Support Bot, a Data Analyst, or a Creative Writer) without reinventing the wheel.

## 1. Architecture Overview

Understanding the pieces will help you know what to change:

*   **The Brain (`agents.py`)**: This contains the logic. It uses **LangChain** and **Vertex AI** to define *what* the agent does.
*   **The Body (`main.py`)**: This is a **Flask** web server. It receives requests (JSON) and triggers the agents.
*   **The Container (`Dockerfile`)**: Packages everything into a lightweight image.
*   **The Infrastructure (`k8s/`)**: Kubernetes configuration to run the container on GKE.
*   **The Pipeline (`.github/workflows/`)**: Automates the build and deployment.

---

## 2. How to Customize This Project

Follow these steps to turn this "Researcher/Writer" demo into your own product.

### Step A: Define Your Agent Logic (`agents.py`)
This is where 90% of your work will happen.

1.  **Change the Prompt**: Look at the `prompt` variable in the `Agent` class.
    *   *Current*: "You are a researcher..."
    *   *New*: "You are a senior SQL analyst. Given a schema, write a query..."
2.  **Change the Model**: In `__init__`, change `model_name`.
    *   `gemini-1.5-flash`: Fast, cheap (good for simple tasks).
    *   `gemini-1.5-pro`: Smarter, more expensive (good for complex reasoning).
3.  **Add Tools**: If your agent needs to search the web or query a database, add LangChain Tools here.

### Step B: Update the API (`main.py`)
If your agent needs different inputs (e.g., a file upload instead of a text topic), change the Flask route.

1.  **Input Parsing**: Change `data = request.json`.
2.  **Orchestration**: If you have multiple agents, change how they call each other in the `/run-agents` function.

### Step C: Local Testing
Always test locally before deploying.

1.  Set your credentials: `export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/key.json`
2.  Run: `python main.py`
3.  Test: `curl -X POST http://localhost:8080/...`

---

## 3. Reusing the Infrastructure (The "Free" Stuff)

The best part of this template is that you **don't** need to touch the infrastructure code for most changes.

*   **Dockerfile**: Generic. Works for any Python app with `requirements.txt`.
*   **CI/CD (`deploy.yaml`)**: Generic. It will build *whatever* is in your folder and deploy it.
*   **Kubernetes (`k8s/`)**: Generic. It exposes port 8080.

**When to change Infrastructure:**
*   **High Memory**: If your agent loads large files, increase `memory: "512Mi"` in `k8s/deployment.yaml`.
*   **High CPU**: If you do heavy processing, increase `cpu: "250m"`.
*   **Secrets**: If your agent needs an API key (e.g., for Slack), add it as a Kubernetes Secret and mount it in `deployment.yaml`.

---

## 4. Deployment Checklist for a New Project

If you fork this repo for a new project:

1.  **Create a New GCP Project**: Don't mix environments.
2.  **Create a New Repo**: Copy the files.
3.  **Set Secrets**: Add `GCP_PROJECT_ID`, `GCP_SA_KEY`, etc., to the new GitHub repo.
4.  **Push**: The CI/CD pipeline will handle the rest.

## 5. Cost & Scaling Tips

*   **Scale to Zero**: GKE Standard doesn't scale to zero nodes easily. If you want true serverless, consider **Cloud Run** (this code works there too!).
*   **Spot Instances**: Keep `k8s/deployment.yaml` replicas low (1) and use Spot instances (as configured in our cluster setup) to save ~70%.
