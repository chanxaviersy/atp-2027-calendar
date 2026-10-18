---
layout: default
title: Home
---

<section class="hero">
  <h1>🎾 ATP Tour 2027</h1>
  <p class="lead">The complete 2027 ATP tennis season — all 66 tournaments, from Brisbane to the Next Gen Finals.</p>
  <p>
    <a href="{{ '/calendar/' | relative_url }}" class="btn">View Calendar</a>
    <a href="{{ '/tournaments/' | relative_url }}" class="btn">All Tournaments</a>
    <a href="{{ '/rankings/' | relative_url }}" class="btn">Live Rankings</a>
  </p>
</section>

## 📊 Season at a Glance

<div class="stats">
  <div class="stat">
    <div class="num">66</div>
    <div class="label">Tournaments</div>
  </div>
  <div class="stat">
    <div class="num">4</div>
    <div class="label">Grand Slams</div>
  </div>
  <div class="stat">
    <div class="num">9</div>
    <div class="label">Masters 1000</div>
  </div>
  <div class="stat">
    <div class="num">15</div>
    <div class="label">ATP 500</div>
  </div>
  <div class="stat">
    <div class="num">31</div>
    <div class="label">ATP 250</div>
  </div>
</div>

## 🗓️ Key Dates

| Date | Event | Surface |
|------|-------|---------|
| Jan 17 – Jan 31 | **Australian Open** 🇦🇺 | Hard |
| Apr 12 – Apr 18 | **Monte-Carlo Masters** 🇲🇨 | Clay |
| May 23 – Jun 6 | **Roland Garros** 🇫🇷 | Clay |
| Jun 28 – Jul 11 | **Wimbledon** 🇬🇧 | Grass |
| Aug 29 – Sep 12 | **US Open** 🇺🇸 | Hard |
| Nov 14 – Nov 21 | **Nitto ATP Finals** 🇮🇹 | Indoor |

## 🏆 Featured Tournaments

- **Grand Slams (4)**: Australian Open, Roland Garros, Wimbledon, US Open
- **Masters 1000 (9)**: Indian Wells, Miami, Monte-Carlo, Madrid, Rome, Canada, Cincinnati, Shanghai, Paris
- **ATP Finals (2)**: Nitto ATP Finals, Next Gen ATP Finals
- **Team Events (3)**: United Cup, Davis Cup (Qualifiers 1st/2nd, Finals), Laver Cup

## 🔗 Quick Links

- 📅 [Full 2027 Calendar]({{ '/calendar/' | relative_url }})
- 🏟️ [All 66 Tournaments]({{ '/tournaments/' | relative_url }})
- 🏷️ [Browse by Category]({{ '/category/' | relative_url }})
- 📈 [Live ATP Rankings]({{ '/rankings/' | relative_url }})
- ℹ️ [About this Project]({{ '/about/' | relative_url }})

## 📝 Data Source

Calendar data sourced from the official **ATP 2027 Calendar** (14 January 2026 update). This site is auto-generated from structured YAML data — see the [data README]({{ '/data-readme/' | relative_url }}) for the schema and update procedure.

## 🤝 Contributing

Found an error or an update? The tournament data is in [`_data/tournaments.yml`]({{ site.repository | append: '/blob/main/_data/tournaments.yml' | prepend: 'https://github.com/' }}). Open a PR or issue.

---

<sub>Last updated: {{ site.time | date: "%B %d, %Y" }}</sub>
<!-- rebuild Sun Oct 18 18:11:37 HKT 2026 -->
