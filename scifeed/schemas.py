from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    title: str
    id: str
    url: str
    description: Optional[str] = ""
    provider: Optional[str] = None
    published: Optional[datetime] = Field(default_factory=datetime.utcnow)
    authors: Optional[str] = None


class Feed(BaseModel):
    title: Optional[str] = "SciFeed"
    description: Optional[str] = None
    version: str = "https://jsonfeed.org/version/1.1"
    items: List[Item] = []
