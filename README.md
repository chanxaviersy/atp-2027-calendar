# 🎾 ATP Tour 2027 Calendar

A clean, fast, structured reference for the **2027 ATP Tour season** — covering all 66 tournaments, with direct links to live ATP rankings and detailed event info.

> Source: [ATP 2027 Calendar (14 January 2026 update)](https://www.atptour.com/)
> Hosted on [GitHub Pages](https://pages.github.com/)
> 🌐 **Live site**: https://chanxaviersy.github.io/atp-2027-calendar/

## ✨ Features

- 📅 **Complete calendar** — All 66 events from Brisbane (Jan 1) to Next Gen Finals (Dec)
- 🏟️ **Per-tournament pages** — 66 detail pages with descriptions, official websites, and live ranking links
- 🏷️ **Browse by category** — Grand Slams, Masters 1000, ATP 500, ATP 250, Finals, Davis Cup
- 📈 **Live ATP Rankings** — Direct links to authoritative sources (no scraping)
- 📱 **Mobile-friendly** — Responsive design, no JS required
- ⚡ **Static site** — Pure HTML/CSS, no build server needed
- 🌍 **i18n-friendly** — Country flags + English tournament names

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Generator | Python (no Jekyll, no Node) |
| Output | Pure static HTML/CSS |
| Data | YAML (66 events) |
| Hosting | GitHub Pages |
| CI/CD | None needed (push to update) |

## 📂 Project Structure

```
atp-2027-calendar/
├── _data/
│   ├── tournaments.yml         # All 66 events
│   ├── notes.yml               # Footnote legend
│   └── README.md               # Data schema
├── _scripts/
│   ├── build.py                # Static site generator
│   └── iso_codes.py            # ISO 3166 mapping
├── docs/                       # GitHub Pages serves from here
│   ├── index.html              # Homepage
│   ├── calendar/index.html
│   ├── tournaments/index.html
│   ├── category/index.html
│   ├── rankings/index.html
│   ├── about/index.html
│   ├── 404.html
│   ├── assets/css/style.css
│   ├── robots.txt
│   ├── sitemap-data.json
│   └── tournaments/            # 66 per-event pages
│       ├── australian-open/index.html
│       ├── roland-garros/index.html
│       └── ...
├── .github/                    # (workflows - gitignored due to token scope)
├── _config.yml                 # (legacy Jekyll config)
├── Gemfile                     # (legacy)
└── README.md                   # This file
```

## 🚀 Local Development

No build tools required. The `docs/` folder is fully static — just open `docs/index.html` in a browser.

To regenerate after data changes:

```bash
python3 _scripts/build.py
```

That regenerates the entire `docs/` folder from `_data/tournaments.yml`.

## 📝 Update Procedure

When the ATP releases a new calendar update (typically 2-3 times/year):

1. Edit `_data/tournaments.yml` (add/modify entries)
2. Run `python3 _scripts/build.py`
3. Commit and push the `docs/` folder

GitHub Pages auto-deploys in ~1 minute.

## 🗂️ Data Schema

Each tournament in `tournaments.yml`:

```yaml
- week: 1                              # Calendar week
  start_date: 2027-01-01               # ISO date
  end_date: 2027-01-04                 # ISO date
  city: "Perth, Sydney"                # Host city
  tournament: "United Cup"             # Official name
  surface: "Hard"                      # Hard, Clay, Grass, Indoor Hard, Various
  category: "United Cup"               # Grand Slam, ATP Masters 1000, ATP 500, ATP 250, ATP Finals, Davis Cup, Laver Cup, United Cup
  draws: 18                            # Draw size (or teams for United Cup)
  notes: ["6"]                         # Footnote codes
  country: "AUS"                       # ISO 3166-1 alpha-3
  url: "https://..."                   # Official website
```

## 🔗 Important Pages

- 🏠 [Home](https://chanxaviersy.github.io/atp-2027-calendar/)
- 📅 [Calendar (by month)](https://chanxaviersy.github.io/atp-2027-calendar/calendar/)
- 🏟️ [All 66 Tournaments](https://chanxaviersy.github.io/atp-2027-calendar/tournaments/)
- 🏷️ [By Category](https://chanxaviersy.github.io/atp-2027-calendar/category/)
- 📈 [Live Rankings](https://chanxaviersy.github.io/atp-2027-calendar/rankings/)
- ℹ️ [About](https://chanxaviersy.github.io/atp-2027-calendar/about/)

## 🤝 Contributing

PRs welcome! Common contributions:
- 🐛 Fix typos or broken links
- 📅 Update dates (after new ATP calendar release)
- 🏟️ Add new tournaments
- 🌐 Add country flag mapping for missing codes
- 📝 Improve tournament descriptions

## 📜 Data Sources & License

- **Calendar data**: © ATP Tour. Used under fair use for informational purposes.
- **Tournament websites**: Linked to, not embedded.
- **Rankings**: Direct links to [ATP official](https://www.atptour.com/en/rankings/singles), not republished.

## 🎾 Related Projects

- [nlp-ml-knowledge-base](https://github.com/chanxaviersy/nlp-ml-knowledge-base) — A comprehensive NLP/ML knowledge base

## 📄 License

MIT (code) / Fair use (data)

---

<sub>🎾 Built with ❤️ by tennis fans. Not affiliated with the ATP Tour.</sub>

