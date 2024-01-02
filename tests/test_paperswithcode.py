from datetime import datetime

import pytest

from scifeed.providers import PapersWithCode


async def handle(route):
    await route.fulfill(path="tests/static/paperswithcode.html")


@pytest.mark.asyncio()
async def test_paperswithcode_fetch(page_async):
    await page_async.route("https://paperswithcode.com/**", handle)
    pm = PapersWithCode(page_async)
    items = await pm.fetch("test")
    assert len(items) == 2
    assert (
        items[0].url
        == "https://paperswithcode.com/paper/characterizing-physiological-and-symptomatic"
    )
    assert items[0].title == "Characterizing physiological and symptomatic variation"
    assert items[0].published == datetime(2020, 5, 14, 0, 0)
