import sys
import os
import asyncio

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

# Load API key
config = load_config()
openai_key = config.openai_key

# LangChain setup
chat_model = ChatOpenAI(model="gpt-4.1-nano")

try:
    result = chat_model.generate(
        messages = [[
            SystemMessage(content="You are a poetic assistant."), 
            HumanMessage(content="Compose a haiku about the moon.") 
        ]]
    )

    # Inspect the structure
    print("---LLM Result ----")
    print(result)

    print("\n--- First Generation ---")
    first_generation = result.generations[0][0]
    print(first_generation)

    print("\n--- Generation's Message ---") 
    ai_message = first_generation.message 
    print(ai_message) 
    print("Content:", ai_message.content)

    print("\n--- Generation Info ---") 
    print(first_generation.generation_info) 

    print("\n--- Aggregated Token Usage ---") 
    print(result.llm_output['token_usage']) 



except Exception as e:
    print(f"An error occurred:{e}")