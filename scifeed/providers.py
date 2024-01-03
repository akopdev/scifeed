import asyncio
import itertools
import random
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Literal, Optional, Tuple

from parsel import Selector
from playwright.async_api import TimeoutError, async_playwright

from .schemas import Item


class Crawler:
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

    @property
    def started(self) -> bool:
        return self.browser is not None

    def __init__(self, browser=None):
        self.browser = browser

    async def start(self, engine: Literal["chromium", "firefox", "webkit"] = "chromium"):
        core = await async_playwright().start()
        browser = getattr(core, engine)
        self.browser = await browser.launch(headless=True, slow_mo=50)

    async def open(self, url: str) -> Optional[str]:
        if not self.started:
            return
        page = await self.browser.new_page(user_agent=random.choice(self._user_agents))
        try:
            await page.goto(url)
        except TimeoutError:
            print("Timeout error")
            await self.end()
            return
        return await page.content()

    async def end(self):
        await self.browser.close()
        self.browser = None


class DataProvider:
    _cache_timeout = 60

    size = 50

    def __init__(self, crawler: Optional[Crawler] = None):
        self._cache: Dict[str, Tuple[datetime, Dict[str, str]]] = {}
        self.crawler = crawler if isinstance(crawler, Crawler) else Crawler()

    def encode_query(self, query: str) -> str:
        return query.replace(" ", "").lower()

    async def get(self, url: str, params: Dict[str, Any]) -> str:
        """Get data from a URL with random user agent."""
        if not self.crawler.started:
            print("Starting crawler from scratch")
            await self.crawler.start()
        content = await self.crawler.open(
            url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        )
        return content

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        """Fetch results for a given query from a single page."""
        raise NotImplementedError

    async def fetch_all(self, query: str, start: int = 0, limit: int = 50) -> List[Dict[str, str]]:
        """Fetch all results for a given query from all pages."""
        key = self.encode_query(query)
        if cached := self._cache.get(key):
            if cached[0] >= datetime.utcnow():
                return cached[1]
        tasks = [self.fetch(query, page) for page in range(start, limit, self.size)]
        items = await asyncio.gather(*tasks)
        result = list(itertools.chain(*items))
        self._cache[key] = (
            datetime.utcnow() + timedelta(minutes=self._cache_timeout),
            result,
        )
        return result


class PubMed(DataProvider):
    name = "PubMed"
    url = "https://pubmed.ncbi.nlm.nih.gov"

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(
            self.url,
            {"term": query, "sort": "date", "size": self.size, "page": start // self.size + 1},
        )
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
        html = await self.get(
            self.url,
            {
                "query": query,
                "searchtype": "all",
                "source": "header",
                "start": start,
                "size": self.size,
                "order": "-submitted_date",
            },
        )
        result = []
        if html:
            headers = re.findall(
                r'<p class="list-title is-inline-block"><a href="(.+?)">.+?</a>.*?<p class="title is-5 mathjax">(.+?)</p>\s+<p class="authors">\s+<span class="(has-text-black-bis has-text-weight-semibold|search-hit)">Authors:</span>\s(.*?)</p>.*?<p class="is-size-7"><span class="has-text-black-bis has-text-weight-semibold">Submitted<\/span>.*?([a-zA-Z0-9, ]+);\s',  # noqa
                html,
                flags=re.S | re.DOTALL,
            )
            clean = re.compile("<.*?>")
            for header in headers:
                title = re.sub(clean, "", header[1])
                authors = re.sub(re.compile("\\s*<.*?>\\s*"), "", header[3])
                try:
                    result.append(
                        Item(
                            url=header[0],
                            id=header[0],
                            title=title.strip(),
                            provider=self.name,
                            authors=", ".join(authors.split(",")),
                            published=datetime.strptime(header[4].strip(), "%d %B, %Y"),
                        )
                    )
                except Exception as e:
                    print(str(e))
        return result


class PapersWithCode(DataProvider):
    name = "PapersWithCode"
    url = "https://paperswithcode.com/search"
    size = 10

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(
            self.url,
            {
                "q": query,
                "sort_by": "trending",
                "page": start // self.size + 1,
            },
        )
        result = []
        if html:
            headers = re.findall(
                r'<div class="row infinite-item item paper-card">.*?<h1><a href="(.+?)">(.+?)</a></h1>.*?<span class="author-name-text item-date-pub">(.+?)</span>',  # noqa
                html,
                flags=re.S | re.DOTALL,
            )
            clean = re.compile("<.*?>")
            for header in headers:
                title = re.sub(clean, "", header[1])
                try:
                    result.append(
                        Item(
                            url="https://paperswithcode.com" + header[0],
                            id=header[0],
                            title=title.strip(),
                            provider=self.name,
                            published=datetime.strptime(header[2].strip(), "%d %b %Y"),
                        )
                    )
                except Exception as e:
                    print(str(e))
        return result


class ResearchGate(DataProvider):
    name = "ResearchGate"
    url = "https://www.researchgate.net/search/publication"

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(
            self.url,
            {
                "q": query,
                "page": start // self.size + 1,
            },
        )
        result = []
        if html:
            selector = Selector(text=html)

            for item in selector.css(".nova-legacy-v-publication-item"):
                try:
                    print()
                    url = item.css(
                        ".nova-legacy-v-publication-item__stack-item a::attr(href)"
                    ).get()
                    result.append(
                        Item(
                            url=f"https://www.researchgate.net/{url}",
                            id=url,
                            title=item.css(
                                ".nova-legacy-v-publication-item__stack-item a::text"
                            ).get(),
                            provider=self.name,
                            published=datetime.strptime(
                                item.css(
                                    ".nova-legacy-v-publication-item__meta-data-item span::text"
                                ).get(),
                                "%b %Y",
                            ),
                            authors=", ".join(
                                item.css(
                                    ".nova-legacy-v-person-inline-item__fullname::text"
                                ).getall()
                            ),
                        )
                    )
                except Exception as e:
                    print(str(e))

        return result


class ScienceDirect(DataProvider):
    name = "ScienceDirect"
    url = "https://www.sciencedirect.com/search"

    async def fetch(self, query: str, start: int = 0) -> List[Item]:
        html = await self.get(
            self.url,
            {
                "qs": query,
                "offset": start * self.size,
            },
        )
        result = []
        if html:
            selector = Selector(text=html)
            clean = re.compile("<.*?>")
            for item in selector.css(".ResultItem"):
                try:
                    url = item.css(".result-list-title-link::attr(href)").get()
                    title = re.sub(
                        clean, "", item.css(".result-list-title-link .anchor-text").get()
                    )
                    result.append(
                        Item(
                            url=f"https://www.sciencedirect.com{url}",
                            id=url,
                            title=title,
                            provider=self.name,
                            # TODO: clean date before processing
                            # published=datetime.strptime(
                            #     str(item.css(".srctitle-date-fields span::text").getall()[1]),
                            #     "%d %B %Y",
                            # ),
                            authors=", ".join(item.css(".Authors .author::text").getall()),
                        )
                    )
                except Exception as e:
                    raise Exception(e)
                    print(str(e))

        return result
