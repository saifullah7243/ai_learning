# Step-1 -> import libraries that required
from openai import OpenAI, OpenAIError
from config import openai_key

# Step -2 -> Set which LLM api key want to use
client = OpenAI(api_key=openai_key)

# Step - 3 Input -> Send request to model
messages = [
    {"role": "system", "content": "You are a world-class travel assistant."},
    {"role": "system", "content": "I want to plan a one-week trip to Japan in April. What itinerary do you suggest?"}
]

try:
    response = client.chat.completions.create(
        model="gpt-4.1-nano", 
        messages=messages,
        max_tokens=300,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

except client.error.OpenAIError as e:
    print(f"API call failed: {e}")
    raise

# Step - 4 Output
assistant_message = response.choices[0].message.content
print("Assistant message Reply:\n", assistant_message)

# Token Usage Logging
usage = response.usage
print(f"\n[Usage] prompt_tokens={usage.prompt_tokens}, completion_tokens={usage.completion_tokens}, total={usage.total_tokens}")
