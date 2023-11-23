import asyncio
import itertools
import random
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

import aiohttp

from .schemas import Item


class DataProvider:
    _user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",  # noqa
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",  # noqa
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",  # noqa
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",  # noqa
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",  # noqa
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",  # noqa
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",  # noqa
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",  # noqa
    ]

    _cache_timeout = 60

    def __init__(self):
        self._cache: Dict[str, Tuple[datetime, Dict[str, str]]] = {}

    def encode_query(self, query: str) -> str:
        return query.replace(" ", "").lower()

    async def get(self, url: str, params: Dict[str, Any]) -> str:
        """Get data from a URL with random user agent."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"User-Agent": random.choice(self._user_agents)},
                params=params,
            ) as resp:
                if resp.status == 200:
                    return await resp.text()

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        """Fetch results for a given query from a single page."""
        raise NotImplementedError

    async def fetch_all(self, query: str, start: int = 0, limit: int = 50) -> List[Dict[str, str]]:
        """Fetch all results for a given query from all pages."""
        key = self.encode_query(query)
        if cached := self._cache.get(key):
            if cached[0] >= datetime.utcnow():
                return cached[1]
        tasks = [self.fetch(query, page) for page in range(start, limit, 10)]
        items = await asyncio.gather(*tasks)
        result = list(itertools.chain(*items))
        self._cache[key] = (
            datetime.utcnow() + timedelta(minutes=self._cache_timeout),
            result,
        )
        return result


class GoogleScholar(DataProvider):
    name = "Google Scholar"
    url = "https://scholar.google.com"

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(
            self.url,
            {"start": start, "hl": "en", "as_sdt": "0,5", "q": query, "scisbd": 1},
        )
        result = []
        if html:
            headers = re.findall(
                r'<h3 class="gs_rt".*?><a id=".*?" href="(.*?)" .*?>(.*?)</a>.*?</h3>',
                html,
            )
            clean = re.compile("<.*?>")
            for header in headers:
                title = re.sub(clean, "", header[1])
                result.append(Item(url=header[0], id=header[0], title=title, provider=self.name))
        return result


class PubMed(DataProvider):
    name = "PubMed"
    url = "https://pubmed.ncbi.nlm.nih.gov"

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(self.url, {"term": query, "sort": "date"})
        result = []
        if html:
            headers = re.findall(
                r'<a\s+class="docsum-title"\s+href="([^"]*)".*?>(.*?)<\/a>.*?<span class="docsum-authors full-authors">(.*?)</span>.*?(\d{4}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}).*?</span>',  # noqa
                html,
                flags=re.S | re.DOTALL,
            )
            clean = re.compile("<.*?>")
            for header in headers:
                title = re.sub(clean, "", header[1])
                try:
                    result.append(
                        Item(
                            url=self.url + header[0],
                            id=header[0],
                            title=title.strip(),
                            provider=self.name,
                            authors=header[2].strip(),
                            published=datetime.strptime(header[3], "%Y %b %d"),
                        )
                    )
                except Exception as e:
                    print(e)
        return result


class Arxiv(DataProvider):
    name = "Arxiv"
    url = "https://arxiv.org/search/"

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(self.url, {"query": query, "searchtype": "all", "source": "header"})
        result = []
        if html:
            headers = re.findall(
                r'<p class="list-title is-inline-block"><a href="(.+?)">.+?</a>.*?<p class="title is-5 mathjax">(.*?)</p>\s+<p class="authors">\s+<span class="has-text-black-bis has-text-weight-semibold">Authors:</span>\s(.*?)</p>.*?<p class="is-size-7"><span class="has-text-black-bis has-text-weight-semibold">Submitted<\/span>.*?([a-zA-Z0-9, ]+);\s',
                html,
                flags=re.S | re.DOTALL,
            )
            clean = re.compile("<.*?>")
            for header in headers:
                title = re.sub(clean, "", header[1])
                authors = re.sub(clean, "", header[2])
                try:
                    result.append(
                        Item(
                            url=header[0],
                            id=header[0],
                            title=title.strip(),
                            provider=self.name,
                            authors=", ".join(authors.split(",")),
                            published=datetime.strptime(header[3].strip(), "%d %B, %Y"),
                        )
                    )
                except Exception as e:
                    print(str(e))
        return result
