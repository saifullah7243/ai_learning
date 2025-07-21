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
    
async def few_shot_cot():
    system_prompt = "You are a logical reasoning assistant. Solve the following problems by thinking step-by-step, then give the final answer." 
 
    # Exemplars will be structured in the messages list 
    messages:List[Dict[str, str]] = [ 
        {"role": "system", "content": system_prompt}, 
        # Example 1 
        {"role": "user", "content": """ 
        Question: 
        Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. 
        How many tennis balls does he have now? 
        """}, 
        {"role": "assistant", "content": """ 
        Step 1: Roger starts with 5 tennis balls. 
        Step 2: He buys 2 more cans of tennis balls. 
        Step 3: Each can has 3 tennis balls. So, 2 cans have 2 * 3 = 6 tennis balls. 
        Step 4: Roger's total tennis balls are the initial amount plus the new ones: 5 + 6 = 11 tennis 
        balls. 
        The final answer is 11. 
        """}, 
        # Example 2 
        {"role": "user", "content": """ 
        Question: 
        The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many 
        apples do they have? 
        """}, 
        {"role": "assistant", "content": """ 
        Step 1: The cafeteria started with 23 apples. 
        Step 2: They used 20 apples for lunch. So, they had 23 - 20 = 3 apples left. 
        Step 3: Then they bought 6 more apples. So, they now have 3 + 6 = 9 apples. 
        The final answer is 9. 
        """}, 
        # New Problem for the LLM 
        {"role": "user", "content": """ 
        Question: 
        Natalia sold clips to 48 of her friends and then divided the total clips into 9 equal boxes. 
        If Natalia sold 2 clips to each friend, how many clips are in each box, assuming clips 
        cannot be broken and each box must contain an equal number of clips with any remainder set 
        aside? 
        """} 
    ] 
    console.rule("[bold cyan] --- Few-Shot CoT Example (Explicit Instruction) ---")

    response = await get_llm_response(prompt_message=messages, temperature=0.3) 
    console.print(Markdown(f"Question:\n{messages[-1]['content']}\n")) 
    console.print(Markdown(f"LLM Response:\n{response}"))

# Run the async function
if __name__ == "__main__":
    asyncio.run(few_shot_cot())
