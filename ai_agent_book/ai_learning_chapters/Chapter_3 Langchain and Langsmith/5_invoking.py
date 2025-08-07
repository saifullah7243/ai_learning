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
chat_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.1)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template( 
"Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner." 
) 

# Define the output parser
str_parser = StrOutputParser()

# Construct the chain
# Method_1
explanation_chain = prompt_template | chat_model | str_parser



### Single Invoke
topic_input = {"user_topic": "Tiktok"}
try: 
    sync_explanation = explanation_chain.invoke(topic_input)
    print(f"Single Invoke Result: {sync_explanation}")
except Exception as e:
    print(f"Error in Single Invoke (Ensure API Key is set): {e}")

# Synchronous batch invocation 
input_batches = [
    {"user_topic":"Machine Learning"},
    {"user_topic":"Batch Learning"},
    {"user_topic":"Online Learning"},
    {"user_topic":"Book Learning"}

] 

try:
    batch_invoke = explanation_chain.batch(input_batches)
    print("\nBatch Invok Resuult")
    for i, res in enumerate(batch_invoke): 
        print(f"Input: {input_batches[i]['user_topic']}, Output: {res[:50]}...") # Print first 50 chars

except Exception as e:
    print("Error in Batch: {e}")

# Batch invocation with error handling
inputs_with_potential_error = [
    {"user_topic": "reinforcement learning"},
    {"malformed_input_key": "this will likely cause an error in the prompt template"}
]

try:
    results_with_error_handling = explanation_chain.batch(
        inputs_with_potential_error,
        return_exceptions=True
    )
    print("\nBatch with Error Handling Results:")
    for res in results_with_error_handling:
        if isinstance(res, Exception):
            print(f"Encountered an error: {res}")
        else:
            print(f"Success: {res[:50]}...")
except Exception as e:
    # This top-level try-except might catch issues with batch setup itself
    print(f"Overall error in batch with error handling: {e}")

