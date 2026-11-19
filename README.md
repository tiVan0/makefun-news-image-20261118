# Wednesday 18 November 2026 in 43 stories

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/tiVan0/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/tiVan0/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

Resubmitted after the first round-1 grade run failed (run_completes); entry code unchanged.

A one-page newspaper front page for Wednesday 18 November 2026: 3 lead
stories, 10 cards, 30 more stories, a dotted world map with every story
pinned, and a BY THE NUMBERS strip. 43 stories, 6 continents, one day.

## Run

```sh
python3 main.py
```

Writes `entry.png` (1024 x 1024, under 1 MiB). Deterministic: every run
produces byte-identical output.

## How it is drawn

Everything is drawn in code with PIL only: the scenes are compositions of
shapes and gradients (sea, ship, drones, skyline, cyclone, chip, dunes,
bridge, parliament, stars, tents, tower, cargo ship, globe, dome), the
world map is a hand-authored dotted land grid, and the text uses embedded
bitmap fonts (DejaVu, generated from the font tables). No photos, no AI
images, no network access at render time. Python 3 standard library +
Pillow only.

## Sources

Every story was reported on Wednesday 18 November 2026 or in the overnight
bulletins that opened the day. Disputed claims are attributed: Gaza toll to
Gaza health authorities via AP; An-12 toll to the Russian ministry; the
1,441-drone claim is not presented as fact. Sources: AP, Reuters, AFP,
BBC, UN, NASA and others.
