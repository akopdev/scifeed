import asyncio
import itertools
from typing import List

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from scifeed.schemas import Feed, Item

from .providers import GoogleScholar, PubMed, Arxiv

app = FastAPI()

templates = Jinja2Templates(directory="scifeed/templates")

providers = {
    "scholar": GoogleScholar(),
    "pubmed": PubMed(),
    "arxiv": Arxiv(),
}


async def fetch(query: str, limit: int = 50) -> List[Item]:
    tasks = [provider.fetch_all(query, limit=limit) for name, provider in providers.items()]
    items = await asyncio.gather(*tasks)
    results = list(itertools.chain(*items))
    results.sort(key=lambda x: x.published, reverse=True)
    return results


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def preview(request: Request):
    results = []
    form = await request.form()
    if query := form.get("query"):
        results = await fetch(query)
    return templates.TemplateResponse(
        "preview.html", {"request": request, "query": query, "results": results}
    )


@app.get("/feed")
async def feed(q: str, limit: int = 50):
    return Feed(title=f"SciFeed | {q}", items=await fetch(q, limit=limit))
