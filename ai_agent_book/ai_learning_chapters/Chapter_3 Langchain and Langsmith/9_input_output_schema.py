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

# Output parser
str_parser = StrOutputParser()

explanation_chain = prompt_template | chat_model | str_parser


print("\n --- Schema Insepction----")
# print("Prompt Template Input Schema:", prompt_template.input_schema.model_json_schema())

print("Prompt Template Output Schema:", prompt_template.output_schema.model_json_schema())


# print("Chat Model Input Schema: ", chat_model.input_schema.model_json_schema())

# print("Chat Model Output Schema:", chat_model.output_schema.model_json_schema())

# print("String Parser Output Schema: ", str_parser.input_schema.model_json_schema())

# print("String Parser Output Schema:", str_parser.output_schema.model_json_schema()) # Will be str 

# print("Explanation Chain Input Schema:", explanation_chain.input_schema.model_json_schema()) 
# # # This will be the input schema of the first element (the RunnablePassthrough or prompt_template) 
# print("Explanation Chain Output Schema:", explanation_chain.output_schema.model_json_schema()) 
