from datetime import datetime

import pytest
from aioresponses import aioresponses

from scifeed.providers import PubMed

# flake8: noqa E501
raw_html = """
<article class="full-docsum" data-rel-pos="1">



<div class="item-selector-wrap selectors-and-actions first-selector">
  <input class="search-result-selector" type="checkbox" name="search-result-selector-37988744" id="select-37988744" value="37988744" aria-labelledby="result-selector-label"/>

  <label class="search-result-position" for="select-37988744"><span class="position-number">1</span></label>







  <div class="result-actions-bar side-bar">


  <div class="cite">

    <button class="cite-search-result trigger result-action-trigger citation-dialog-trigger"
            aria-haspopup="true" data-ga-category="save_share" data-ga-action="cite" data-ga-label="open"
            data-all-citations-url="/37988744/citations/"
            data-citation-style="nlm"
            data-pubmed-format-link="/37988744/export/">
      Cite
    </button>
  </div>


  <div class="share">
    <button class="share-search-result trigger result-action-trigger share-dialog-trigger" aria-haspopup="true"
            data-twitter-url="http://twitter.com/intent/tweet?text=Living%20With%20Endometriosis%3A%20A%20Reflexive%20Thematic%20Analysis%20Examining%20Women%27s%20Experiences%20With%20the%20Irish%20Healthcare%20Se%E2%80%A6%20https%3A//pubmed.ncbi.nlm.nih.gov/37988744/"
            data-facebook-url="http://www.facebook.com/sharer/sharer.php?u=https%3A//pubmed.ncbi.nlm.nih.gov/37988744/"
            data-permalink-url="https://pubmed.ncbi.nlm.nih.gov/37988744/">
      Share
    </button>
  </div>



  </div>



</div>

    <div class="docsum-wrap">
      <div class="docsum-content">




            <a
              class="docsum-title"
              href="/37988744/"
              ref="linksrc=docsum_link&amp;article_id=37988744&amp;ordinalpos=1&amp;page=1"
              data-ga-category="result_click"
              data-ga-action="1"
              data-ga-label="37988744"
              data-full-article-url="from_term=endometriosis&amp;from_sort=date&amp;from_size=100&amp;from_pos=1"
              data-article-id="37988744">

                Living With <b>Endometriosis</b>: A Reflexive Thematic Analysis Examining Women's Experiences With the Irish Healthcare Services.

            </a>
            <div class="docsum-citation full-citation">



        <span class="docsum-authors full-authors">Lightbourne A, Foley S, Dempsey M, Cronin M.</span>



    <span class="docsum-authors short-authors">Lightbourne A, et al.</span>
    <span class="docsum-journal-citation full-journal-citation">Qual Health Res. 2023 Nov 21:10497323231214114. doi: 10.1177/10497323231214114. Online ahead of print.</span>
    <span class="docsum-journal-citation short-journal-citation">Qual Health Res. 2023.</span>

  <span class="citation-part">PMID: <span class="docsum-pmid">37988744</span></span>





</div>




          <div class="docsum-snippet">
            <div class="full-view-snippet">
              <span><b>Endometriosis</b> is an incurable chronic condition associated with debilitating pain and subfertility, affecting 1 in 10 women. The current study aims to explore the perceptions and experiences of women with <b>endometriosis</b> regarding the diagnosis, support and treatment</span> …
            </div>
            <div class="short-view-snippet">
              <span><b>Endometriosis</b> is an incurable chronic condition associated with debilitating pain and subfertility, affecting 1 in 10 women. The curr</span> …
            </div>
          </div>

      </div>





  <div class="result-actions-bar bottom-bar">


  <div class="cite">

    <button class="cite-search-result trigger result-action-trigger citation-dialog-trigger"
            aria-haspopup="true" data-ga-category="save_share" data-ga-action="cite" data-ga-label="open"
            data-all-citations-url="/37988744/citations/"
            data-citation-style="nlm"
            data-pubmed-format-link="/37988744/export/">
      Cite
    </button>
  </div>


  <div class="share">
    <button class="share-search-result trigger result-action-trigger share-dialog-trigger" aria-haspopup="true"
            data-twitter-url="http://twitter.com/intent/tweet?text=Living%20With%20Endometriosis%3A%20A%20Reflexive%20Thematic%20Analysis%20Examining%20Women%27s%20Experiences%20With%20the%20Irish%20Healthcare%20Se%E2%80%A6%20https%3A//pubmed.ncbi.nlm.nih.gov/37988744/"
            data-facebook-url="http://www.facebook.com/sharer/sharer.php?u=https%3A//pubmed.ncbi.nlm.nih.gov/37988744/"
            data-permalink-url="https://pubmed.ncbi.nlm.nih.gov/37988744/">
      Share
    </button>
  </div>


  <div class="in-clipboard-label " hidden>
  Item in Clipboard
</div>


  </div>



    </div>
  </article>










  <article class="full-docsum" data-rel-pos="2">



<div class="item-selector-wrap selectors-and-actions">
  <input class="search-result-selector" type="checkbox" name="search-result-selector-37987824" id="select-37987824" value="37987824" aria-labelledby="result-selector-label"/>

  <label class="search-result-position" for="select-37987824"><span class="position-number">2</span></label>







  <div class="result-actions-bar side-bar">


  <div class="cite">

    <button class="cite-search-result trigger result-action-trigger citation-dialog-trigger"
            aria-haspopup="true" data-ga-category="save_share" data-ga-action="cite" data-ga-label="open"
            data-all-citations-url="/37987824/citations/"
            data-citation-style="nlm"
            data-pubmed-format-link="/37987824/export/">
      Cite
    </button>
  </div>


  <div class="share">
    <button class="share-search-result trigger result-action-trigger share-dialog-trigger" aria-haspopup="true"
            data-twitter-url="http://twitter.com/intent/tweet?text=Pilot%20study%20of%20treatment%20of%20patients%20with%20deep%20infiltrative%20endometriosis%20with%20methotrexate%20carried%20in%20lipid%20nanopa%E2%80%A6%20https%3A//pubmed.ncbi.nlm.nih.gov/37987824/"
            data-facebook-url="http://www.facebook.com/sharer/sharer.php?u=https%3A//pubmed.ncbi.nlm.nih.gov/37987824/"
            data-permalink-url="https://pubmed.ncbi.nlm.nih.gov/37987824/">
      Share
    </button>
  </div>



  </div>



</div>

    <div class="docsum-wrap">
      <div class="docsum-content">




            <a
              class="docsum-title"
              href="/37987824/"
              ref="linksrc=docsum_link&amp;article_id=37987824&amp;ordinalpos=2&amp;page=1"
              data-ga-category="result_click"
              data-ga-action="2"
              data-ga-label="37987824"
              data-full-article-url="from_term=endometriosis&amp;from_sort=date&amp;from_size=100&amp;from_pos=2"
              data-article-id="37987824">

                Pilot study of treatment of patients with deep infiltrative <b>endometriosis</b> with methotrexate carried in lipid nanoparticles.

            </a>
            <div class="docsum-citation full-citation">



        <span class="docsum-authors full-authors">Avila-Tavares R, Gibran L, Brito LGO, Tavoni TM, Gonçalves MO, Baracat EC, Maranhão RC, Podgaec S.</span>



    <span class="docsum-authors short-authors">Avila-Tavares R, et al.</span>
    <span class="docsum-journal-citation full-journal-citation">Arch Gynecol Obstet. 2023 Nov 21. doi: 10.1007/s00404-023-07246-8. Online ahead of print.</span>
    <span class="docsum-journal-citation short-journal-citation">Arch Gynecol Obstet. 2023.</span>

  <span class="citation-part">PMID: <span class="docsum-pmid">37987824</span></span>





</div>




          <div class="docsum-snippet">
            <div class="full-view-snippet">
              OBJECTIVE: Previously, lipid nanoparticles (LDE) injected in women with <b>endometriosis</b> were shown to concentrate in the lesions. Here, the safety and feasibility of LDE carrying methotrexate (MTX) to treat deep infiltrating <b>endometriosis</b> was tested. ...SUBJECTS: Elev …
            </div>
            <div class="short-view-snippet">
              OBJECTIVE: Previously, lipid nanoparticles (LDE) injected in women with <b>endometriosis</b> were shown to concentrate in the lesions. Here, …
            </div>
          </div>

      </div>





  <div class="result-actions-bar bottom-bar">


  <div class="cite">

    <button class="cite-search-result trigger result-action-trigger citation-dialog-trigger"
            aria-haspopup="true" data-ga-category="save_share" data-ga-action="cite" data-ga-label="open"
            data-all-citations-url="/37987824/citations/"
            data-citation-style="nlm"
            data-pubmed-format-link="/37987824/export/">
      Cite
    </button>
  </div>


  <div class="share">
    <button class="share-search-result trigger result-action-trigger share-dialog-trigger" aria-haspopup="true"
            data-twitter-url="http://twitter.com/intent/tweet?text=Pilot%20study%20of%20treatment%20of%20patients%20with%20deep%20infiltrative%20endometriosis%20with%20methotrexate%20carried%20in%20lipid%20nanopa%E2%80%A6%20https%3A//pubmed.ncbi.nlm.nih.gov/37987824/"
            data-facebook-url="http://www.facebook.com/sharer/sharer.php?u=https%3A//pubmed.ncbi.nlm.nih.gov/37987824/"
            data-permalink-url="https://pubmed.ncbi.nlm.nih.gov/37987824/">
      Share
    </button>
  </div>


  <div class="in-clipboard-label " hidden>
  Item in Clipboard
</div>


  </div>



    </div>
  </article>
"""


@pytest.mark.asyncio()
async def test_pubmed_fetch():
    pm = PubMed()
    with aioresponses() as m:
        m.get(
            "https://pubmed.ncbi.nlm.nih.gov?term=test&sort=date&size=50&page=1",
            body=raw_html,
            status=200,
        )
        items = await pm.fetch("test")
        assert len(items) == 2
        assert "Living With Endometriosis: A Reflexive Thematic " in items[0].title
        assert items[0].url == "https://pubmed.ncbi.nlm.nih.gov/37988744/"
        assert items[0].authors == "Lightbourne A, Foley S, Dempsey M, Cronin M."
        assert items[0].published == datetime(2023, 11, 21, 0, 0)
