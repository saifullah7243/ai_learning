from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
# System Message
system_instruction = SystemMessage(
    content = "You are helpfull assistant that translates English to French"
)

# User Message
user_request = HumanMessage(
    content = "I love AI"
)

# AI Messages
ai_examples_response = AIMessage(
    content = "J'adore l'IA"
)

# Tool Messages
tool_call_output = ToolMessage(
    content = "5",
    tool_call_id ="call_abc123"
)

conversation = [system_instruction, user_request, ai_examples_response, tool_call_output]

print (conversation)

