import sys
import os
import asyncio
from typing import List, Dict, Any

from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Rich console setup
console = Console()

# Load environment variables from .env
load_dotenv()

# Go 3 levels up to reach the root path of ai_agent_course/
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_path)

# Now import from llm/config.py at root level
try:
    from llm.config import openai_key
except ImportError:
    console.print("[bold red]Error:[/bold red] Could not import `openai_key` from llm.config")
    sys.exit(1)

# Setup OpenAI async client
client = AsyncOpenAI(api_key=openai_key)

# Define the message format
async def get_llm_response(prompt_message: list, temperature: float) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=prompt_message,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    
async def manual_react_turn_example():
    system_prompt_react = """ 
        You are MovieBot, an AI expert on films, designed to answer questions about movies. 
        To do this, you must use the following tools and output format strictly. 
        
        Available Tools: 
        1. `movie_db.find_director(movie_title: str) -> str`: Returns the director's name for a given movie. 
        2. `movie_db.find_release_year(movie_title: str) -> int`: Returns the release year for a given 
        movie. 
        
        Output Format: 
        Thought: [Your reasoning about what to do next, which tool to use, and why. If you have enough 
        information to answer, reason about how to construct the final answer.] 
        Action: [tool_name.method(parameter_name="value") OR FinalAnswer(answer_string="Your 
        final answer here.")] 
        
        After your Action, I will provide an Observation. You will then continue with Thought/Action. 
        Repeat this process until you can provide the FinalAnswer. Only use the tools provided. 
""" 
    initial_user_question = "Who directed the movie 'Inception' and what year was it released?"
    #  --- Turn 1: Ask initial question --- 
    console.rule("[bold cyan] --- --- ReAct Simulation: Turn 1 --- ---")
    messages_turn1 = [ 
        {"role": "system", "content": system_prompt_react}, 
        {"role": "user", "content": initial_user_question} 
    ] 

    console.print(Markdown(f"To LLM (User): {initial_user_question}")) 
    llm_response_turn1_content = await get_llm_response(messages_turn1, temperature=0.0) 
    console.print(Markdown(f"From LLM (Assistant):\n{llm_response_turn1_content}\n"))

    #  --- Turn 2: Provide Observation for director, expect action for year --- 
    console.rule("[bold cyan] --- --- ReAct Simulation: Turn 2 --- ---")
     # Developer simulates the tool call: movie_db.find_director(movie_title="Inception") 
    observation_director = "Christopher Nolan" # Simulated observation 
    console.print(Markdown(f"To LLM (User - providing observation): Observation: {observation_director}")) 
    messages_turn2 = messages_turn1 + [ 
        {"role": "assistant", "content": llm_response_turn1_content}, # Add LLM's previous response 
        {"role": "user", "content": f"Observation: {observation_director}"} 
    ] 
    llm_response_turn2_content = await get_llm_response(messages_turn2, temperature=0.0) 
    console.print(Markdown(f"From LLM (Assistant):\n{llm_response_turn2_content}\n")) 

    #  --- Turn 3: Provide Observation for year, expect FinalAnswer --- 
    console.rule("[bold cyan] --- --- ReAct Simulation: Turn 3 --- ---")
     # Developer simulates the tool call: movie_db.find_release_year(movie_title="Inception") 
    observation_year = "2010" # Simulated observation 
    print(f"To LLM (User - providing observation): Observation: {observation_year}") 
     
    messages_turn3 = messages_turn2 + [ 
        {"role": "assistant", "content": llm_response_turn2_content}, # Add LLM's previous response 
        {"role": "user", "content": f"Observation: {observation_year}"} 
    ] 
    llm_response_turn3_content = await get_llm_response(messages_turn3, temperature=0.0) 
    print(f"From LLM (Assistant):\n{llm_response_turn3_content}\n") 


# Run the async function
if __name__ == "__main__":
    asyncio.run(manual_react_turn_example())
