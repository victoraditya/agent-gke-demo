# Part 2: Local Development Guide

Before deploying to the cloud, it's best to run and test the agents locally on your machine.

## 1. Understanding the Code

The project is structured as follows:

*   **`agents.py`**: Defines the AI Agents using **Google ADK**.
    *   `researcher`: Uses `gemini-2.0-flash-exp` to search/summarize.
    *   `writer`: Uses the summary to write a blog post.
*   **`main.py`**: The **FastAPI** web server.
    *   Exposes `POST /run-agents`.
    *   Orchestrates the flow: `Researcher -> Writer`.
*   **`Dockerfile`**: Packages the app for GKE.

## 2. Local Setup

### Install Dependencies
We recommend using a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Authentication
For local testing, we use your personal Google credentials (ADC).

```bash
gcloud auth application-default login
```
*This creates a temporary credential file that the ADK library will find automatically.*

### Set Environment Variables
The ADK needs to know it's running in Vertex AI mode.

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=agent-gke-demo
export GOOGLE_CLOUD_LOCATION=us-central1
```

## 3. Running the App

Start the FastAPI server using `uvicorn`.

```bash
uvicorn main:app --reload --port 8080
```

## 4. Testing

### Option A: Swagger UI (Browser)
Open **http://127.0.0.1:8080/docs**.
1.  Click **POST /run-agents**.
2.  Click **Try it out**.
3.  Enter a topic (e.g., `{"topic": "Future of AI"}`).
4.  Click **Execute**.

### Option B: Curl (Terminal)
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"topic": "Space Exploration"}' \
  http://127.0.0.1:8080/run-agents
```

---

**🎉 Success!** If you see a JSON response with a blog post, your code works. Move on to **[Part 3: Deployment](03_cicd_deployment.md)**.
