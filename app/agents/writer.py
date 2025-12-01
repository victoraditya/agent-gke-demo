import os
from google.adk.agents.llm_agent import Agent

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
