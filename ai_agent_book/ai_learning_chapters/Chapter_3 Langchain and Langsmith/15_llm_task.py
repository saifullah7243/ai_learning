import sys
import os
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

# Check for key and proceed
if not openai_key:
    print("OPENAI_API_KEY not found. Please set it in your .env file.")
else:
    creative_model = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=1.2,
        max_tokens=1024
    )

    factual_model = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0.1,
        max_tokens=1024
    )

    message = HumanMessage(content = "Write a single sentence describing a cat.")

    for i in range(1,4):
        print(f"\n--- Round {i} ---")
        
        creative_response = creative_model.invoke([message])
        factual_response = factual_model.invoke([message])

        print(f"Creative Model Response: {creative_response.content}")
        print(f"Factual Model Response: {factual_response.content}")
        