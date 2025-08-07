import sys
import os

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
chat_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template( 
"Create a short, catchy marketing slogan for a product called '{product_name}'" 
) 

# Define the output parser
str_parser = StrOutputParser()

# Method_2
explanation_chain_2 = (
    RunnablePassthrough()
    | prompt_template
    | chat_model
    | str_parser
)

### Try Asyn
import asyncio

async def get_async_explanation(topic_dict):
    return await explanation_chain_2.ainvoke(topic_dict)

async def main():
    print("\n--- Asynchronous Invocation ---")
    topic_input_async = {"product_name":"Cable Holder"}
    try:
        async_explanation = await get_async_explanation(topic_input_async)
        print(f"Async Explanation for '{topic_input_async['product_name']}':\n{async_explanation}")
    except Exception as e:
        print(f"Error during async invocation (ensure API key is set): {e}") 

if __name__ == "__main__":
    asyncio.run(main()) 

