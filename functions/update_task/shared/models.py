from pydantic import BaseModel, Field
from typing import Optional

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool
