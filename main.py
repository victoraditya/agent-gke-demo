import os
import uuid
import asyncio
from flask import Flask, request, jsonify
from google.adk.runners import InMemoryRunner
from google.genai import types
from agents import researcher, writer

# Configure Environment for Vertex AI
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
# GOOGLE_CLOUD_PROJECT and LOCATION should be set in env or Dockerfile
# GOOGLE_APPLICATION_CREDENTIALS should be set for local test

app = Flask(__name__)

# Initialize Runners
# We use InMemoryRunner for simplicity in this PoC.
# In production, you might use a persistent runner or a different architecture.
researcher_runner = InMemoryRunner(agent=researcher)
writer_runner = InMemoryRunner(agent=writer)

async def run_adk_agent(runner, prompt_text):
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

@app.route('/', methods=['GET'])
def health_check():
    return "Agent Service is Running (Google ADK Edition)!"

@app.route('/run-agents', methods=['POST'])
async def run_agents():
    data = request.json
    topic = data.get('topic', 'Artificial Intelligence in 2024')
    
    try:
        # Agent 1: Research
        research_output = await run_adk_agent(researcher_runner, topic)
        
        # Agent 2: Write
        # We pass the research output as input to the writer
        writer_input = f"Research Material:\n{research_output}"
        final_post = await run_adk_agent(writer_runner, writer_input)
        
        return jsonify({
            "topic": topic,
            "research_summary": research_output,
            "blog_post": final_post
        })
    except Exception as e:
        app.logger.error(f"Error running agents: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
