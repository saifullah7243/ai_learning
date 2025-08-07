import sys
import os
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

## 1 import libraries
import asyncio
import time
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from langchain_core.callbacks import AsyncCallbackHandler 
from langchain_core.outputs import LLMResult 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI

## 2 Create the custome class
class ComprehensiveMonitorHandler(AsyncCallbackHandler):

    def __init__(self):
        self.start_times:Dict[UUID, float] = {}
        self.metrics = {
            "success":0,
            "errors":0,
            "total_tokens":0,
            "prompt_tokens":0,
            "completion_tokens":0,
            "total_latency":0.0
        }

    ## llm start
    async def on_llm_start(self, serialized, prompts, *, run_id, **kwargs):
        print(f"---- LLM Start ---- Run ID: {run_id}--------")
        print(f"Prompt:\n{prompts[0][:100]}....")
        self.start_times[run_id]= time.monotonic()

    ### llm end
    async def on_llm_end(self, response, *, run_id, **kwargs):
        latency = time.monotonic() - self.start_times.pop(run_id, 0)
        token_usage = response.llm_output.get("token_usage",{})
        prompt_tokens = token_usage.get("prompt_tokens",0)
        completion_tokens = token_usage.get("completion_tokens",0)
        total_tokens = token_usage.get("total_tokens",0)
        print(f"Latency: {latency:.2f}sec")
        print(f"Tokens: {total_tokens} (Prompt: {prompt_tokens}, Completion: {completion_tokens})")


        ## Update the metrics
        self.metrics["success"] += 1
        self.metrics["prompt_tokens"] += prompt_tokens
        self.metrics["completion_tokens"] += completion_tokens
        self.metrics["total_tokens"] += total_tokens
        self.metrics["total_latency"] += latency

    ## on_llm_error
    async def on_llm_error(self, error, *, run_id, **kwargs):
        print(f"--- LLM Error ---- Run ID: {run_id} --- ")
        print(f"Error: {error.__class__.__name__}:{error}")
        self.start_times.pop(run_id, None)
        self.metrics["errors"] += 1

    ## Print Summary:
    def print_summary(self):
        print("\n--- MONITORING SUMMARY ---")
        print(f"Total Runs: {self.metrics['success'] + self.metrics['errors']}")
        print(f"Successful Runs: {self.metrics['success']}")
        print(f"Failed Runs: {self.metrics['errors']}")

        if self.metrics['success'] > 0:
            avg_latency = self.metrics['total_latency'] / self.metrics['success']
            print(f"Average Latency: {avg_latency:.2f} seconds")
        print(f"Total Tokens Used: {self.metrics['total_tokens']}")
        print("______________________________")

async def main():
    monitor = ComprehensiveMonitorHandler()
    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    prompt = ChatPromptTemplate.from_template("What are the three main benefits of using {technology}?")
    chain = prompt | model
    await chain.ainvoke({"technology": "asynchronous programming"}, config={"callbacks": [monitor]})

    try:
        error_model = ChatOpenAI(model="gpt-non-existent-model")
        error_chain = prompt | error_model
        await error_chain.ainvoke({"technology": "rust"}, config={"callbacks": [monitor]})
    except Exception as e:
        print("An error occured:{e}")
    
    monitor.print_summary() 



if __name__ == "__main__": 
    asyncio.run(main())

