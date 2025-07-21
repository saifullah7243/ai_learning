import sys
import os
import asyncio
from typing import List, Dict, Any
import json

from openai import AsyncOpenAI, OpenAIError
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

async def get_json_output_task():
    system_prompt_json = (
        "You are an AI assistant that extracts product information from text and outputs it "
        "as a valid JSON object. The JSON object MUST contain exactly two keys: "
        "'product_name' (string) and 'price' (float)."
    )

    user_prompt_product = "The new 'UltraWidget X100' is now available for only $49.99!"
    try:
        console.rule("[bold cyan]OpenAI Json output Using response type josn format and prompt")
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt_json},
                {"role": "user", "content": user_prompt_product}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        raw_json_output = response.choices[0].message.content
        print(f"\n Raw LLM output: {raw_json_output}")

         # Verify if it's valid JSON 
        try: 
            parsed_json = json.loads(raw_json_output) 
            print("\nParsed JSON object:") 
            print(parsed_json) 
            if 'product_name' in parsed_json and 'price' in parsed_json: 
                print("\nJSON contains the required keys!") 
            else: 
                print("\nError: JSON does not contain all required keys.") 
        except json.JSONDecodeError as e: 
            print(f"\nError: Output was not valid JSON. Details: {e}") 

    except Exception as e:
        print(f"\n An API Error Occured")

# Run the async function
if __name__ == "__main__":
    asyncio.run(get_json_output_task())
