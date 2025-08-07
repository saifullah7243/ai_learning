import json
from pathlib import Path
from typing import List, Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict, HumanMessage, AIMessage


class FileChatMessageHistory(BaseChatMessageHistory):
    """Custom chat history stored in a JSON file"""

    def __init__(self, session_id: str, file_path: str = "chat_session"):
        self.session_id = session_id
        self.file_path = Path(file_path) / f"{session_id}.json"
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def messages(self) -> List[BaseMessage]:
        """Retrieve Messages from file"""
        if not self.file_path.exists():
            return []
        with self.file_path.open("r") as f:
            return messages_from_dict(json.load(f))

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """Append messages to the file"""
        stored_messages = self.messages
        all_messages = messages_to_dict(stored_messages + list(messages))
        with self.file_path.open("w") as f:
            json.dump(all_messages, f, indent=2)

    def clear(self) -> None:
        """Clear session history."""
        if self.file_path.exists():
            self.file_path.unlink()

# --- Usage ---
custom_history = FileChatMessageHistory(session_id="custom_session_1")
custom_history.add_user_message("This is a test of custom file history.")
custom_history.add_ai_message("I see your test, and it is stored.")
print(custom_history.messages)
