import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import InMemoryRunner
from google.genai import types
from agents import researcher, writer

# Configure Environment for Vertex AI
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

app = FastAPI(
    title="Agent GKE Demo",
    description="ADK Agents running on GKE with FastAPI",
    version="1.0.0"
)

# Initialize Runners
researcher_runner = InMemoryRunner(agent=researcher)
writer_runner = InMemoryRunner(agent=writer)

class AgentInput(BaseModel):
    topic: str = "Artificial Intelligence in 2024"

class AgentOutput(BaseModel):
    topic: str
    research_summary: str
    blog_post: str

async def run_adk_agent(runner, prompt_text: str) -> str:
    session_id = str(uuid.uuid4())
    user_id = "api-user"
    
    # Create session
    await runner.session_service.create_session(
        session_id=session_id,
        app_name="InMemoryRunner",
        user_id=user_id
    )
    
    content = types.Content(parts=[types.Part(text=prompt_text)])
    
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.content:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
                    
    return response_text

@app.get("/")
async def health_check():
    return {"status": "Agent Service is Running (Google ADK + FastAPI Edition)!"}

@app.post("/run-agents", response_model=AgentOutput)
async def run_agents(input_data: AgentInput):
    try:
        # Agent 1: Research
        research_output = await run_adk_agent(researcher_runner, input_data.topic)
        
        # Agent 2: Write
        writer_input = f"Research Material:\n{research_output}"
        final_post = await run_adk_agent(writer_runner, writer_input)
        
        return AgentOutput(
            topic=input_data.topic,
            research_summary=research_output,
            blog_post=final_post
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
