# Step 1: Import required libraries
from openai import OpenAI
from config import openai_key, openweather_key
import requests
import json
from datetime import date

# Step 2: Initialize OpenAI client
client = OpenAI(api_key=openai_key)

# Step 3: Define function schema
function_def = {
    "name": "get_weather",
    "description": "Get the weather forecast for a given city and day",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"},
            "date": {"type": "string", "description": "Date in YYYY-MM-DD"}
        },
        "required": ["location", "date"]
    }
}

# Step 4: Create user message
messages = [
    {"role": "user", "content": "What's the weather in Tokyo today?"}
]

# Step 5: Call the model (let it decide if it wants to call a function)
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    functions=[function_def],
    function_call="auto"
)

# Step 6: Check if model triggered function call
response_msg = response.choices[0].message

if response_msg.function_call:
    print("\n✅ Model triggered function call")
    
    func_name = response_msg.function_call.name
    args_json = response_msg.function_call.arguments
    args = json.loads(args_json)

    print("Function Name:", func_name)
    print("Arguments:", args)

    # Step 7: Real OpenWeatherMap API call
    def call_openweather_api(city, forecast_date):
        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={openweather_key}&units=metric"
            )
            res = requests.get(url)
            data = res.json()

            if res.status_code != 200 or "main" not in data:
                return {"error": data.get("message", "Failed to get weather.")}

            return {
                "location": city,
                "date": forecast_date,
                "forecast": (
                    f"{data['weather'][0]['description'].capitalize()}, "
                    f"{data['main']['temp']}°C "
                    f"(min: {data['main']['temp_min']}°C, max: {data['main']['temp_max']}°C)"
                )
            }
        except Exception as e:
            return {"error": str(e)}

    # Step 8: Get result from real API
    result = call_openweather_api(args["location"], args["date"])
    print("\n🌦️ Weather API result:", result)

    # Step 9: Pass the result back to the model
    messages.append({
        "role": "function",
        "name": func_name,
        "content": json.dumps(result)
    })

    # Step 10: Ask model to produce final natural reply
    follow_up = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages
    )

    final_reply = follow_up.choices[0].message.content
    print("\n🤖 Assistant Final Answer:\n", final_reply)

else:
    print("\n🤖 No function call. Model answered directly:")
    print(response_msg.content)
