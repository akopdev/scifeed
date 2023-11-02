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
            if cached[0] >= (datetime.utcnow() - timedelta(minutes=self._cache_timeout)):
                return cached[1]
        tasks = [self.fetch(query, page) for page in range(start, limit, 10)]
        items = await asyncio.gather(*tasks)
        result = list(itertools.chain(*items))
        self._cache[key] = (
            datetime.utcnow(),
            result,
        )
        return result


class GoogleScholar(DataProvider):
    name = "Google Scholar"

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(
            "https://scholar.google.com/scholar",
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
                r'<div class="docsum-content">.+?<a.+? class="docsum-title".+?href="(.+?)".+?>(.+?)</a>',  # noqa
                html,
                flags=re.S | re.DOTALL,
            )
            clean = re.compile("<.*?>")
            for header in headers:
                title = re.sub(clean, "", header[1])
                result.append(
                    Item(
                        url=self.url + header[0],
                        id=header[0],
                        title=title.strip(),
                        provider=self.name,
                    )
                )
        return result
