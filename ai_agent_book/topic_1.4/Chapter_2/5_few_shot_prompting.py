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

async def get_llm_response(messages_list: list) -> str:
    """
    Get a response from the LLM given system and user messages.
    Uses the gpt-4.1-nano model.
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages_list,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

async def few_shot_style_transfer_task(): 
    system_prompt_style ="""
    You are an expert editor specializing in transforming informal text 
    into formal, professional language. Preserve the core meaning completely. Only output the 
    transformed text. 
    """
 
 # Few-shot examples using user/assistant roles 
    messages = [ 
        {"role": "system", "content": system_prompt_style}, 
        {"role": "user", "content": "Hey, gotta cancel our meeting tomorrow, something came up."}, 
        {"role": "assistant", "content": "I regret to inform you that I must cancel our scheduled meeting for tomorrow due to an unforeseen circumstance. I apologize for any inconvenience this may cause."}, 
        {"role": "user", "content": "Can u send me the report ASAP?"}, 
        {"role": "assistant", "content": "Please send me the report soon."}, 
        {"role": "user", "content": "lol, that bug was a real pain in the neck!"}, # Another example 
        {"role": "assistant", "content": "That particular software defect presented a significant challenge."}, 
        # New query for the LLM to complete 
        {"role": "user", "content": "btw, the team loved ur presentation, it was awesome!"} 
    ]

    console.rule("[bold cyan]  Few-Shot Style Transfer Task ")
    formal_output = await get_llm_response(messages_list=messages) 
    console.print(Markdown(f"Informal Input: btw, the team loved ur presentation, it was awesome!")) 
    console.print(Markdown(f"Formal Output: {formal_output}"))

    console.rule("[bold blue] Test_1 with differet input that not in few_shot")
    messages_test_2 = messages[:-1] + [{"role": "user", "content": "Thx for the docs, they look good."}]
    formal_output_2 = await get_llm_response(messages_list=messages_test_2) 
    print(f"Informal Input: Thx for the docs, they look good.")
    console.print(Markdown(f"Formal Output: {formal_output_2}"))

    console.rule("[bold blue] Test_2 with differet input that not in few_shot")
    messages_test_3 = messages[:-1] + [{"role": "user", "content": "yo, can u hook me up with that API endpoint real quick?"}]
    formal_output_3 = await get_llm_response(messages_list=messages_test_3) 
    print(f"yo, can u hook me up with that API endpoint real quick?")
    console.print(Markdown(f"Formal Output: {formal_output_3}"))
 
if __name__ == "__main__":
    asyncio.run(few_shot_style_transfer_task())
