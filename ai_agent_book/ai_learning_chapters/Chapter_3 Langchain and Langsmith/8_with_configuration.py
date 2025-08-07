import sys
import os
import asyncio

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API key
config = load_config()
openai_key = config.openai_key

# LangChain setup
chat_model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.5)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template(
    "Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner."
)

# Define the output parser
str_parser = StrOutputParser()

# Construct the chain
explanation_chain = prompt_template | chat_model | str_parser

# apply configured
configured_explanation_chain = explanation_chain.with_config(
    tags=["explanation_module", "v1.0"],
    metadata={"source_script": "section_3_1_2_example.py"}
)

# Invoke Config chained
result_with_config = configured_explanation_chain.invoke(
    {"user_topic": "dark matter"},
    config={"metadata": {"invocation_specific": True, "user_id": "test_user_001"}}
)

print(f"Result (check LangSmith for tags/metadata): {result_with_config}") 