from datetime import datetime

import pytest

from scifeed.providers import Crawler, PubMed


class CrawlerMock(Crawler):
    async def open(self, *args, **kwargs):
        return open("tests/static/pubmed.html").read()


@pytest.mark.asyncio()
async def test_pubmed_fetch():
    pm = PubMed(CrawlerMock())
    items = await pm.fetch("test")
    assert len(items) == 2
    assert "Living With Endometriosis: A Reflexive Thematic " in items[0].title
    assert items[0].url == "https://pubmed.ncbi.nlm.nih.gov/37988744/"
    assert items[0].authors == "Lightbourne A, Foley S, Dempsey M, Cronin M."
    assert items[0].published == datetime(2023, 11, 21, 0, 0)
