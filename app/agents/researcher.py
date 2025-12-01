import os
from google.adk.agents.llm_agent import Agent

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
