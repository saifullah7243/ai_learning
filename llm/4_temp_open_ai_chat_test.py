### Temperature 0.0 to 1.0 with defualt top_p
# Step-1 -> import libraries that required
# from openai import OpenAI
# from config import openai_key

# # Step -2 -> Set which LLM api key want to use
# client = OpenAI(api_key=openai_key)

# # Step - 3 Input -> Send request to model
# prompt = "Give one creative analogy to explain the concept of artificial intelligence."

# for temp in [0.0, 1.0]:
#     response = client.chat.completions.create(
#         model="gpt-4.1-nano",  # Replace with "gpt-4.1-nano" only if you're sure it's available to your account
#         messages=[{"role": "user", "content": prompt}],
#         temperature=temp,
#         max_tokens=50
#     )
#     # ✅ Use .content not ['content']
#     message = response.choices[0].message
#     print(f"\nTemperature {temp}: {message.content}")

# <--------------------------------------------------------------------------------------->

# Step-1 -> import libraries that required
from openai import OpenAI
from config import openai_key

# Step-2 -> Set which LLM api key want to use
client = OpenAI(api_key=openai_key)

# Step-3 -> Define your prompt
prompt = "Tell me a short story about a robot learning to feel emotions."

# Step-4 -> Experiment with different temperatures
print("=== Experiment: Changing Temperature (top_p = 1.0 fixed) ===")
for temp in [0.0, 0.7, 1.0]:
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        top_p=1.0,
        max_tokens=100
    )
    print(f"\nTemperature {temp}:\n{response.choices[0].message.content}")

# Step-5 -> Experiment with different top_p values while keeping temperature fixed
print("\n=== Experiment: Changing top_p (temperature = 0.7 fixed) ===")
for top_p_val in [0.5, 1.0]:
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        top_p=top_p_val,
        max_tokens=100
    )
    print(f"\ntop_p = {top_p_val}:\n{response.choices[0].message.content}")
