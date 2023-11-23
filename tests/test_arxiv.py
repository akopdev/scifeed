from datetime import datetime

import pytest
from aioresponses import aioresponses

from scifeed.providers import Arxiv

# flake8: noqa E501
raw_html = """
  <li class="arxiv-result">
    <div class="is-marginless">
      <p class="list-title is-inline-block"><a href="https://arxiv.org/abs/2309.14156">arXiv:2309.14156</a>
        <span>&nbsp;[<a href="https://arxiv.org/pdf/2309.14156">pdf</a>, <a href="https://arxiv.org/format/2309.14156">other</a>]&nbsp;</span>
      </p>
      <div class="tags is-inline-block">
        <span class="tag is-small is-link tooltip is-tooltip-top" data-tooltip="Machine Learning">cs.LG</span>


            <span class="tag is-small is-grey tooltip is-tooltip-top" data-tooltip="Applications">stat.AP</span>

            <span class="tag is-small is-grey tooltip is-tooltip-top" data-tooltip="Methodology">stat.ME</span>

        </div>

    </div>

    <p class="title is-5 mathjax">

        Designing and evaluating an online reinforcement learning agent for physical exercise recommendations in N-of-1 trials

    </p>
    <p class="authors">
      <span class="has-text-black-bis has-text-weight-semibold">Authors:</span>

      <a href="/search/?searchtype=author&amp;query=Meier%2C+D">Dominik Meier</a>,

      <a href="/search/?searchtype=author&amp;query=Ensari%2C+I">Ipek Ensari</a>,

      <a href="/search/?searchtype=author&amp;query=Konigorski%2C+S">Stefan Konigorski</a>

    </p>

    <p class="abstract mathjax">
      <span class="search-hit">Abstract</span>:
      <span class="abstract-short has-text-grey-dark mathjax" id="2309.14156v1-abstract-short" style="display: inline;">
        &hellip;intervention by an online reinforcement learning agent is feasible and effective. Throughout, we use a new study on physical exercise recommendations to reduce pain in <span class="search-hit mathjax">endometriosis</span> for illustration. We describe the design of a contextual bandit recommendation agent and evaluate the agent in simulation studies. The results show that adaptive interventions ad&hellip;
        <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2309.14156v1-abstract-full').style.display = 'inline'; document.getElementById('2309.14156v1-abstract-short').style.display = 'none';">&#9661; More</a>
      </span>
      <span class="abstract-full has-text-grey-dark mathjax" id="2309.14156v1-abstract-full" style="display: none;">
        Personalized adaptive interventions offer the opportunity to increase patient benefits, however, there are challenges in their planning and implementation. Once implemented, it is an important question whether personalized adaptive interventions are indeed clinically more effective compared to a fixed gold standard intervention. In this paper, we present an innovative N-of-1 trial study design testing whether implementing a personalized intervention by an online reinforcement learning agent is feasible and effective. Throughout, we use a new study on physical exercise recommendations to reduce pain in <span class="search-hit mathjax">endometriosis</span> for illustration. We describe the design of a contextual bandit recommendation agent and evaluate the agent in simulation studies. The results show that adaptive interventions add complexity to the design and implementation process, but have the potential to improve patients&#39; benefits even if only few observations are available. In order to quantify the expected benefit, data from previous interventional studies is required. We expect our approach to be transferable to other interventions and clinical interventions.
        <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2309.14156v1-abstract-full').style.display = 'none'; document.getElementById('2309.14156v1-abstract-short').style.display = 'inline';">&#9651; Less</a>
      </span>
    </p>


    <p class="is-size-7"><span class="has-text-black-bis has-text-weight-semibold">Submitted</span> 25 September, 2023;
      <span class="has-text-black-bis has-text-weight-semibold">originally announced</span> September 2023.

    </p>





  </li>

  <li class="arxiv-result">
    <div class="is-marginless">
      <p class="list-title is-inline-block"><a href="https://arxiv.org/abs/2307.02000">arXiv:2307.02000</a>
        <span>&nbsp;[<a href="https://arxiv.org/pdf/2307.02000">pdf</a>, <a href="https://arxiv.org/format/2307.02000">other</a>]&nbsp;</span>
      </p>
      <div class="tags is-inline-block">
        <span class="tag is-small is-link tooltip is-tooltip-top" data-tooltip="Image and Video Processing">eess.IV</span>


            <span class="tag is-small is-grey tooltip is-tooltip-top" data-tooltip="Computer Vision and Pattern Recognition">cs.CV</span>

            <span class="tag is-small is-grey tooltip is-tooltip-top" data-tooltip="Machine Learning">cs.LG</span>

        </div>

    </div>

    <p class="title is-5 mathjax">

        Distilling Missing Modality Knowledge from Ultrasound for <span class="search-hit mathjax">Endometriosis</span> Diagnosis with Magnetic Resonance Images

    </p>
    <p class="authors">
      <span class="has-text-black-bis has-text-weight-semibold">Authors:</span>

      <a href="/search/?searchtype=author&amp;query=Zhang%2C+Y">Yuan Zhang</a>,

      <a href="/search/?searchtype=author&amp;query=Wang%2C+H">Hu Wang</a>,

      <a href="/search/?searchtype=author&amp;query=Butler%2C+D">David Butler</a>,

      <a href="/search/?searchtype=author&amp;query=To%2C+M">Minh-Son To</a>,

      <a href="/search/?searchtype=author&amp;query=Avery%2C+J">Jodie Avery</a>,

      <a href="/search/?searchtype=author&amp;query=Hull%2C+M+L">M Louise Hull</a>,

      <a href="/search/?searchtype=author&amp;query=Carneiro%2C+G">Gustavo Carneiro</a>

    </p>

    <p class="abstract mathjax">
      <span class="search-hit">Abstract</span>:
      <span class="abstract-short has-text-grey-dark mathjax" id="2307.02000v1-abstract-short" style="display: inline;">
        <span class="search-hit mathjax">Endometriosis</span> is a common chronic gynecological disorder that has many characteristics, including the pouch of Douglas (POD) obliteration, which can be diagnosed using Transvaginal gynecological ultrasound (TVUS) scans and magnetic resonance imaging (MRI). TVUS and MRI are complementary non-invasive&hellip;
        <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2307.02000v1-abstract-full').style.display = 'inline'; document.getElementById('2307.02000v1-abstract-short').style.display = 'none';">&#9661; More</a>
      </span>
      <span class="abstract-full has-text-grey-dark mathjax" id="2307.02000v1-abstract-full" style="display: none;">
        <span class="search-hit mathjax">Endometriosis</span> is a common chronic gynecological disorder that has many characteristics, including the pouch of Douglas (POD) obliteration, which can be diagnosed using Transvaginal gynecological ultrasound (TVUS) scans and magnetic resonance imaging (MRI). TVUS and MRI are complementary non-invasive <span class="search-hit mathjax">endometriosis</span> diagnosis imaging techniques, but patients are usually not scanned using both modalities and, it is generally more challenging to detect POD obliteration from MRI than TVUS. To mitigate this classification imbalance, we propose in this paper a knowledge distillation training algorithm to improve the POD obliteration detection from MRI by leveraging the detection results from unpaired TVUS data. More specifically, our algorithm pre-trains a teacher model to detect POD obliteration from TVUS data, and it also pre-trains a student model with 3D masked auto-encoder using a large amount of unlabelled pelvic 3D MRI volumes. Next, we distill the knowledge from the teacher TVUS POD obliteration detector to train the student MRI model by minimizing a regression loss that approximates the output of the student to the teacher using unpaired TVUS and MRI data. Experimental results on our <span class="search-hit mathjax">endometriosis</span> dataset containing TVUS and MRI data demonstrate the effectiveness of our method to improve the POD detection accuracy from MRI.
        <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2307.02000v1-abstract-full').style.display = 'none'; document.getElementById('2307.02000v1-abstract-short').style.display = 'inline';">&#9651; Less</a>
      </span>
    </p>


    <p class="is-size-7"><span class="has-text-black-bis has-text-weight-semibold">Submitted</span> 4 July, 2023;
      <span class="has-text-black-bis has-text-weight-semibold">originally announced</span> July 2023.

    </p>

    <p class="comments is-size-7">
      <span class="has-text-black-bis has-text-weight-semibold">Comments:</span>
      <span class="has-text-grey-dark mathjax">This paper is accepted by 2023 IEEE 20th International Symposium on Biomedical Imaging(ISBI 2023)</span>
    </p>





  </li>

"""


@pytest.mark.asyncio()
async def test_pubmed_fetch():
    ax = Arxiv()
    with aioresponses() as m:
        m.get(
            "https://arxiv.org/search/?query=test&searchtype=all&source=header",
            body=raw_html,
            status=200,
        )
        items = await ax.fetch("test")
        assert len(items) == 2
        assert (
            "Designing and evaluating an online reinforcement learning agent for" in items[0].title
        )
        assert items[0].url == "https://arxiv.org/abs/2309.14156"
        assert items[0].authors == "Dominik Meier, Ipek Ensari, Stefan Konigorski"
        assert items[0].published == datetime(2023, 9, 25, 0, 0)
