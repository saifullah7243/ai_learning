from langchain.memory import ConversationBufferWindowMemory

window_memory = ConversationBufferWindowMemory(memory_key = "history", k=3, return_messages = True)

window_memory.save_context(
    {"input":"Hi, I am bob"},
    {"output":"Hello Bob! how can i help you today?"}
)
window_memory.save_context( 
    {"input": "What's my name?"}, 
    {"output": "Your name is Bob."} 
)

## And "load" it for the next prompt. 
memory_variables = window_memory.load_memory_variables({}) 
print(memory_variables) 


