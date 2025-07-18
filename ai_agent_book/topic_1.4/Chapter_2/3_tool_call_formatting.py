import sys
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Rich console setup
console = Console()

# Load environment variables (optional but safe practice)
load_dotenv()

# Go 3 levels up from this file to reach ai_agent_course/
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_path)

# Now import from llm/config.py at root
from llm.config import openai_key

# Setup OpenAI client
client = AsyncOpenAI(api_key=openai_key)

async def get_llm_response(system_message_content: str | None, user_message_content: str) -> str:
    """
    Get a response from the LLM given system and user messages.
    Uses the gpt-4.1-nano model.
    """
    messages = []
    if system_message_content:
        messages.append({"role": "system", "content": system_message_content})
    messages.append({"role": "user", "content": user_message_content})

    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

async def conceptual_tool_call_task():
    system_message_tool_persona = """
You are 'CalcMate', a helpful shopping assistant. You are great at breaking down cost 
calculation problems. 
You have access to the following tool: 
Tool Name: `calculator` 
Description: Evaluates a mathematical expression string and returns a numerical result. 
Usage: `calculator.calculate(expression: str) -> number` 

When you need to use the calculator to determine a numerical result as part of your reasoning, 
you MUST state your intention to use it and the exact expression you would use. 
Format this as: 
ACTION: calculator.calculate(expression='<your mathematical expression string here>') 

Do not perform the final calculation yourself in the thought process. Just show the ACTION call. 
After showing the ACTION, you can then state what the next step would be 
(e.g., "Then I would present this total to the user.")
Always include the full mathematical expression for the final result inside the ACTION.
Do not break it into multiple tool calls unless strictly necessary.
"""

    user_message_for_tool = (
        "I want to buy 3 t-shirts that cost $25 each and one pair of shorts that cost $40. "
        "Can you tell me the steps to figure out the total cost and show me how you'd use the calculator for the math part?"
    )

    console.rule("[bold cyan] Conceptual Tool Call Task Response")
    response = await get_llm_response(system_message_content=system_message_tool_persona, user_message_content=user_message_for_tool)
    console.print(Markdown(response))


if __name__ == "__main__":
    asyncio.run(conceptual_tool_call_task())
