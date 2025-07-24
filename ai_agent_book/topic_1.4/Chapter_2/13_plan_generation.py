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
    
# async def plan_generation_task(): 
#     system_prompt_planner = ( 
#         "You are 'ProjectPlannerAI', an expert AI assistant skilled at breaking down " 
#         "software development projects into clear, manageable, and actionable steps. " 
#         "The plans should be high-level but cover the essential phases." 
#     ) 
#     user_prompt_todo_app = """ 
#     I want to build a simple command-line To-Do list application in Python. 
#     Please generate a 4-step plan for creating this application. The plan should cover: 
#     1. Defining the core features and task structure. 
#     2. Deciding on a simple data storage mechanism (e.g., JSON or CSV file). 
#     3. Implementing basic CRUD (Create, Read, Update, Delete) operations for tasks. 
#     4. Designing and implementing the command-line interface for user interaction. 
 
#     Output the plan as a numbered list, with each step briefly described. 
#     """ 
 
#     messages = [ 
#         {"role": "system", "content": system_prompt_planner}, 
#         {"role": "user", "content": user_prompt_todo_app} 
#     ] 
 
#     console.print(Markdown("--- Plan Generation Task (To-Do App) ---")) 
#     response = await get_llm_response(messages, temperature=0.3) 
#     console.print(Markdown(f"User Request:\n{user_prompt_todo_app}\n")) 
#     console.print(Markdown(f"Generated Plan:\n{response}")) 

async def execute_step_3_crud_operations():
    system_prompt_executor = (
        "You are 'PythonCodeCrafter', an expert Python developer. "
        "You help implement features based on detailed plans."
    )

    step_context = """
    Based on the following plan, please execute Step 2.
    1. Defining the core features and task structure. 
    2. Deciding on a simple data storage mechanism (e.g., JSON or CSV file). 
    3. Implementing basic CRUD (Create, Read, Update, Delete) operations for tasks.
        • Write functions to add new tasks, retrieve and display existing tasks, update task details, and delete tasks.        
        • Ensure data consistency by updating the JSON file after each operation.
        • Handle edge cases, such as invalid task IDs or empty task lists. 
    4. Designing and implementing the command-line interface for user interaction. 
    """

    messages = [
        {"role": "system", "content": system_prompt_executor},
        {"role": "user", "content": step_context}
    ]

    console.print(Markdown("--- Execution Task: Implement CRUD Operations ---"))
    response = await get_llm_response(messages, temperature=0.3)
    console.print(Markdown(response))


# Run the async function
if __name__ == "__main__":
    asyncio.run(execute_step_3_crud_operations())
