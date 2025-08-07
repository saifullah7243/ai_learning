# Step-1 -> import libraries that required
from openai import OpenAI
from config import openai_key

# Step -2 -> Set which LLM api key want to use
client = OpenAI(api_key=openai_key)

# Step - 3 Input -> Send request to model
user_query = "Weather in Tokyo tomorrow"
prompt = f"""
 You are a weather bot. Provide a JSON with the weather forecast. 
 The JSON should have two keys: "location" and "forecast". 
 Query: "{user_query}
"""
response = client.chat.completions.create(
    model = "gpt-4.1-nano",
    messages = [{"role":"user", "content":prompt}],
    max_tokens = 50,
    temperature = 0.7
)
print("Response from Model : ", response)
# Step - 4 Output
answer = response.choices[0].message.content
print("GPT Model Reply:", answer)