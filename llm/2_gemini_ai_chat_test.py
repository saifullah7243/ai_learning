# # Step-1 -> import libraries that required
# import google.generativeai as genai
# from config import google_key  

# # Step -2 -> Set which LLM api key want to use
# genai.configure(api_key=google_key)

# # Step - 3 Input -> Initialize the model and define the prompt
# model = genai.GenerativeModel("gemini-2.5-flash")
# prompt = "What is gen ai"

# # Step - 4 Output -> Generate response and print the output
# response = model.generate_content(prompt)
# print("Gemini model reply:", response.text)
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)


