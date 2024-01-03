from datetime import datetime

import pytest

from scifeed.providers import Crawler, PapersWithCode


class CrawlerMock(Crawler):
    async def open(self, *args, **kwargs):
        return open("tests/static/paperswithcode.html").read()


@pytest.mark.asyncio()
async def test_paperswithcode_fetch():
    pm = PapersWithCode(CrawlerMock())
    items = await pm.fetch("test")
    assert len(items) == 2
    assert (
        items[0].url
        == "https://paperswithcode.com/paper/characterizing-physiological-and-symptomatic"
    )
    assert items[0].title == "Characterizing physiological and symptomatic variation"
    assert items[0].published == datetime(2020, 5, 14, 0, 0)
