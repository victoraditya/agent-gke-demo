# Observability Guide for Agentic AI

Observability is critical for AI agents because you need to know *why* an agent gave a specific answer, not just *if* the server is running.

## 1. The Three Layers of Observability

| Layer | What it tells you | Tooling |
| :--- | :--- | :--- |
| **Infrastructure** | "Is the pod crashing? Is CPU high?" | **GKE Dashboard / Cloud Monitoring** |
| **Application** | "Did the API return 200 OK?" | **Cloud Logging (stdout)** |
| **AI / Logic** | "What prompt was sent? Why did it choose that tool?" | **LangSmith / OpenTelemetry** |

---

## 2. Infrastructure & Logs (Already Built-in)

Because we deployed to GKE, you get this for free:

*   **Logs**: Go to GCP Console > **Logging**. You will see every `print()` statement from your Python code.
*   **Metrics**: Go to GCP Console > **Kubernetes Engine** > **Observability**. You see CPU, Memory, and Restart counts.

**Action Item**: Add more structured logging to `main.py`.
```python
import logging
# Use JSON logging for better parsing in Cloud Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.info('{"event": "agent_start", "topic": "AI"}')
```

---

## 3. AI Tracing (The Missing Piece)

To see the "Chain of Thought" (e.g., Researcher -> Gemini -> Summary -> Writer), you need **Tracing**.

### Option A: LangSmith (Easiest for LangChain)
If you use LangChain, this is the native way.

1.  Sign up for LangSmith.
2.  Add environment variables in `k8s/deployment.yaml`:
    ```yaml
    env:
      - name: LANGCHAIN_TRACING_V2
        value: "true"
      - name: LANGCHAIN_API_KEY
        valueFrom:
          secretKeyRef:
            name: langchain-secret
            key: api-key
    ```
3.  **Result**: You see a beautiful UI showing every step the agent took.

### Option B: OpenTelemetry (Enterprise Standard)
If you want to send data to **Dynatrace**, **Splunk**, or **Google Cloud Trace**.

1.  Install packages:
    ```bash
    pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-langchain
    ```
2.  Initialize in `main.py`:
    ```python
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
    # Or export to Google Cloud Trace
    ```

### Option C: Google Cloud Trace (Native)
Since you are on GCP, you can send traces directly to Cloud Trace.

1.  Add `opencensus-ext-stackdriver` to `requirements.txt`.
2.  It links the "Trace" in GCP Console to the "Log" entry.

---

## 4. Recommendation for You

**Start with Option A (LangSmith)** for development. It is purpose-built for debugging prompts.

**Move to Option B (OpenTelemetry)** for production if your company uses Dynatrace/Splunk, so your AI metrics sit alongside your database metrics.
