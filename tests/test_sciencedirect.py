import pytest

from scifeed.providers import Crawler, ScienceDirect


class CrawlerMock(Crawler):
    async def open(self, *args, **kwargs):
        return open("tests/static/sciencedirect.html").read()


@pytest.mark.asyncio()
async def test_sciencedirect_fetch():
    rg = ScienceDirect(CrawlerMock())
    items = await rg.fetch("test")
    assert len(items) == 25
    assert "Identification and validation of M2 macrophage-related genes" in items[0].title
    assert "https://www.sciencedirect.com/science/article/pii/S2405844023094665" in items[0].url
    assert "Hongyan Ding" in items[0].authors
