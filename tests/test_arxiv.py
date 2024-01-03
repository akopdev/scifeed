from datetime import datetime

import pytest

from scifeed.providers import Arxiv, Crawler


class CrawlerMock(Crawler):
    async def open(self, *args, **kwargs):
        return open("tests/static/arxiv.html").read()


@pytest.mark.asyncio()
async def test_arxiv_fetch():
    ax = Arxiv(CrawlerMock())
    items = await ax.fetch("test")
    assert len(items) == 2
    assert "Designing and evaluating an online reinforcement learning agent for" in items[0].title
    assert items[0].url == "https://arxiv.org/abs/2309.14156"
    assert items[0].authors == "Dominik Meier, Ipek Ensari, Stefan Konigorski"
    assert items[0].published == datetime(2023, 9, 25, 0, 0)
