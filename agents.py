import os
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class Agent:
    def __init__(self, role, goal, model_name="gemini-2.0-flash-exp", project=None):
        self.role = role
        self.goal = goal
        self.llm = VertexAI(model_name=model_name, project=project)
    
    def run(self, input_text):
        raise NotImplementedError("Subclasses must implement run method")

class ResearcherAgent(Agent):
    def __init__(self, project=None):
        super().__init__(role="Researcher", goal="Research the given topic thoroughly.", project=project)
        self.template = """
        You are a generic Researcher.
        Your goal is to: {goal}
        
        Topic: {topic}
        
        Provide a detailed summary of the key points regarding this topic.
        """
        self.prompt = PromptTemplate(template=self.template, input_variables=["goal", "topic"])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def run(self, topic):
        print(f"[{self.role}] Researching topic: {topic}...")
        return self.chain.invoke({"goal": self.goal, "topic": topic})

class WriterAgent(Agent):
    def __init__(self, project=None):
        super().__init__(role="Writer", goal="Write a compelling blog post based on research.", project=project)
        self.template = """
        You are a creative Writer.
        Your goal is to: {goal}
        
        Research Material:
        {research_material}
        
        Write a short, engaging blog post based on the above research.
        """
        self.prompt = PromptTemplate(template=self.template, input_variables=["goal", "research_material"])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def run(self, research_material):
        print(f"[{self.role}] Writing blog post...")
        return self.chain.invoke({"goal": self.goal, "research_material": research_material})
