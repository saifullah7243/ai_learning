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

# Ensure project root (ai_agent_book/) is in sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

# Import config loader from utils
from utils.config_loader import load_config
config = load_config()
openai_key = config.openai_key

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
    
async def zero_shot_cot():
   system_prompt_cot = "You are a meticulous math problem solver. When asked a question, first provide a step-by-step derivation of your thought process, and then state the final answer clearly prefixed with 'The final answer is '." 
   user_prompt_explicit_cot = """ 
    Natalia sold clips to 48 of her friends and then divided the clips into 9 equal boxes. 
    If Natalia sold 2 clips to each friend, how many clips are in each box? 
    Please show your reasoning. 
    """ 

   messages = [
        {"role": "system", "content": system_prompt_cot},
        {"role": "user", "content": user_prompt_explicit_cot},
    ]

   console.rule("[bold cyan] --- Zero-Shot CoT Example (Explicit Instruction) ---")

   response = await get_llm_response(prompt_message=messages, temperature=0.3) 
   console.print(Markdown(f"Question:\n{user_prompt_explicit_cot}\n")) 
   console.print(Markdown(f"LLM Response:\n{response}"))

# Run the async function
if __name__ == "__main__":
    asyncio.run(zero_shot_cot())
