from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

summarizer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

summary_buffer_memory = ConversationSummaryBufferMemory(
    llm=summarizer_llm,
    max_token_limit=1000,
    memory_key="history",
    return_messages=True
)
