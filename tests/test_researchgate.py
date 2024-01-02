import pytest
from playwright.async_api import Page

from scifeed.providers import ResearchGate


async def handle(route):
    await route.fulfill(path="tests/static/researchgate.html")


@pytest.mark.asyncio()
async def test_researchgate_fetch(page_async: Page):
    await page_async.route("https://www.researchgate.net/**", handle)
    rg = ResearchGate(page=page_async)
    items = await rg.fetch("test")
    assert len(items) == 10
    assert "Elagolix for endometriosis: all that glitters is not gold" in items[0].title
    assert (
        "publication/330883423_Elagolix_for_endometriosis_all_that_glitters_is_not_gold"
        in items[0].url
    )
    assert (
        items[0].authors
        == "Paolo Vercellini, Paola Vigano, Giussy Barbara, Laura Buggio, Edgardo Somigliana"
    )
