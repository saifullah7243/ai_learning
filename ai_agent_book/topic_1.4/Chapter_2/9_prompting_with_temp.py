# import sys
# import os
# import asyncio
# from typing import List, Dict, Any
# import json

# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from rich.console import Console
# from rich.markdown import Markdown

# # Rich console setup
# console = Console()

# # Load environment variables from .env
# load_dotenv()

# # Go 3 levels up to reach the root path of ai_agent_course/
# root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# sys.path.append(root_path)

# # Now import from llm/config.py at root level
# try:
#     from llm.config import openai_key
# except ImportError:
#     console.print("[bold red]Error:[/bold red] Could not import `openai_key` from llm.config")
#     sys.exit(1)

# # Setup OpenAI async client
# client = AsyncOpenAI(api_key=openai_key)

# # Define the message format

# async def get_prompt_with_temp():
#     def count_words(text):
#             return len(text.split())

#     system_prompt_json = ("You are a fantasy storyteller with a vivid imagination")

#     user_prompt_product = "Describe a newly discovered creature called a 'Shadow Whisperer'. Focus on its appearance, habitat, and one unique ability. Keep it under 75 words."
#     try:
#         ## First Response --> Temprature is 0.2
#         console.rule("[bold cyan]When Temprature is 0.2")
#         response_1 = await client.chat.completions.create(
#             model="gpt-4.1-nano",
#             messages=[
#                 {"role": "system", "content": system_prompt_json},
#                 {"role": "user", "content": user_prompt_product}
#             ],
#             temperature=0.2
#         )
#         first_respponse = response_1.choices[0].message.content
#         console.print(Markdown((f"{first_respponse}\n Word in Paragragh: {count_words(first_respponse)}")))

#         ## Second Response --> Temprature is 0.7
#         console.rule("[bold cyan]When Temprature is 0.7")
#         response_2 = await client.chat.completions.create(
#             model="gpt-4.1-nano",
#             messages=[
#                 {"role": "system", "content": system_prompt_json},
#                 {"role": "user", "content": user_prompt_product}
#             ],
#             temperature=0.7
#         )
#         second_response = response_2.choices[0].message.content
#         console.print(Markdown(f"{second_response}\n Word in Paragragh: {count_words(second_response)}"))

#         ## Third Response --> Temprature is 1.2
#         console.rule("[bold cyan]When Temprature is 1.2")
#         response_3 = await client.chat.completions.create(
#             model="gpt-4.1-nano",
#             messages=[
#                 {"role": "system", "content": system_prompt_json},
#                 {"role": "user", "content": user_prompt_product}
#             ],
#             temperature=1.2
#         )
#         third_response = response_3.choices[0].message.content
#         console.print(Markdown((f"{third_response}\n Word in Paragragh: {count_words(third_response)}")))

#     except Exception as e:
#         print(f"\n An API Error Occured")

# async def main():
#     await get_prompt_with_temp()

# # Run the async function
# if __name__ == "__main__":
#     asyncio.run(main())


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
async def get_llm_response_with_temp(messages_list: list, temperature: float) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages_list,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"
    
async def temperature_experiment_task():
    system_prompt_story = (
        "You are a fantasy storyteller with a vivid imagination, known for your unique creature descriptions."
    )
    user_prompt_creature = (
        "Describe a newly discovered creature called a 'Shadow Whisperer'. "
        "Focus on its appearance, habitat, and one unique ability. Keep the description under 75 words."
    )

    messages = [
        {"role": "system", "content": system_prompt_story},
        {"role": "user", "content": user_prompt_creature},
    ]

    console.rule("[bold cyan] When--- Temperature Experiment Task ---")

    # Temperature = 0.2
    temp_low = 0.2
    print(f"\n--- Output with Temperature: {temp_low} ---")
    response_low_temp = await get_llm_response_with_temp(messages, temp_low)
    console.print(Markdown(response_low_temp))

    # Temperature = 0.7
    temp_medium = 0.7
    print(f"\n--- Output with Temperature: {temp_medium} ---")
    response_medium_temp = await get_llm_response_with_temp(messages, temp_medium)
    console.print(Markdown(response_medium_temp))

    # Temperature = 1.2
    temp_high = 1.2
    print(f"\n--- Output with Temperature: {temp_high} ---")
    response_high_temp = await get_llm_response_with_temp(messages, temp_high)
    console.print(Markdown(response_high_temp))

# Run the async function
if __name__ == "__main__":
    asyncio.run(temperature_experiment_task())
