import json
from openai import OpenAI
from config import openai_key

# Step 1: Initialize OpenAI client
client = OpenAI(api_key=openai_key)

# Step 2: Define the tool/function schema
function_defs = [
    {
        "name": "add_numbers",
        "description": "Add two numbers and return the result.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    }
]

# Step 3: User message
messages = [
    {"role": "user", "content": "What is 256 + 144? Just give me the number."}
]

# Step 4: First call to model — may trigger function call
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    functions=function_defs,
    function_call="auto"  # Let the model decide
)

# Step 5: Check model’s response
assistant_msg = response.choices[0].message

# Step 6: If model chose to call a function
if assistant_msg.function_call:
    print("\n Tool was called by the model!")

    func_name = assistant_msg.function_call.name
    args = json.loads(assistant_msg.function_call.arguments)

    print("Function Name:", func_name)
    print("Arguments:", args)

    # Step 7: Execute the tool logic (here, adding the numbers)
    if func_name == "add_numbers":
        result_value = args["a"] + args["b"]

        # Step 8: Append function call and result to conversation
        messages.append(assistant_msg)  # function call message
        messages.append({
            "role": "function",
            "name": func_name,
            "content": json.dumps({"result": result_value})
        })

        # Step 9: Ask model to give final answer using result
        follow_up = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages
        )

        final_answer = follow_up.choices[0].message.content
        print("\nAssistant Final Answer:", final_answer)

else:
    print("\nModel replied directly without tool call:")
    print(assistant_msg.content)
