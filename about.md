---
layout: base
title: About
---

# ℹ️ About This Project

A static, structured, easy-to-update reference for the **2027 ATP Tour season**.

## 🎯 Goals

1. **Single source of truth** — All tournament data lives in one YAML file
2. **No stale data** — Direct links to live rankings (no scraping)
3. **Free hosting** — Uses GitHub Pages with Jekyll
4. **Zero JS** — Pure HTML/CSS for fast loads and great SEO
5. **Community-friendly** — Anyone can submit a PR to fix a typo or update dates

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Static site | [Jekyll](https://jekyllrb.com/) |
| Theme | [Minima](https://github.com/jekyll/minima) (customized) |
| Data format | [YAML](https://yaml.org/) |
| Hosting | [GitHub Pages](https://pages.github.com/) |
| Version control | Git |

## 📂 Project Structure

```
atp-2027-calendar/
├── _config.yml              # Jekyll config
├── _data/
│   ├── tournaments.yml      # Master data (66 events)
│   ├── notes.yml            # Footnote legend
│   └── README.md            # Data schema docs
├── _includes/               # Reusable HTML partials
├── _layouts/                # Page templates
├── _sass/                   # Custom styles
├── assets/
│   └── css/
│       └── style.scss       # Custom CSS
├── index.md                 # Homepage
├── calendar.md              # Calendar by month
├── tournaments.md           # All tournaments (by category)
├── category.md              # By category overview
├── rankings.md              # Live rankings links
├── about.md                 # This file
└── tournaments/             # Auto-generated per-event pages
    └── [name].md
```

## 🔄 How to Update

When the ATP releases a calendar update:

1. Fork this repo
2. Edit `_data/tournaments.yml` (or just the relevant entries)
3. Open a pull request

GitHub Actions / Pages will auto-rebuild the site in ~1 minute.

## 📜 Data License

- **Calendar data**: © ATP Tour. Used under fair use for informational purposes.
- **Tournament websites**: Linked to, not embedded.
- **Rankings**: Linked to the official ATP site, not republished.

## 🤝 Contributing

PRs welcome! Common contributions:
- 🐛 Fix typos or broken links
- 📅 Update tournament dates (after new ATP calendar release)
- 🏟️ Add new tournaments
- 🌐 Add country flags / translations

## 📬 Contact

Open an issue on the [GitHub repo]({{ site.repository | prepend: 'https://github.com/' }}).

---

<sub>Built with ❤️ by the tennis community. Not affiliated with the ATP Tour.</sub>
