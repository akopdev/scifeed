from fastapi import FastAPI

from .providers import GoogleScholar

app = FastAPI()


@app.get("/scholar")
async def scholar(q: str, limit: int = 50):
    return await GoogleScholar(q, limit).feed(q)
