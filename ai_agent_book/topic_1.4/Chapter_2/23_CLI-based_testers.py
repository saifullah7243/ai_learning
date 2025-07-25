import sys
import os
import asyncio
from typing import List, Dict, Any
import json
import time
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

### -- Placeholder for loading prompts and test cases
def load_prompt_variants(filepath="prompt_variants.json"):
    """Load prompt variants from a JSON file"""
    try:
        with open(filepath,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Prompt variants file {filepath} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Error:Could not decode JSON from {filepath}")
        return {}
    
def load_test_cases(filepath = "test_cases.json"):
    """Load test cases from a JSON file(list of strings or diict)"""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Test cases file {filepath} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return {}

async def run_experiment(prompt_variant_name, system_prompt, user_prompt_template, test_case, temperature, model_name="gpt-4.1-nano"):
    """
    Runs a single experiement for one prompt variant and one test case.
    """
    if isinstance(test_case, dict):
        #  If test_case is a dict, assume user_prompt_template can use its keys for formatting 
        try:
            user_prompt = user_prompt_template.format(**test_case)
        except KeyError as e:
            print(f"Error missing Key{e} in test_case for prompt formatting. Test case:{test_case}")
            return None
        
        # Assume test_case is a string and user_prompt_template uses a generic placeholder
    else:
        user_prompt = user_prompt_template.format(input=test_case)
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    start_time = time.perf_counter()
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature
        )
        latency = time.perf_counter() - start_time
        llm_response = response.choices[0].message.content
        usage = response.usage

        result = {
            "prompt_variant_name": prompt_variant_name, 
            "system_prompt": system_prompt, 
            "user_prompt": user_prompt, # Log the formatted user prompt 
            "test_case_input": test_case, 
            "temperature": temperature, 
            "model_name": model_name, 
            "llm_response": llm_response, 
            "latency_seconds": round(latency, 4), 
            "prompt_tokens": usage.prompt_tokens if usage else None, 
            "completion_tokens": usage.completion_tokens if usage else None, 
            "total_tokens": usage.total_tokens if usage else None, 
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S") 
        }

        return result
    except Exception as e:
        print(f"Error during API call for{prompt_variant_name} with test case {test_case}: {e}")
        latency = time.perf_counter() - start_time
        return{
           "prompt_variant_name": prompt_variant_name, 
            "system_prompt": system_prompt, 
            "user_prompt": user_prompt, 
            "test_case_input": test_case, 
            "temperature": temperature, 
            "model_name": model_name, 
            "llm_response": f"ERROR: {e}", 
            "latency_seconds": round(latency, 4), 
            "prompt_tokens": None, 
            "completion_tokens": None, 
            "total_tokens": None, 
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")  
        }

async def main_batch_runner():
    prompt_variants = load_prompt_variants()  # Expects a dict: {"variant_name": {"system": "...", "user_template": "..."}} 
    test_cases = load_test_cases()  # Expects a list of inputs, e.g., ["input1", "input2"] or [{"query": "q1", "context": "c1"}] 

    if not prompt_variants or not test_cases:
        print("Exiting due to missing prompts or test cases")
        return
    
    all_results = []
    temperatures_to_test = [0.2, 0.7] 
    for variant_name, prompt_data in prompt_variants.items():
        system_p = prompt_data.get("system","")
        user_p_template = prompt_data.get("user_template",{input})

        for test_case in test_cases:
            for temp in temperatures_to_test:
                print(f"Running: {variant_name} - Test Case: {str(test_case)[:50]}...' Temp:{temp}")
                result = await run_experiment(variant_name, system_p, user_p_template, test_case, temp)

                if result:
                    all_results.append(result)
                    # simple console log of the result
                    print(f" LLM Output:{str(result['llm_response'])[:100]}")
                    print(f" Latency:{result['latency_seconds']:.2f}s, Tokens: {result['total_tokens']}")

    output_file = "experiment_results.jsonl"
    with open(output_file, 'w') as f: 
        for res in all_results: 
            f.write(json.dumps(res) + "\n") 
    print(f"\nAll experiments complete. Results saved to {output_file}")


if __name__ == "__main__": 
    # Create dummy files for the script to run 
    # 1. prompt_variants.json 
    dummy_prompts = { 
        "variant_A_formal": { 
            "system": "You are a formal summarizer.", 
            "user_template": "Please formally summarize the following text: {input}" 
        }, 
        "variant_B_bullet": { 
            "system": "You are a concise summarizer that uses bullet points.", 
            "user_template": "Summarize this text using bullet points: {input}" 
        } 
    } 
    with open("prompt_variants.json", "w") as f: 
        json.dump(dummy_prompts, f, indent=2) 
 
    # 2. test_cases.json 
    dummy_test_cases = [ 
        "The quick brown fox jumps over the lazy dog. This sentence is famous for containing all letters of the English alphabet.", 
        "Large language models are transforming various industries by automating tasks, generating creative content, and providing insights from data." 
    ] 
    with open("test_cases.json", "w") as f: 
        json.dump(dummy_test_cases, f, indent=2) 
 
    asyncio.run(main_batch_runner())
                
    