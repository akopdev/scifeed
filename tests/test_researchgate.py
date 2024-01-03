import pytest

from scifeed.providers import Crawler, ResearchGate


class CrawlerMock(Crawler):
    async def open(self, *args, **kwargs):
        return open("tests/static/researchgate.html").read()


@pytest.mark.asyncio()
async def test_researchgate_fetch():
    rg = ResearchGate(CrawlerMock())
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
