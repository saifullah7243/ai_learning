# Step-1 -> import libraries that required
from openai import OpenAI
from Config.config import openai_key

# Step -2 -> Set which LLM api key want to use
client = OpenAI(api_key=openai_key)

# Step - 3 Input -> Send request to model
function_def = {
    "name": "get_weather",
    "description": "Get the weather forecast for a given city and day",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"},
            "date": {"type": "string", "description": "Date (YYYY-MM-DD)"}
        },
        "required": ["location", "date"]
    }
}

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[{"role": "user", "content": "What is Tokyo weather today?"}],
    max_tokens=50,
    temperature=0.7,
    functions=[function_def],
    function_call="auto"
)

# Step - 4 Output
message = response.choices[0].message
# print(message.content)


if message.function_call:
    print("\n Model chose to call a function:")
    print("Function name:", message.function_call.name)
    print("Arguments:", message.function_call.arguments)
else:
    print("\nGPT Model Reply:", message.content)
