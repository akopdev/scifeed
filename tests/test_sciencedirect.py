import pytest
from playwright.async_api import Page

from scifeed.providers import ScienceDirect


async def handle(route):
    await route.fulfill(path="tests/static/sciencedirect.html")


@pytest.mark.asyncio()
async def test_sciencedirect_fetch(page_async: Page):
    await page_async.route("https://www.sciencedirect.com/**", handle)
    rg = ScienceDirect(page=page_async)
    items = await rg.fetch("test")
    assert len(items) == 25
    assert "Identification and validation of M2 macrophage-related genes" in items[0].title
    assert "https://www.sciencedirect.com/science/article/pii/S2405844023094665" in items[0].url
    assert "Hongyan Ding" in items[0].authors
