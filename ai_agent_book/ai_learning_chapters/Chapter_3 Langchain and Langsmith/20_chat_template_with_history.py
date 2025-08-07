from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Define a chat template with a placeholder for history
chat_template_with_history = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer the user's questions."),
    # The 'history' placeholder will be filled with a list of Message objects
    MessagesPlaceholder(variable_name="history"),
    # The final user question
    ("human", "{user_input}")
])

# Simulate a conversation history
conversation_history = [
    HumanMessage(content="What is the capital of France?"),
    AIMessage(content="The capital of France is Paris.")
]

# Format the template, providing both the history and the new user input
final_messages = chat_template_with_history.format_messages(
    history=conversation_history,
    user_input="What is a famous landmark there?"
)

# Print the final prompt message objects
print(final_messages)
