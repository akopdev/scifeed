from typing import List, Optional

from pydantic import BaseModel


class Item(BaseModel):
    title: str
    id: str
    url: str
    description: Optional[str] = ""


class Feed(BaseModel):
    title: Optional[str] = "SciFeed"
    description: Optional[str] = None
    version: str = "https://jsonfeed.org/version/1.1"
    items: List[Item] = []
