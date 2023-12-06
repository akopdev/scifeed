import asyncio
import itertools
from enum import Enum
from os import path
from typing import Annotated, List

from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates

from .providers import Providers
from .schemas import Feed, Item

app = FastAPI()

templates = Jinja2Templates(directory=path.join(path.dirname(__file__), "templates"))

Provider = Enum(
    "Provider",
    [(id, id) for id in Providers.keys()],
)


async def fetch(query: str, limit: int = 50, providers: List[Provider] = []) -> List[Item]:
    if not providers:
        return []
    tasks = [Providers[provider.value].fetch_all(query, limit=limit) for provider in providers]
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
    query = form.get("query")
    providers = form.getlist("provider") or list(Providers.keys())
    if query:
        results = await fetch(query, providers=[Provider(provider) for provider in providers])
    return templates.TemplateResponse(
        "preview.html",
        {
            "request": request,
            "query": query,
            "providers": providers,
            "all_providers": Providers,
            "results": results,
        },
    )


@app.get("/feed")
async def feed(
    q: Annotated[str, Query(max_length=100)],
    providers: Annotated[List[Provider], Query()] = [],
    limit: Annotated[int, Query(lt=200)] = 50,
) -> Feed:
    return Feed(
        title=f"SciFeed | {q}",
        items=await fetch(q, limit=limit, providers=providers),
    )
