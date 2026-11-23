# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dftaufiq/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dftaufiq/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up the world's news of Tuesday 24 November 2026: a newspaper front page with 38 stories across 7 regions — 1 illustrated lead story, 4 illustrated features, a numbered dotted world map with 12 pinned stories, and 21 more briefs — every one of them dated to Tuesday 24 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory. The image itself is drawn from scratch by `generate_image.py` (build-time only, needs Pillow) — no photographs or copied artwork: every panel, illustration and the dotted world map are drawn in code. Every story on the page was checked against reporting of 24 November 2026, with sources named beside each story:

- Antalya: COP31 collapses — no deal on fossil fuels. Two weeks of talks end without agreement on phasing out fossil fuels; the Guardian asks what the failure reveals about a divided world. Small island states call it a betrayal; UN chief Guterres: "deeply disappointed."
- Banten, Indonesia: factory fire kills at least 24, around 30 missing as rescuers search the burned-out factory
- New York: Wall Street sells off after the Democrats' midterm win — $1 trillion wiped out; Trump blames the Democrats: "As I predicted"
- Ukraine at sea: a Russian cargo ship burns off Finland after a drone strike; a suspected drone boat hits a Russian ship off Benghazi, Libya, 10 hurt; a Russian drone strike on a Kyiv-region apartment block kills 8, 11 feared buried
- New Delhi: Modi and Nepal PM Balendra Shah flag off the Saryu-Kamala Express, sign 8 MoUs and a Rs 15,000-crore package
- Washington: Trump warns Iran of a "very traumatic" outcome if a nuclear deal fails and weighs sending a second aircraft carrier; Trump urges Nvidia to bring back Jensen Huang as CEO
- Lisbon: thousands march over living costs; Dhaka: Bangladesh vows to arrest Sheikh Hasina if she returns; Wellington: Rishabh Pant hits 128 as the first Test against New Zealand ends in a draw; Las Vegas: Verstappen wins the Grand Prix
- Plus the West Bank settler-violence condemnation, the EU sanctions package on Russia, the Don Toliver concert evacuation in Manchester, Gisèle Pelicot's statement, China's 2030 welfare targets, South Korea's reshuffle, Armenia's new constitution, the Sensex's 1,484-point fall, India's oil import bill up 60%, and SoftBank's reported $2bn Intel investment — and 21 briefs

The DATE CHECK box at the foot of the page names the big stories deliberately left out because they happened on earlier days (Iran's strikes on US bases of Wed 18 Nov, the Shenzhen APEC summit of Sat 21 Nov, Cyclone Akvan's landfall) — and flags honestly that COP31's collapse came at Sunday's closing plenary and the Democrats' House win was sealed Sunday, both leading Tuesday's pages because the fallout dominates the day. Africa briefs were first reported 22–23 Nov.

To redraw the image from its source data: `python3 generate_image.py`

---

<sub>Entered on [make.fun](https://make.fun/?ref=bqc0tvks&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
