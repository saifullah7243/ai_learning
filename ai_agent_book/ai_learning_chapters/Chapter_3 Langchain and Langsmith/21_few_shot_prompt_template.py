from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate

# Define few-shot examples
examples = [
    {
        "input": "A happy sentence.",
        "output": "The sun is shining and the birds are singing."
    },
    {
        "input": "A sad sentence.",
        "output": "The rain fell gently on the empty streets."
    }
]

# Create a prompt for a single example
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

# Create the few-shot template
few_shot_template = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt
)

# Final chat prompt with system message, few-shot examples, and user input
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a master of writing sentences with a specific mood. Emulate the user's examples."),
    few_shot_template,
    ("human", "{input}")
])

# Format the prompt with a new user input
formatted_chat_prompt = final_prompt.format_messages(input="An excited sentence.")

# Output the result
print(formatted_chat_prompt)
