from datetime import datetime

import pytest
from aioresponses import aioresponses

from scifeed.providers import PapersWithCode

# flake8: noqa E501
raw_html = """
<div class="row infinite-item item paper-card">
    <!-- 1695088 -->
<div class="col-lg-3 item-image-col">
            <a href="/paper/characterizing-physiological-and-symptomatic">
                <div class="item-image" style="background-image: url('https://production-media.paperswithcode.com/thumbnails/paper/1909.11211.jpg');"> </div>
            </a>

</div>

    <div class="col-lg-9 item-col">
        <div class="row">
            <div class="col-lg-9 item-content">
                    <h1><a href="/paper/characterizing-physiological-and-symptomatic">Characterizing physiological and symptomatic variation</a></h1>
         <p class="author-section" style="padding-top:2px">
                                <a href="/paper/characterizing-physiological-and-symptomatic#code">1 code implementation</a>
                        •
                    <span class="author-name-text item-date-pub">14 May 2020</span>
         </p>
                    <p class="item-strip-abstract">The symptoms that we identify as showing statistically significant association with timing data can be useful to clinicians and users for predicting cycle variability from symptoms or as potential health indicators for conditions like endometriosis.</p>
                                    <div class="sota">
</div>
                <p>
                            <span class="badge badge-primary badge-primary-nohover">Quantitative Methods</span>
                            <span class="badge badge-primary badge-primary-nohover">Applications</span>
                </p>
            </div>
            <div class="col-lg-3 item-interact text-center">
                <div class="entity-stars">

                        <span class="badge badge-secondary"><span class=" icon-wrapper icon-ion" data-name="star"><svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><path d="M394 480a16 16 0 0 1-9.39-3L256 383.76 127.39 477a16 16 0 0 1-24.55-18.08L153 310.35 23 221.2a16 16 0 0 1 9-29.2h160.38l48.4-148.95a16 16 0 0 1 30.44 0l48.4 149H480a16 16 0 0 1 9.05 29.2L359 310.35l50.13 148.53A16 16 0 0 1 394 480z"/></svg></span> 17</span>
                </div>

                <div class="entity" style="margin-bottom: 20px;">

                    <a href="/paper/characterizing-physiological-and-symptomatic" class="badge badge-light ">
                         <span class=" icon-wrapper icon-ion" data-name="document"><svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><path d="M428 224H288a48 48 0 0 1-48-48V36a4 4 0 0 0-4-4h-92a64 64 0 0 0-64 64v320a64 64 0 0 0 64 64h224a64 64 0 0 0 64-64V228a4 4 0 0 0-4-4z"/><path d="M419.22 188.59L275.41 44.78a2 2 0 0 0-3.41 1.41V176a16 16 0 0 0 16 16h129.81a2 2 0 0 0 1.41-3.41z"/></svg></span> Paper
                    </a>

                    <br/>



                        <a href="/paper/characterizing-physiological-and-symptomatic#code" class="badge badge-dark ">
                             <span class=" icon-wrapper icon-ion" data-name="logo-github"><svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><path d="M256 32C132.3 32 32 134.9 32 261.7c0 101.5 64.2 187.5 153.2 217.9a17.56 17.56 0 0 0 3.8.4c8.3 0 11.5-6.1 11.5-11.4 0-5.5-.2-19.9-.3-39.1a102.4 102.4 0 0 1-22.6 2.7c-43.1 0-52.9-33.5-52.9-33.5-10.2-26.5-24.9-33.6-24.9-33.6-19.5-13.7-.1-14.1 1.4-14.1h.1c22.5 2 34.3 23.8 34.3 23.8 11.2 19.6 26.2 25.1 39.6 25.1a63 63 0 0 0 25.6-6c2-14.8 7.8-24.9 14.2-30.7-49.7-5.8-102-25.5-102-113.5 0-25.1 8.7-45.6 23-61.6-2.3-5.8-10-29.2 2.2-60.8a18.64 18.64 0 0 1 5-.5c8.1 0 26.4 3.1 56.6 24.1a208.21 208.21 0 0 1 112.2 0c30.2-21 48.5-24.1 56.6-24.1a18.64 18.64 0 0 1 5 .5c12.2 31.6 4.5 55 2.2 60.8 14.3 16.1 23 36.6 23 61.6 0 88.2-52.4 107.6-102.3 113.3 8 7.1 15.2 21.1 15.2 42.5 0 30.7-.3 55.5-.3 63 0 5.4 3.1 11.5 11.4 11.5a19.35 19.35 0 0 0 4-.4C415.9 449.2 480 363.1 480 261.7 480 134.9 379.7 32 256 32z"/></svg></span> Code
                        </a>

                        <br/>

                </div>
            </div>
        </div>
    </div>

</div>
<div class="row infinite-item item paper-card">
    <!-- 2198484 -->
<div class="col-lg-3 item-image-col">
            <a href="/paper/designing-and-evaluating-an-online">
                <div class="item-image" style="background-image: url('https://production-media.paperswithcode.com/thumbnails/paper/2309.14156.jpg');"> </div>
            </a>
</div>
    <div class="col-lg-9 item-col">
        <div class="row">
            <div class="col-lg-9 item-content">

                    <h1><a href="/paper/designing-and-evaluating-an-online">Designing and evaluating an online reinforcement learning agent for physical exercise recommendations in N-of-1 trials</a></h1>

         <p class="author-section" style="padding-top:2px">

                                <a href="/paper/designing-and-evaluating-an-online#code">1 code implementation</a>
                        •
                    <span class="author-name-text item-date-pub">25 Sep 2023</span>
         </p>
                    <p class="item-strip-abstract">In this paper, we present an innovative N-of-1 trial study design testing whether implementing a personalized intervention by an online reinforcement learning agent is feasible and effective.</p>
                                    <div class="sota">
</div>

                <p>
                    <a href="/task/reinforcement-learning-2">
                        <span class="badge badge-primary">

                                    <img src="https://production-media.paperswithcode.com/tasks/default.gif">
                        <span>reinforcement-learning</span>
                        </span>
                    </a>

                </p>

            </div>

            <div class="col-lg-3 item-interact text-center">
                <div class="entity-stars">
                        <span class="badge badge-secondary"><span class=" icon-wrapper icon-ion" data-name="star"><svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><path d="M394 480a16 16 0 0 1-9.39-3L256 383.76 127.39 477a16 16 0 0 1-24.55-18.08L153 310.35 23 221.2a16 16 0 0 1 9-29.2h160.38l48.4-148.95a16 16 0 0 1 30.44 0l48.4 149H480a16 16 0 0 1 9.05 29.2L359 310.35l50.13 148.53A16 16 0 0 1 394 480z"/></svg></span> 0</span>
                </div>
                <div class="entity" style="margin-bottom: 20px;">
                    <a href="/paper/designing-and-evaluating-an-online" class="badge badge-light ">
                         <span class=" icon-wrapper icon-ion" data-name="document"><svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><path d="M428 224H288a48 48 0 0 1-48-48V36a4 4 0 0 0-4-4h-92a64 64 0 0 0-64 64v320a64 64 0 0 0 64 64h224a64 64 0 0 0 64-64V228a4 4 0 0 0-4-4z"/><path d="M419.22 188.59L275.41 44.78a2 2 0 0 0-3.41 1.41V176a16 16 0 0 0 16 16h129.81a2 2 0 0 0 1.41-3.41z"/></svg></span> Paper
                    </a>
                    <br/>

                        <a href="/paper/designing-and-evaluating-an-online#code" class="badge badge-dark ">
                             <span class=" icon-wrapper icon-ion" data-name="logo-github"><svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><path d="M256 32C132.3 32 32 134.9 32 261.7c0 101.5 64.2 187.5 153.2 217.9a17.56 17.56 0 0 0 3.8.4c8.3 0 11.5-6.1 11.5-11.4 0-5.5-.2-19.9-.3-39.1a102.4 102.4 0 0 1-22.6 2.7c-43.1 0-52.9-33.5-52.9-33.5-10.2-26.5-24.9-33.6-24.9-33.6-19.5-13.7-.1-14.1 1.4-14.1h.1c22.5 2 34.3 23.8 34.3 23.8 11.2 19.6 26.2 25.1 39.6 25.1a63 63 0 0 0 25.6-6c2-14.8 7.8-24.9 14.2-30.7-49.7-5.8-102-25.5-102-113.5 0-25.1 8.7-45.6 23-61.6-2.3-5.8-10-29.2 2.2-60.8a18.64 18.64 0 0 1 5-.5c8.1 0 26.4 3.1 56.6 24.1a208.21 208.21 0 0 1 112.2 0c30.2-21 48.5-24.1 56.6-24.1a18.64 18.64 0 0 1 5 .5c12.2 31.6 4.5 55 2.2 60.8 14.3 16.1 23 36.6 23 61.6 0 88.2-52.4 107.6-102.3 113.3 8 7.1 15.2 21.1 15.2 42.5 0 30.7-.3 55.5-.3 63 0 5.4 3.1 11.5 11.4 11.5a19.35 19.35 0 0 0 4-.4C415.9 449.2 480 363.1 480 261.7 480 134.9 379.7 32 256 32z"/></svg></span> Code
                        </a>
                        <br/>
                </div>
            </div>
        </div>
    </div>
</div>
"""


@pytest.mark.asyncio()
async def test_paperswithcode_fetch():
    pm = PapersWithCode()
    with aioresponses() as m:
        m.get(
            "https://paperswithcode.com/search?page=1&q=test&sort_by=trending",
            body=raw_html,
            status=200,
        )
        items = await pm.fetch("test")
        assert len(items) == 2
        assert items[0].url == "https://paperswithcode.com/paper/characterizing-physiological-and-symptomatic"
        assert items[0].title == "Characterizing physiological and symptomatic variation"
        assert items[0].published == datetime(2020, 5, 14, 0, 0)
