from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: Optional[datetime] = None
