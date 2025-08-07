from langchain_community.chat_message_histories import RedisChatMessageHistory, SQLChatMessageHistory

# Redis message history
redis_history = RedisChatMessageHistory(
    session_id="user_123_conversation_456",
    url="redis://localhost:6379/0"
)

# SQL message history using SQLite
sql_history = SQLChatMessageHistory(
    session_id="user_xyz_thread_abc",
    connection_string="sqlite:///chat_history.db"
)

# Add messages to SQL history
sql_history.add_user_message("Hello from SQL!")
sql_history.add_ai_message("Hello! Your message is saved.")

# Retrieve messages
print(sql_history.messages)
