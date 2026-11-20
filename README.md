# The Global Edition — Friday 20 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261120-blue)](https://make.fun)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stories](https://img.shields.io/badge/stories-56-red)](SOURCES.md)
[![Regions](https://img.shields.io/badge/regions-7-green)](SOURCES.md)

One image. The whole world, dated and sourced.

**The Global Edition** sums up Friday 20 November 2026 in a single 1024×1024
world-news poster: **56 numbered stories across 7 regions**, every one published
or reported on 20 Nov 2026 and tagged with its outlet on the page.

## What is on the poster

- **3 lead stories** — the Trump–Xi–Putin "peace declaration" from Shenzhen, the
  World Court's Myanmar genocide ruling (9–6), and Anthropic's record $81.3bn IPO.
- **Dot-matrix world map** with 7 numbered region pins + a region key.
- **16 illustrated scenes** drawn from the day's stories.
- **The day in 56 stories** — 8 per region, each with its outlet tag.
- **UTC timeline** of the day's timed events, **by-the-numbers** strip, and a
  **weather strip** (day highs from the forecast issued 19 Nov).
- **"Left out & why"** box — the date rule, and what was excluded for being
  stale or unverified.

## Sources

Every story is listed with outlet, date and verification URL in
[SOURCES.md](SOURCES.md). Note: the Just Security Early Edition for 20 Nov 2026
had not been published yet at build time (09:24 WIB / 02:24 UTC), so stories
were verified against Reuters, AP, BBC, The Guardian and the other outlets
listed there instead.

## Regenerate

```sh
python3 main.py   # writes entry.png (1024x1024, deterministic) and SOURCES.md
```

No network calls, no timestamps, no randomness — two runs produce a
byte-identical `entry.png`.

## About

Built for the make.fun competition
[`news-image-20261120`](https://make.fun) — "Sum up 20 November's world news
in one image". Entry by
[@salikamarlisa3-cell](https://github.com/salikamarlisa3-cell).
Prepared 2026-11-20; submission awaits the owner's paste into the make.fun
Ruang Build chat before the deadline (2026-11-22 07:00 WIB).

## License

MIT — see [LICENSE](LICENSE).
