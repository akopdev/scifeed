from datetime import datetime

import pytest

from scifeed.providers import Arxiv


async def handle(route):
    await route.fulfill(path="tests/static/arxiv.html")


@pytest.mark.asyncio()
async def test_arxiv_fetch(page_async):
    await page_async.route("https://arxiv.org/**", handle)

    ax = Arxiv(page_async)
    items = await ax.fetch("test")
    assert len(items) == 2
    assert "Designing and evaluating an online reinforcement learning agent for" in items[0].title
    assert items[0].url == "https://arxiv.org/abs/2309.14156"
    assert items[0].authors == "Dominik Meier, Ipek Ensari, Stefan Konigorski"
    assert items[0].published == datetime(2023, 9, 25, 0, 0)
