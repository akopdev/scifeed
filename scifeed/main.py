from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from scifeed.schemas import Feed

from .providers import GoogleScholar

app = FastAPI()

templates = Jinja2Templates(directory="scifeed/templates")

scholar = GoogleScholar()


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def preview(request: Request):
    results = []
    form = await request.form()
    query = form.get("query")
    if query:
        results = await scholar.fetch_all(query)
    return templates.TemplateResponse(
        "preview.html", {"request": request, "query": query, "results": results}
    )


@app.get("/scholar")
async def get_scholar(q: str, limit: int = 50):
    items = await scholar.fetch_all(q, limit=limit)
    return Feed(title=f"Google Scholar | {q}", items=items)
