# import time
# from openai import OpenAI
# from config import openai_key
# from openai._exceptions import RateLimitError, APIError, Timeout

# client = OpenAI(api_key=openai_key)

# def query_gpt(messages, max_retries=3):
#     for attempt in range(max_retries):
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4.1-nano",
#                 messages=messages,
#                 timeout=15
#             )
#             return response 
        
#         except RateLimitError:
#             wait = 2 ** attempt
#             print(f"Rate limit hit, retrying in {wait} seconds...")
#             time.sleep(wait)
#             continue

#         except Timeout as e: 
#             print("Request timed out. Retrying...") 
#             continue 
#         except APIError as e: 
#             # If it's a server error (500) or similar, maybe retry, or break depending on e.http_status 
#             if e.http_status != 500: 
#                 raise  # for non-retryable errors, re-raise 
#             print("Server error, retrying...") 
#             continue 
#     raise Exception("Failed to get completion after multiple retries.") 

import time
from openai import OpenAI
from config import openai_key
from openai._exceptions import RateLimitError, APIError, APIConnectionError

client = OpenAI(api_key=openai_key)

def query_gpt(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages,
                timeout=15
            )
            return response 
        
        except RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limit hit, retrying in {wait} seconds...")
            time.sleep(wait)
            continue

        except APIConnectionError:
            print("Connection timed out. Retrying...")
            continue

        except APIError as e: 
            if e.http_status != 500: 
                raise  # For non-retryable errors, re-raise
            print("Server error, retrying...")
            continue

    raise Exception("Failed to get completion after multiple retries.")
if __name__ == "__main__":
    messages = [{"role": "user", "content": "Hello!"}]
    response = query_gpt(messages)
    print("✅ Response:", response.choices[0].message.content)