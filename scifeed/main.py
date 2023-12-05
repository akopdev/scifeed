import asyncio
import itertools
from os import path
from typing import List

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from .providers import Arxiv, GoogleScholar, PapersWithCode, PubMed
from .schemas import Feed, Item

app = FastAPI()

templates = Jinja2Templates(directory=path.join(path.dirname(__file__), "templates"))

data_providers = {
    "scholar": GoogleScholar(),
    "pubmed": PubMed(),
    "arxiv": Arxiv(),
    "paperswithcode": PapersWithCode(),
}


async def fetch(query: str, limit: int = 50, providers: List[str] = []) -> List[Item]:
    tasks = [data_providers[provider].fetch_all(query, limit=limit) for provider in providers]
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
    providers = form.getlist("provider") or list(data_providers.keys())
    if query := form.get("query"):
        results = await fetch(query, providers=providers)
    return templates.TemplateResponse(
        "preview.html",
        {"request": request, "query": query, "providers": providers, "results": results},
    )


@app.get("/feed")
async def feed(q: str, limit: int = 50):
    return Feed(title=f"SciFeed | {q}", items=await fetch(q, limit=limit))
