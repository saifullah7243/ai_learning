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
async def llm_response(system_prompt:str, prompt_text:str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
             messages=[ 
                {"role": "system", "content":system_prompt }, 
                {"role": "user", "content": prompt_text} 
            ],
            temperature=0.1,
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
    

async def main():
    console.rule("[bold blue] Before changing prompt")
    system_message = "You are English Subject expert, Rewrite the english senteces"
    user_prompt ="Next, we’ll test different prompts using Python to find the best one. This helps improve quality, speed, and cost, without using big tools. Let’s begin experimenting"
    response_1 = await llm_response(system_prompt=system_message, prompt_text=user_prompt)
    console.print(Markdown(response_1))

    console.rule("[bold Red] After changing prompt(Baseline + Changing)")
    system_message = "You are English Subject expert, Rewrite the sentence to make it more formal and academic"
    user_prompt ="Next, we’ll test different prompts using Python to find the best one. This helps improve quality, speed, and cost, without using big tools. Let’s begin experimenting"
    response_2 = await llm_response(system_prompt=system_message, prompt_text=user_prompt)
    console.print(Markdown(response_2))

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
