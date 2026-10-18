# 🎾 ATP Tour 2027 Calendar

A clean, fast, structured reference for the **2027 ATP Tour season** — covering all 66 tournaments, with direct links to live ATP rankings and detailed event info.

> Source: [ATP 2027 Calendar (14 January 2026 update)](https://www.atptour.com/)
> Hosted on [GitHub Pages](https://pages.github.com/)

## ✨ Features

- 📅 **Complete calendar** — All 66 events from Brisbane (Jan 1) to Next Gen Finals (Dec)
- 🏟️ **Per-tournament pages** — 66 detail pages with descriptions, official websites, and live ranking links
- 🏷️ **Browse by category** — Grand Slams, Masters 1000, ATP 500, ATP 250, Finals, Davis Cup
- 📈 **Live ATP Rankings** — Direct links to authoritative sources (no scraping)
- 📱 **Mobile-friendly** — Responsive design, no JS required
- ⚡ **Static site** — Pure Jekyll, no server-side processing
- 🌍 **i18n-friendly** — Country flags + English tournament names

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Generator | [Jekyll 4.3](https://jekyllrb.com/) |
| Theme | [Minima](https://github.com/jekyll/minima) (customized) |
| Data | YAML |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions (auto-deploy on push) |

## 📂 Project Structure

```
atp-2027-calendar/
├── _config.yml                 # Jekyll config
├── _data/
│   ├── tournaments.yml         # All 66 events
│   ├── notes.yml               # Footnote legend
│   └── README.md               # Data schema
├── _layouts/
│   └── base.html               # Custom base layout
├── _sass/                      # Custom styles
│   └── _custom.scss
├── assets/css/
│   └── style.scss              # Main stylesheet
├── tournaments/                # 66 auto-generated detail pages
│   ├── australian-open.md
│   ├── roland-garros.md
│   └── ...
├── index.md                    # Homepage
├── calendar.md                 # Calendar by month
├── tournaments.md              # All tournaments (by category)
├── category.md                 # By category overview
├── rankings.md                 # Live rankings links
├── about.md                    # About
├── 404.html                    # 404 page
├── Gemfile                     # Ruby dependencies
└── README.md                   # This file
```

## 🚀 Local Development

### Prerequisites
- Ruby 3.0+
- Bundler

### Setup
```bash
git clone https://github.com/YOUR-USERNAME/atp-2027-calendar.git
cd atp-2027-calendar
bundle install
bundle exec jekyll serve --livereload
```

Visit `http://localhost:4000` to preview.

## 📝 Update Procedure

When the ATP releases a new calendar update (typically 2-3 times/year):

1. Edit `_data/tournaments.yml`
2. Add new entries, modify changed ones
3. Re-generate detail pages (optional — but recommended for new events):

```python
python3 _scripts/gen_tournament_pages.py
```

4. Commit and push. GitHub Pages will auto-rebuild in ~1 minute.

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
  draws: 18                            # Draw size (or teams for United Cup / TBD)
  notes: ["6"]                         # Footnote codes
  country: "AUS"                       # ISO 3166-1 alpha-3
  url: "https://..."                   # Official website
```

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
- [Ultimate Tennis Statistics](https://www.ultimatetennistatistics.com/) — Community-maintained stats

## 📄 License

MIT (code) / Fair use (data)

---

<sub>🎾 Built with ❤️ by tennis fans. Not affiliated with the ATP Tour.</sub>
