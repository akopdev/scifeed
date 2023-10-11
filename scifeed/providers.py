import asyncio
import itertools
import random
import re
from typing import Any, Dict, List

import aiohttp

from .schemas import Feed, Item


class DataProvider:
    _limit = 50
    _title = "SciFeed"
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

    async def get(self, url: str, params: Dict[str, Any]) -> str:
        """
        Wrapper around aiohttp to get data from a URL with random user agent.

        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"User-Agent": random.choice(self._user_agents)},
                params=params,
            ) as resp:
                assert resp.status == 200
                return await resp.text()

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        """Fetch results for a given query from a single page."""
        raise NotImplementedError

    async def fetch_all(self, query: str, start: int = 0) -> List[Dict[str, str]]:
        """Fetch all results for a given query from all pages."""
        tasks = [self.fetch(query, page) for page in range(0, self._limit, 10)]
        items = await asyncio.gather(*tasks)
        return list(itertools.chain(*items))

    async def feed(self, query: str) -> Feed:
        """Format results as RSS feed."""
        data = await self.fetch_all(query)
        return Feed(title=self._title, items=data)


class GoogleScholar(DataProvider):
    def __init__(self, name: str = "", limit: int = 50):
        self._limit = limit
        if name:
            self._title = " | ".join([name, "Google Scholar"])

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(
            "https://scholar.google.com/scholar",
            {"start": start, "hl": "en", "as_sdt": "0,5", "q": query, "scisbd": 1},
        )
        headers = re.findall(
            r'<h3 class="gs_rt".*?><a id=".*?" href="(.*?)" .*?>(.*?)</a>.*?</h3>', html
        )
        result = []
        clean = re.compile("<.*?>")
        for header in headers:
            title = re.sub(clean, "", header[1])
            result.append(Item(url=header[0], id=header[0], title=title))
        return result
