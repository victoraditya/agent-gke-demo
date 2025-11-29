import os
from flask import Flask, request, jsonify
from agents import ResearcherAgent, WriterAgent

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return "Agent Service is Running!"

@app.route('/run-agents', methods=['POST'])
def run_agents():
    data = request.json
    topic = data.get('topic', 'Artificial Intelligence in 2024')
    
    try:
        # Get Project ID from env
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        
        # Instantiate Agents
        researcher = ResearcherAgent(project=project_id)
        writer = WriterAgent(project=project_id)
        
        # Agent 1: Research
        research_output = researcher.run(topic)
        
        # Agent 2: Write
        final_post = writer.run(research_output)
        
        return jsonify({
            "topic": topic,
            "research_summary": research_output,
            "blog_post": final_post
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For local testing, you might want to set a port
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
