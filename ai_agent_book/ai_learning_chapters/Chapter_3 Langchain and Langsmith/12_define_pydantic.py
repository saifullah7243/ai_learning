from pydantic import BaseModel, Field
from typing import Optional, List

## Define schema:
class UserProfile(BaseModel):
    user_name: str = Field(description="The user's unique username.")
    user_id: int = Field(description="The user's integer ID")
    email: Optional[str] = Field(None, description="The user's Optional email address")
    interests: List[str] = Field(description="A list of the user's interest")

try:
    user = UserProfile(
        user_name="john_doe", 
        user_id=123,
        email="123@gmail.com",
        interests=["AI", "Python", "hiking"]
    )

    print("Successfully created UserProfile instance:")
    print(user.model_dump_json(indent=2))
except Exception as e:
    print(f"\nCaught validation error as expected: {e}")
