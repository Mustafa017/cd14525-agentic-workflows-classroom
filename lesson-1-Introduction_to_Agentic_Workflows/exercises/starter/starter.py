"""
Program Management Knowledge Agent - Starter Code

This program demonstrates two approaches to answering program management questions:
1. Using hardcoded knowledge
2. Using an LLM API

Complete the DONEs to build your knowledge agent.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict

# DONE: Initialize the OpenAI client if API key is available
# Hint: Use os.getenv() to get the API key from environment variables

load_dotenv()

open_api_key = os.getenv("OPENAI_API_KEY")
print(open_api_key)

client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=open_api_key
)

def get_hardcoded_answer(question:str):
    """
    Return answers to program management questions using hardcoded knowledge.
    
    Args:
        question (str): The question about program management
        
    Returns:
        str: The answer to the question
    """
    # DONE: Convert question to lowercase for easier matching
    question = question.lower()
    
    # DONE: Implement responses for at least 5 common program management questions
    # Include questions about: Gantt charts, Agile, sprints, critical path, and milestones

    # DONE: Add a default response for questions not in your knowledge base
    if "Gantt chart" in question:
        return "A Gantt chart is a type of bar chart that illustrates a project schedule, " \
        "showing start and end dates of tasks."
    elif "Agile" in question:
        return "It is a project management framework that emphasizes flexibility, collaboration, " \
        "and continuous improvement."
    elif "sprint" in question:
        return "A sprint is a set period during which specific work has to be completed and " \
        "made ready for review in project management"
    elif "critical path" in question:
        return "A critical path is the longest sequence of dependent activities" \
        "that determines the shortest time to complete a project."
    elif "milestones" in question:
        return "They are key checkpoints or significant events that mark important goals or " \
        "phases within a project's timeline."
    else:
        return "I'm sorry, I only have information on a few specific program management topics. " \
                "Could you ask about Gantt charts, Agile, sprints, critical path, or milestones?"

def get_llm_answer(question:str):
    """
    Get answers to program management questions using an LLM API.
    
    Args:
        question (str): The question about program management
        
    Returns:
        str: The answer from the LLM
    """
    # DONE: Check if the LLM client is initialized
    
    # DONE: Implement the API call to get an answer from the LLM
    # Use a system message to specify that the LLM should act as a program management expert
    
    # DONE: Add error handling for API calls

    messages:List[Dict[str, str]] = [
        {"role":"system", "content":"You are a program management expert"},
        {"role":"user", "content":question}
    ]
  
    if client is None:
        raise ValueError("A valid openAI client must be provided.")
    else:    
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )
    return response.choices[0].message.content

        

# Demo function to compare both approaches
def compare_answers(question:str):
    """Compare answers from both approaches for a given question."""
    print(f"\nQuestion: {question}")
    print("-" * 50)
    
    # DONE: Get and display the hardcoded answer
    print(f"\nHardcoded answer : {get_hardcoded_answer(question)}")
    # DONE: Get and display the LLM answer (or a placeholder message)
    print(f"\nLLM answer : {get_llm_answer(question)}")
    print("=" * 50)

# Demo with sample questions
if __name__ == "__main__":
    print("PROGRAM MANAGEMENT KNOWLEDGE AGENT DEMO")
    print("=" * 50)
    
    # DONE: Create a list of sample program management questions
    sample_questions = [
        "What is a Gantt chart?",
        "Tell me about Agile methodology.",
        "What are key project milestones?",
        "What is risk management in projects?", # This one might not be hardcoded
        "Can you explain a sprint review?"
    ]
    
    # DONE: Loop through the questions and compare answers
    for question in sample_questions:
        compare_answers(question)