import os
from google.adk.agents.llm_agent import Agent

# Ensure PROJECT_ID is set
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

# Define the Researcher Agent
researcher = Agent(
    model='gemini-2.0-flash-exp',
    name='researcher',
    description="Researches a given topic thoroughly.",
    instruction="""
    You are a generic Researcher.
    Your goal is to research the given topic thoroughly and provide a detailed summary of key points.
    """
)

# Define the Writer Agent
writer = Agent(
    model='gemini-2.0-flash-exp',
    name='writer',
    description="Writes a compelling blog post based on research.",
    instruction="""
    You are a creative Writer.
    Your goal is to write a short, engaging blog post based on the provided research material.
    """
)
