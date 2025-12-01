# Agent GKE Platform: The Complete Handbook

Welcome! This repository contains a production-ready **Agentic AI Platform** running on **Google Kubernetes Engine (GKE)**.

It is designed for beginners and enterprise teams alike, using the latest Google technologies:
*   **Google ADK (`google-adk`)**: The official Python library for building agents.
*   **FastAPI**: High-performance, async-native web framework.
*   **Workload Identity**: Keyless, secure authentication for CI/CD.

## 📚 Documentation Guide

We have organized the documentation to take you from "Zero" to "Production".

### 1. [Infrastructure Setup](docs/01_infrastructure_setup.md)
**Start Here.** How to set up your Google Cloud Project, GKE Cluster, and Artifact Registry.
*   *Replaces: `gkeprerequisite.md`, `SleepToRun.md`*

### 2. [Local Development](docs/02_local_development.md)
How to run the agents on your laptop, understand the code (`agents.py`, `main.py`), and test with `curl`.
*   *Replaces: `local_testing.md`, `explanation.md`*

### 3. [Deployment & CI/CD](docs/03_cicd_deployment.md)
How to automate deployment using GitHub Actions and Workload Identity Federation.
*   *Replaces: `step.md`, `demo.md`*

### 4. [Architecture & Advanced Concepts](docs/04_architecture_and_concepts.md)
Deep dive into the system design, ADK vs LangChain, and Observability (Tracing).
*   *Replaces: `architecture.md`, `observability.md`, `plan.md`, `agent_starter_pack.md`*

---

## 🚀 Quick Start (If you just want to run it)

1.  **Clone** this repo.
2.  **Follow Guide #1** to create your cluster.
3.  **Follow Guide #3** to push your code and deploy.
