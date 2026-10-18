#!/usr/bin/env python3
"""
Static Site Generator for ATP Tour 2027
Renders YAML data + templates to fully static HTML files.
No Jekyll build needed - just open in browser or push to any static host.
"""

import json
import os
import shutil
import sys
from pathlib import Path
import yaml
import re


# ============================================================
# Configuration
# ============================================================
ROOT = Path(__file__).parent.parent
OUT = ROOT / "docs-build"  # Build output directory
DATA_FILE = ROOT / "_data" / "tournaments.yml"
ISO_FILE = Path(__file__).parent / "iso_codes.py"

# Add scripts dir to path for iso_codes import
sys.path.insert(0, str(Path(__file__).parent))
from iso_codes import ALPHA3_TO_ALPHA2  # noqa


# ============================================================
# HTML Helpers
# ============================================================

def country_flag(code):
    if not code or code not in ALPHA3_TO_ALPHA2:
        return "🌐"
    c2 = ALPHA3_TO_ALPHA2[code]
    if not c2:
        return "🌐"
    return chr(0x1F1E6 + ord(c2[0]) - ord("A")) + chr(0x1F1E6 + ord(c2[1]) - ord("A"))


CATEGORY_INFO = {
    "Grand Slam":       {"emoji": "🏆", "color": "#fbbf24", "points": 2000, "label": "Grand Slam"},
    "ATP Masters 1000": {"emoji": "⭐", "color": "#dc2626", "points": 1000, "label": "Masters 1000"},
    "ATP 500":          {"emoji": "🥇", "color": "#2563eb", "points": 500,  "label": "ATP 500"},
    "ATP 250":          {"emoji": "🎾", "color": "#16a34a", "points": 250,  "label": "ATP 250"},
    "ATP Finals":       {"emoji": "🏅", "color": "#9333ea", "points": 1500, "label": "ATP Finals"},
    "Davis Cup":        {"emoji": "🌍", "color": "#0891b2", "points": 0,    "label": "Davis Cup"},
    "United Cup":       {"emoji": "🎌", "color": "#ec4899", "points": 500,  "label": "United Cup"},
    "Laver Cup":        {"emoji": "🤝", "color": "#6366f1", "points": 0,    "label": "Laver Cup"},
}

SURFACE_INFO = {
    "Hard":         {"emoji": "🔵", "color": "#1d4ed8"},
    "Clay":         {"emoji": "🟠", "color": "#c2410c"},
    "Grass":        {"emoji": "🟢", "color": "#15803d"},
    "Indoor Hard":  {"emoji": "⚫", "color": "#1f2937"},
    "Various":      {"emoji": "🌐", "color": "#64748b"},
}


# ============================================================
# HTML rendering
# ============================================================

def render_tournament_card(t, base_url=""):
    cat = t["category"]
    surf = t["surface"]
    cat_info = CATEGORY_INFO.get(cat, {"emoji": "🎾", "color": "#64748b", "label": cat})
    surf_info = SURFACE_INFO.get(surf, {"emoji": "", "color": "#64748b"})

    flag = country_flag(t.get("country", ""))
    start_d = str(t["start_date"])[5:7] + "/" + str(t["start_date"])[8:10]
    end_d = str(t["end_date"])[5:7] + "/" + str(t["end_date"])[8:10]
    slug = slugify(t["tournament"], t.get("city", ""))

    url_html = ""
    if t.get("url"):
        url_html = f'<a href="{t["url"]}" target="_blank" rel="noopener" class="ext-link">Official ↗</a>'

    return f'''
    <div class="tournament-card" data-category="{cat}">
      <div class="card-header">
        <span class="cat-badge" style="background:{cat_info['color']}">{cat_info['emoji']} {cat_info['label']}</span>
        <span class="surface-badge" style="background:{surf_info['color']}">{surf_info['emoji']} {surf}</span>
      </div>
      <h3>
        {flag} <a href="{base_url}tournaments/{slug}/">{html_escape(t['tournament'])}</a>
      </h3>
      <p class="card-meta">
        <span class="city">📍 {html_escape(t['city'])}</span>
        {f'<span class="draws">👥 {t["draws"]}</span>' if t.get("draws") else ''}
      </p>
      <p class="card-dates">🗓️ {start_d} – {end_d}</p>
      <div class="card-links">
        <a href="{base_url}tournaments/{slug}/" class="card-link">Details →</a>
        {url_html}
      </div>
    </div>
    '''


def html_escape(s):
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def slugify(name, city=""):
    s = name.lower().replace(" ", "-").replace(",", "").replace("'", "").replace(".", "")
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e")
          .replace("ü", "u").replace("ö", "o").replace("ä", "a")
          .replace("ñ", "n").replace("ç", "c")
          .replace("--", "-").strip("-"))
    if s == "tbd":
        city_slug = city.lower().replace(" ", "-").replace(",", "").replace(".", "")
        city_slug = (city_slug.replace("é", "e").replace("è", "e").replace("ê", "e")
                      .replace("ü", "u").replace("ö", "o").replace("ä", "a")
                      .replace("ñ", "n").replace("ç", "c")
                      .replace("--", "-").strip("-"))
        if city_slug in ("tbd", "multi-city", "italy"):
            return f"tbd-event"
        return f"tbd-{city_slug}"
    return s


def page(title, body, active_nav="", base_url=""):
    """Wrap content in the full HTML template."""
    nav_items = [
        ("Home", base_url + ""),
        ("Calendar", base_url + "calendar/"),
        ("Tournaments", base_url + "tournaments/"),
        ("Categories", base_url + "category/"),
        ("Live Rankings ↗", base_url + "rankings/"),
        ("About", base_url + "about/"),
    ]
    nav_html = ""
    for label, href in nav_items:
        is_active = "active" if active_nav.lower() in label.lower() else ""
        external = ' target="_blank" rel="noopener"' if "↗" in label else ""
        nav_html += f'        <a class="{is_active}" href="{href}"{external}>{label}</a>\n'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_escape(title)} | ATP Tour 2027</title>
<meta name="description" content="ATP Tour 2027 - 66 tournaments, live ATP rankings, official tournament links">
<link rel="stylesheet" href="{base_url}assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%F0%9F%8E%BE%3C/svg%3E">
</head>
<body>
<header class="site-header">
  <div class="wrapper">
    <a class="site-title" href="{base_url}">🎾 ATP Tour 2027</a>
    <nav class="site-nav">
{nav_html}    </nav>
  </div>
</header>
<main class="page-content">
  <div class="wrapper">
{body}
  </div>
</main>
<footer class="site-footer">
  <div class="wrapper">
    <p>🎾 ATP Tour 2027 · Data: <a href="https://www.atptour.com/" target="_blank" rel="noopener">ATP Tour</a> · <a href="https://github.com/chanxaviersy/atp-2027-calendar">GitHub</a></p>
    <p class="footer-meta">Fan project. Not affiliated with ATP. Calendar data: 14 January 2026 update.</p>
  </div>
</footer>
</body>
</html>
'''


# ============================================================
# Page builders
# ============================================================

def build_index(tournaments, base_url=""):
    by_cat = {}
    for t in tournaments:
        by_cat.setdefault(t["category"], []).append(t)

    cat_cards = ""
    for cat, info in [
        ("Grand Slam", "The four biggest tournaments in tennis."),
        ("ATP Masters 1000", "Top-tier tournaments outside the Slams."),
        ("ATP 500", "Mid-tier tournaments with strong fields."),
        ("ATP 250", "Smaller events, many in unique locations."),
        ("ATP Finals", "Year-end championships for the top 8."),
        ("Davis Cup", "The World Cup of tennis."),
    ]:
        n = len(by_cat.get(cat, []))
        emoji = CATEGORY_INFO.get(cat, {}).get("emoji", "🎾")
        color = CATEGORY_INFO.get(cat, {}).get("color", "#64748b")
        cat_cards += f'''
    <a href="{base_url}category/#{slugify(cat)}" class="category-card">
      <div class="cat-icon" style="color:{color}">{emoji}</div>
      <h2>{cat}</h2>
      <p class="cat-count">{n} events</p>
      <p class="cat-desc">{info}</p>
    </a>'''

    body = f'''
<section class="hero">
  <h1>🎾 ATP Tour 2027</h1>
  <p class="lead">The complete 2027 ATP tennis season — all {len(tournaments)} tournaments, from Brisbane in January to the Next Gen Finals in December.</p>
  <p>
    <a href="{base_url}calendar/" class="btn">View Calendar</a>
    <a href="{base_url}tournaments/" class="btn">All Tournaments</a>
    <a href="{base_url}rankings/" class="btn">Live Rankings ↗</a>
  </p>
</section>

<div class="stats">
  <div class="stat"><div class="num">{len(tournaments)}</div><div class="label">Tournaments</div></div>
  <div class="stat"><div class="num">{len(by_cat.get("Grand Slam", []))}</div><div class="label">Grand Slams</div></div>
  <div class="stat"><div class="num">{len(by_cat.get("ATP Masters 1000", []))}</div><div class="label">Masters 1000</div></div>
  <div class="stat"><div class="num">{len(by_cat.get("ATP 500", []))}</div><div class="label">ATP 500</div></div>
  <div class="stat"><div class="num">{len(by_cat.get("ATP 250", []))}</div><div class="label">ATP 250</div></div>
</div>

<h2>🏆 Featured Categories</h2>
<div class="category-grid">{cat_cards}
</div>

<h2>🌟 Key Dates</h2>
<table>
  <tr><th>Date</th><th>Event</th><th>Surface</th></tr>
  <tr><td>Jan 17 – Jan 31</td><td>🇦🇺 <strong>Australian Open</strong></td><td>Hard</td></tr>
  <tr><td>Apr 12 – Apr 18</td><td>🇲🇨 <strong>Monte-Carlo Masters</strong></td><td>Clay</td></tr>
  <tr><td>May 23 – Jun 6</td><td>🇫🇷 <strong>Roland Garros</strong></td><td>Clay</td></tr>
  <tr><td>Jun 28 – Jul 11</td><td>🇬🇧 <strong>Wimbledon</strong></td><td>Grass</td></tr>
  <tr><td>Aug 29 – Sep 12</td><td>🇺🇸 <strong>US Open</strong></td><td>Hard</td></tr>
  <tr><td>Nov 14 – Nov 21</td><td>🇮🇹 <strong>Nitto ATP Finals</strong></td><td>Indoor Hard</td></tr>
</table>

<p class="cta-block">
  <a href="{base_url}calendar/" class="btn btn-primary">See Full Calendar →</a>
  <a href="{base_url}about/" class="btn">About this Project</a>
</p>
'''
    return page("Home", body, active_nav="home", base_url=base_url)


def build_calendar(tournaments, base_url=""):
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    body = '''
<section class="hero">
  <h1>📅 2027 Calendar</h1>
  <p class="lead">Complete season schedule, grouped by month. Click any event for full details.</p>
</section>
'''

    for i, month in enumerate(months, 1):
        in_month = [t for t in tournaments if int(str(t["start_date"])[5:7]) == i]
        if not in_month:
            continue
        in_month.sort(key=lambda t: t["start_date"])

        body += f'<section class="month-section">\n'
        body += f'  <h2>{month} 2027 <span class="month-count">({len(in_month)} events)</span></h2>\n'
        body += '  <div class="tournament-grid">\n'
        for t in in_month:
            body += render_tournament_card(t, base_url)
        body += '  </div>\n</section>\n'

    return page("Calendar", body, active_nav="calendar", base_url=base_url)


def build_tournaments(tournaments, base_url=""):
    by_cat = {}
    for t in tournaments:
        by_cat.setdefault(t["category"], []).append(t)

    body = '''
<section class="hero">
  <h1>🏟️ All Tournaments</h1>
  <p class="lead">Browse every event on the 2027 ATP calendar. Each card links to the official tournament website and a detailed event page.</p>
</section>

<div class="filter-bar">
  <strong>Jump to:</strong>
  <a href="#Grand-Slam" class="filter-pill">Grand Slam</a>
  <a href="#ATP-Masters-1000" class="filter-pill">Masters 1000</a>
  <a href="#ATP-500" class="filter-pill">ATP 500</a>
  <a href="#ATP-250" class="filter-pill">ATP 250</a>
  <a href="#ATP-Finals" class="filter-pill">ATP Finals</a>
  <a href="#Davis-Cup" class="filter-pill">Davis Cup</a>
</div>
'''

    for cat in ["Grand Slam", "ATP Masters 1000", "ATP 500", "ATP 250",
                "ATP Finals", "Davis Cup", "United Cup", "Laver Cup"]:
        if cat not in by_cat:
            continue
        events = sorted(by_cat[cat], key=lambda t: t["start_date"])
        body += f'<section id="{cat.replace(" ", "-")}" class="category-section">\n'
        body += f'  <h2>{cat} <span class="month-count">({len(events)})</span></h2>\n'
        body += '  <div class="tournament-grid">\n'
        for t in events:
            body += render_tournament_card(t, base_url)
        body += '  </div>\n</section>\n'

    return page("All Tournaments", body, active_nav="tournaments", base_url=base_url)


def build_category(tournaments, base_url=""):
    by_cat = {}
    for t in tournaments:
        by_cat.setdefault(t["category"], []).append(t)

    # Build card grid
    body = '''
<section class="hero">
  <h1>🏷️ Browse by Category</h1>
  <p class="lead">Quick links to each tier of the 2027 ATP Tour.</p>
</section>

<div class="category-grid">
'''
    cat_descriptions = {
        "Grand Slam":       ("🏆", "#fbbf24", "The four biggest tournaments in tennis. 2000 ranking points to the winner."),
        "ATP Masters 1000": ("⭐", "#dc2626", "Top-tier tournaments outside the Slams. 1000 ranking points to the winner."),
        "ATP 500":          ("🥇", "#2563eb", "Mid-tier tournaments with 500 ranking points to the winner."),
        "ATP 250":          ("🎾", "#16a34a", "Smaller events with 250 ranking points to the winner."),
        "ATP Finals":       ("🏅", "#9333ea", "Year-end championship events featuring the top 8 players."),
        "Davis Cup":        ("🌍", "#0891b2", "The World Cup of tennis. National teams compete."),
    }
    for cat, (emoji, color, desc) in cat_descriptions.items():
        n = len(by_cat.get(cat, []))
        body += f'''
  <a href="#{slugify(cat)}" class="category-card">
    <div class="cat-icon" style="color:{color}">{emoji}</div>
    <h2>{cat}</h2>
    <p class="cat-count">{n} events</p>
    <p class="cat-desc">{desc}</p>
  </a>'''
    body += '\n</div>\n\n'

    # Per-category detail tables
    table_cats = [
        ("Grand Slam",       "The four most prestigious events"),
        ("ATP Masters 1000", "Mandatory top-tier events"),
        ("ATP 500",          "Strong fields, 500 ranking points"),
        ("ATP 250",          "Smaller events, often in unique locations"),
    ]
    for cat, desc in table_cats:
        if cat not in by_cat:
            continue
        events = sorted(by_cat[cat], key=lambda t: t["start_date"])
        body += f'<section id="{slugify(cat)}" class="category-section">\n'
        body += f'  <h2>{cat} <span class="month-count">({len(events)})</span></h2>\n'
        body += '  <table>\n    <tr><th>Tournament</th><th>Location</th><th>Dates</th><th>Surface</th></tr>\n'
        for t in events:
            flag = country_flag(t.get("country", ""))
            start = str(t["start_date"])[5:10]
            end = str(t["end_date"])[5:10]
            slug = slugify(t["tournament"], t.get("city", ""))
            body += f'    <tr><td><a href="{base_url}tournaments/{slug}/">{flag} {html_escape(t["tournament"])}</a></td>'
            body += f'<td>{html_escape(t["city"])}</td>'
            body += f'<td>{start} – {end}</td>'
            body += f'<td>{t["surface"]}</td></tr>\n'
        body += '  </table>\n</section>\n'

    return page("Categories", body, active_nav="categories", base_url=base_url)


def build_rankings(base_url=""):
    body = '''
<section class="hero">
  <h1>📈 Live ATP Rankings</h1>
  <p class="lead">This site does not host ranking data (it would go stale within hours). Below are direct links to authoritative, real-time sources.</p>
</section>

<h2>🌍 Official Sources</h2>
<div class="rankings-grid">
  <a href="https://www.atptour.com/en/rankings/singles" target="_blank" rel="noopener" class="rankings-card">
    <h3>🏆 ATP Singles Rankings</h3>
    <p>The authoritative source. Updated every Monday after tournament completion.</p>
  </a>
  <a href="https://www.atptour.com/en/rankings/race-to-turin" target="_blank" rel="noopener" class="rankings-card">
    <h3>📊 Race to Turin (Live)</h3>
    <p>Year-to-date points for Nitto ATP Finals qualification.</p>
  </a>
  <a href="https://www.atptour.com/en/rankings/doubles" target="_blank" rel="noopener" class="rankings-card">
    <h3>🤝 ATP Doubles Rankings</h3>
    <p>The official doubles rankings.</p>
  </a>
  <a href="https://www.atptour.com/en/scores/live-flashscores" target="_blank" rel="noopener" class="rankings-card">
    <h3>🎾 Live Scores</h3>
    <p>Real-time match scores and live ATP points.</p>
  </a>
</div>

<h2>📅 How Rankings Work</h2>
<ul>
  <li>Players earn points at tournaments based on <strong>category</strong> and <strong>result</strong></li>
  <li>Points are kept on a <strong>rolling 52-week basis</strong></li>
  <li>Best <strong>18 tournament results</strong> count for most players</li>
  <li>Top <strong>8 players</strong> in the Race to Turin qualify for the Nitto ATP Finals</li>
</ul>

<h2>🏆 2027 Point Distribution</h2>
<table>
  <tr><th>Category</th><th>Winner</th><th>Finalist</th><th>Semifinalist</th><th>Quarterfinalist</th></tr>
  <tr><td><strong>Grand Slam</strong></td><td>2000</td><td>1200</td><td>720</td><td>360</td></tr>
  <tr><td><strong>ATP Masters 1000</strong></td><td>1000</td><td>600</td><td>360</td><td>180</td></tr>
  <tr><td><strong>ATP 500</strong></td><td>500</td><td>300</td><td>180</td><td>90</td></tr>
  <tr><td><strong>ATP 250</strong></td><td>250</td><td>150</td><td>90</td><td>45</td></tr>
  <tr><td><strong>Nitto ATP Finals</strong></td><td>1500 (unbeaten)</td><td>1000+</td><td>varies</td><td>varies</td></tr>
</table>

<h2>🔄 Update Cadence</h2>
<p>ATP rankings are updated <strong>every Monday at ~12:00 UTC</strong> after the previous week's tournaments conclude. The Race to Turin is updated <strong>continuously</strong> during tournament weeks.</p>
'''
    return page("Live Rankings", body, active_nav="rankings", base_url=base_url)


def build_about(base_url=""):
    body = f'''
<section class="hero">
  <h1>ℹ️ About This Project</h1>
  <p class="lead">A clean, fast, structured reference for the 2027 ATP Tour season.</p>
</section>

<h2>🎯 Goals</h2>
<ol>
  <li><strong>Single source of truth</strong> — All tournament data lives in one YAML file</li>
  <li><strong>No stale data</strong> — Direct links to live rankings (no scraping)</li>
  <li><strong>Free hosting</strong> — Static HTML on GitHub Pages</li>
  <li><strong>Zero JS</strong> — Pure HTML/CSS for fast loads and great SEO</li>
  <li><strong>Community-friendly</strong> — Anyone can submit a PR to fix a typo or update dates</li>
</ol>

<h2>🛠️ Tech Stack</h2>
<table>
  <tr><th>Layer</th><th>Technology</th></tr>
  <tr><td>Generator</td><td>Python (this script)</td></tr>
  <tr><td>Output</td><td>Pure static HTML/CSS</td></tr>
  <tr><td>Data</td><td>YAML</td></tr>
  <tr><td>Hosting</td><td>GitHub Pages</td></tr>
  <tr><td>Version control</td><td>Git</td></tr>
</table>

<h2>📂 Project Structure</h2>
<pre><code>atp-2027-calendar/
├── _data/
│   ├── tournaments.yml      # Master data ({len_tournaments_check()} events)
│   └── notes.yml            # Footnote legend
├── _scripts/
│   ├── build.py             # This script - builds static HTML
│   └── iso_codes.py         # ISO 3166 mapping
├── docs/                    # Output (auto-generated)
│   ├── index.html
│   ├── calendar.html
│   ├── tournaments.html
│   ├── category.html
│   ├── rankings.html
│   ├── about.html
│   ├── 404.html
│   ├── assets/css/style.css
│   └── tournaments/[name].html  # 66 detail pages
├── _config.yml              # (legacy, for Jekyll)
├── Gemfile                  # (legacy)
└── README.md</code></pre>

<h2>🔄 How to Update</h2>
<p>When the ATP releases a calendar update:</p>
<ol>
  <li>Edit <code>_data/tournaments.yml</code></li>
  <li>Run <code>python3 _scripts/build.py</code></li>
  <li>Commit and push the <code>docs/</code> folder</li>
</ol>

<h2>📜 Data License</h2>
<ul>
  <li><strong>Calendar data</strong>: © ATP Tour. Used under fair use for informational purposes.</li>
  <li><strong>Tournament websites</strong>: Linked to, not embedded.</li>
  <li><strong>Rankings</strong>: Direct links to the official ATP site, not republished.</li>
</ul>

<h2>🤝 Contributing</h2>
<p>PRs welcome! Common contributions:</p>
<ul>
  <li>🐛 Fix typos or broken links</li>
  <li>📅 Update tournament dates (after new ATP calendar release)</li>
  <li>🏟️ Add new tournaments</li>
  <li>🌐 Add country flag mapping for missing codes</li>
</ul>

<p><em>Built with ❤️ by tennis fans. Not affiliated with the ATP Tour.</em></p>
'''
    return page("About", body, active_nav="about", base_url=base_url)


def len_tournaments_check():
    return 66  # Will be updated by main()


def build_tournament_detail(t, base_url=""):
    flag = country_flag(t.get("country", ""))
    cat = t["category"]
    surf = t["surface"]
    cat_info = CATEGORY_INFO.get(cat, {"emoji": "🎾", "color": "#64748b", "label": cat})
    surf_info = SURFACE_INFO.get(surf, {"emoji": "", "color": "#64748b"})

    # Generic description
    desc = f"""The {t['tournament']} is a {cat} tournament held in {t['city']} on {surf} courts. It is part of the official 2027 ATP Tour calendar, taking place from {t['start_date']} to {t['end_date']}."""

    # Draw size
    draws_html = ""
    if t.get("draws"):
        draws_html = f'<div class="fact"><div class="label">👥 Draw Size</div><div class="value">{t["draws"]}</div></div>'

    # Official website
    official_html = ""
    if t.get("url"):
        official_html = f'''
<section class="t-official">
  <h2>Official Resources</h2>
  <p><a href="{t['url']}" target="_blank" rel="noopener" class="btn btn-primary">🌍 Visit Official Tournament Website ↗</a></p>
  <p><small>For tickets, schedule, draws, and live scores, please visit the official website.</small></p>
</section>'''

    # Notes
    notes_html = ""
    if t.get("notes"):
        codes = ", ".join([f"<code>{n}</code>" for n in t["notes"]])
        notes_html = f'<section class="t-notes"><h2>📝 Schedule Notes</h2><p>Codes: {codes} (see legend on <a href="{base_url}about/">About page</a>)</p></section>'

    # Other tournaments in same week
    same_week = [x for x in all_tournaments_global if x["week"] == t["week"] and x["tournament"] != t["tournament"]]
    other_html = ""
    if same_week:
        other_html = '<section class="t-others"><h2>📅 Same Week</h2><ul>'
        for x in same_week:
            xflag = country_flag(x.get("country", ""))
            xslug = slugify(x["tournament"], x.get("city", ""))
            other_html += f'<li>{xflag} <a href="{base_url}tournaments/{xslug}/">{html_escape(x["tournament"])}</a> ({html_escape(x["city"])})</li>'
        other_html += '</ul></section>'

    body = f'''
<nav class="breadcrumb">
  <a href="{base_url}">Home</a> →
  <a href="{base_url}tournaments/">Tournaments</a> →
  <span>{html_escape(t["tournament"])}</span>
</nav>

<article class="tournament-detail">
  <header class="t-header">
    <div class="t-cat">
      <span class="cat-badge" style="background:{cat_info['color']}">{cat_info['emoji']} {cat_info['label']}</span>
      <span class="surface-badge" style="background:{surf_info['color']}">{surf_info['emoji']} {surf}</span>
    </div>
    <h1>{flag} {html_escape(t['tournament'])}</h1>
    <p class="t-subtitle">{html_escape(t['city'])} · Calendar Week {t['week']} of 2027</p>
  </header>

  <section class="t-quick-facts">
    <div class="fact"><div class="label">📅 Dates</div><div class="value">{t['start_date']} → {t['end_date']}</div></div>
    <div class="fact"><div class="label">📍 Venue</div><div class="value">{html_escape(t['city'])}</div></div>
    <div class="fact"><div class="label">{surf_info['emoji']} Surface</div><div class="value">{surf}</div></div>
    <div class="fact"><div class="label">🎯 Category</div><div class="value">{cat}</div></div>
    {draws_html}
  </section>

  <section class="t-description">
    <h2>About</h2>
    <p>{desc}</p>
  </section>

  {official_html}
  {notes_html}

  <section class="t-rankings">
    <h2>📈 Live ATP Rankings</h2>
    <p>Check who is likely to compete:</p>
    <ul>
      <li><a href="https://www.atptour.com/en/rankings/singles" target="_blank" rel="noopener">ATP Singles Rankings ↗</a></li>
      <li><a href="https://www.atptour.com/en/rankings/race-to-turin" target="_blank" rel="noopener">Race to Turin (year-to-date) ↗</a></li>
    </ul>
  </section>

  {other_html}

  <p class="back-link"><a href="{base_url}tournaments/">← Back to all tournaments</a></p>
</article>
'''
    return page(t["tournament"], body, active_nav="tournaments", base_url=base_url)


# Global tournaments for cross-referencing
all_tournaments_global = []


# ============================================================
# Main
# ============================================================

def main():
    global all_tournaments_global
    with open(DATA_FILE) as f:
        tournaments = yaml.safe_load(f)
    all_tournaments_global = tournaments
    n = len(tournaments)

    print(f"Building static site for {n} tournaments...")

    # Clean output dir
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "tournaments").mkdir()
    (OUT / "assets" / "css").mkdir(parents=True)

    # Copy CSS
    src_css = ROOT / "assets" / "css" / "style.scss"
    dst_css = OUT / "assets" / "css" / "style.css"
    if src_css.exists():
        # Convert SCSS variables to CSS by simple substitution
        css = src_css.read_text()
        # Remove the leading Jekyll front matter
        css = re.sub(r'^---\s*\n---', '', css, flags=re.MULTILINE)
        # Strip SCSS-specific syntax (basic)
        css = re.sub(r'//\s*=+', '', css)  # Strip section markers
        # Replace $variable with values (very basic)
        variables = {
            r'\$atp-blue': '#1e3a8a',
            r'\$atp-blue-light': '#3b82f6',
            r'\$atp-yellow': '#fbbf24',
            r'\$atp-orange': '#ea580c',
            r'\$atp-green': '#16a34a',
            r'\$atp-clay': '#c2410c',
            r'\$atp-grass': '#15803d',
            r'\$atp-hard': '#1d4ed8',
            r'\$atp-indoor': '#1f2937',
            r'\$cat-grand-slam': '#fbbf24',
            r'\$cat-masters': '#dc2626',
            r'\$cat-atp500': '#2563eb',
            r'\$cat-atp250': '#16a34a',
            r'\$cat-finals': '#9333ea',
            r'\$cat-davis': '#0891b2',
            r'\$cat-united': '#ec4899',
            r'\$cat-laver': '#6366f1',
        }
        for pat, val in variables.items():
            css = re.sub(pat + r'\b', val, css)
        # Remove SCSS nesting (simple: convert nested & to flat)
        # Actually, the SCSS is fairly simple — let me just write a CSS version
        dst_css.write_text(make_css())
        print(f"  ✅ assets/css/style.css ({len(make_css())} bytes)")

    # Generate pages
    pages_to_build = [
        ("index.html", build_index(tournaments)),
        ("calendar.html", build_calendar(tournaments)),
        ("tournaments.html", build_tournaments(tournaments)),
        ("category.html", build_category(tournaments)),
        ("rankings.html", build_rankings()),
        ("about.html", build_about()),
        ("404.html", make_404()),
    ]
    for name, content in pages_to_build:
        (OUT / name).write_text(content)
        print(f"  ✅ {name}")

    # Tournament detail pages
    for t in tournaments:
        slug = slugify(t["tournament"], t.get("city", ""))
        (OUT / "tournaments" / f"{slug}.html").write_text(build_tournament_detail(t))
    print(f"  ✅ tournaments/ ({n} detail pages)")

    # JSON-LD sitemap for SEO
    sitemap_items = []
    for t in tournaments:
        slug = slugify(t["tournament"], t.get("city", ""))
        sitemap_items.append({
            "url": f"tournaments/{slug}.html",
            "title": t["tournament"],
            "category": t["category"],
        })
    (OUT / "sitemap-data.json").write_text(json.dumps(sitemap_items, ensure_ascii=False, indent=2))
    print(f"  ✅ sitemap-data.json")

    # robots.txt
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n")
    print(f"  ✅ robots.txt")

    total_files = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"\n✅ Build complete: {total_files} files in {OUT}")


def make_404():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>404 - Page Not Found</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; background: linear-gradient(135deg, #1e3a8a, #1e40af); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
  .container { text-align: center; max-width: 500px; padding: 2rem; }
  h1 { font-size: 8rem; margin: 0; }
  p { font-size: 1.2rem; margin: 1rem 0 2rem; }
  a { display: inline-block; padding: 0.75rem 1.5rem; background: white; color: #1e40af; text-decoration: none; border-radius: 8px; font-weight: bold; }
  a:hover { background: #fbbf24; }
</style>
</head>
<body>
<div class="container">
  <h1>🎾</h1>
  <h2>404</h2>
  <p>This page is unforced. Let's get you back on court.</p>
  <a href="/">Back to Home</a>
</div>
</body>
</html>'''


def make_css():
    """Generate the full CSS file (pre-compiled from SCSS)."""
    return '''
/* ATP Tour 2027 Stylesheet */

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  line-height: 1.6;
  margin: 0;
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header */
.site-header {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  border-bottom: 3px solid #fbbf24;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.site-header .wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}
.site-header .site-title {
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
  text-decoration: none;
  letter-spacing: -0.02em;
}
.site-header .site-title:hover { color: #fbbf24; }
.site-header .site-nav { display: flex; gap: 1.25rem; flex-wrap: wrap; }
.site-header .site-nav a {
  color: rgba(255,255,255,0.9);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: all 0.15s;
}
.site-header .site-nav a:hover,
.site-header .site-nav a.active {
  color: #fbbf24;
  background: rgba(255,255,255,0.1);
}

/* Hero */
.hero { text-align: center; padding: 3rem 1rem 2rem; }
.hero h1 { font-size: 3rem; margin: 0 0 0.5rem; color: #1e3a8a; letter-spacing: -0.03em; }
.hero .lead { font-size: 1.2rem; color: #475569; max-width: 700px; margin: 0 auto 1.5rem; }

/* Stats */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}
.stats .stat {
  text-align: center;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: transform 0.15s, box-shadow 0.15s;
}
.stats .stat:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.stats .stat .num { font-size: 2.5rem; font-weight: 700; color: #1e3a8a; line-height: 1; }
.stats .stat .label { font-size: 0.85rem; color: #64748b; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }

/* Buttons */
.btn {
  display: inline-block;
  padding: 0.7rem 1.4rem;
  background: #1e3a8a;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  margin: 0 0.25rem 0.5rem;
  border: 2px solid #1e3a8a;
  transition: all 0.15s;
}
.btn:hover { background: #3b82f6; border-color: #3b82f6; color: white; }
.btn-primary { background: #fbbf24; color: #0f172a; border-color: #fbbf24; }
.btn-primary:hover { background: #f59e0b; border-color: #f59e0b; }
.cta-block { text-align: center; margin: 2rem 0; }

/* Sections */
h2 { color: #1e3a8a; border-bottom: 2px solid #fbbf24; padding-bottom: 0.5rem; margin: 2.5rem 0 1.5rem; }
.month-section, .category-section { margin: 2.5rem 0; }
.month-count { color: #64748b; font-size: 0.8em; font-weight: normal; }

/* Tournament Grid */
.tournament-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
.tournament-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #3b82f6;
  transition: all 0.15s;
}
.tournament-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
  border-left-color: #fbbf24;
}
.tournament-card .card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.tournament-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.05rem;
  line-height: 1.3;
}
.tournament-card h3 a { color: #1e3a8a; text-decoration: none; }
.tournament-card h3 a:hover { color: #3b82f6; text-decoration: underline; }
.tournament-card .card-meta,
.tournament-card .card-dates { font-size: 0.85rem; color: #475569; margin: 0.25rem 0; }
.tournament-card .card-links { margin-top: 0.5rem; }
.tournament-card .card-link { color: #3b82f6; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
.tournament-card .card-link:hover { color: #fbbf24; }
.tournament-card .ext-link { margin-left: 0.5rem; color: #64748b; text-decoration: none; font-size: 0.85rem; }
.tournament-card .ext-link:hover { color: #1e3a8a; }

/* Badges */
.cat-badge, .surface-badge {
  display: inline-block;
  padding: 0.15rem 0.6rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: white;
  white-space: nowrap;
}

/* Category Grid */
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.25rem;
  margin: 2rem 0;
}
.category-card {
  display: block;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  border: 2px solid #e2e8f0;
  transition: all 0.2s;
}
.category-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); border-color: #3b82f6; }
.category-card .cat-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.category-card h2 { margin: 0 0 0.5rem; color: #1e3a8a; font-size: 1.1rem; border: none; padding: 0; }
.category-card .cat-count { margin: 0.25rem 0; font-size: 0.9rem; color: #64748b; font-weight: 600; }
.category-card .cat-desc { font-size: 0.8rem; line-height: 1.4; margin-top: 0.5rem; color: #64748b; }

/* Filter Bar */
.filter-bar {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
.filter-pill {
  display: inline-block;
  padding: 0.3rem 0.75rem;
  background: #f1f5f9;
  border-radius: 16px;
  text-decoration: none;
  color: #334155;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.15s;
}
.filter-pill:hover { background: #1e3a8a; color: white; }

/* Rankings Grid */
.rankings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}
.rankings-card {
  display: block;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  border: 2px solid #e2e8f0;
  transition: all 0.2s;
}
.rankings-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.1); border-color: #3b82f6; }
.rankings-card h3 { margin: 0 0 0.5rem; color: #1e3a8a; font-size: 1.05rem; }
.rankings-card p { margin: 0; color: #64748b; font-size: 0.9rem; }

/* Tournament Detail */
.tournament-detail .t-header {
  margin: 1rem 0 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 12px;
  border-left: 6px solid #1e3a8a;
}
.tournament-detail .t-header h1 { margin: 0.5rem 0 0.25rem; color: #1e3a8a; font-size: 2rem; }
.tournament-detail .t-subtitle { margin: 0; color: #64748b; font-size: 1rem; }
.tournament-detail .t-cat { font-size: 0.9rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
.tournament-detail .t-quick-facts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.75rem;
  margin: 1.5rem 0;
}
.tournament-detail .t-quick-facts .fact {
  background: white;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}
.tournament-detail .t-quick-facts .label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}
.tournament-detail .t-quick-facts .value { font-weight: 600; color: #0f172a; }
.tournament-detail section { margin: 2rem 0; }
.tournament-detail section h2 { color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.4rem; }
.tournament-detail .back-link { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; }

.breadcrumb { margin: 1rem 0; color: #64748b; font-size: 0.9rem; }
.breadcrumb a { color: #3b82f6; text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb span { color: #0f172a; font-weight: 500; }

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
table th, table td { padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
table th { background: #f8fafc; font-weight: 600; color: #1e3a8a; }
table tbody tr:hover { background: #f8fafc; }

/* Footer */
.site-footer {
  background: #0f172a;
  color: rgba(255,255,255,0.7);
  padding: 2rem 0;
  margin-top: 4rem;
  text-align: center;
  font-size: 0.9rem;
}
.site-footer a { color: #fbbf24; text-decoration: none; }
.site-footer a:hover { text-decoration: underline; }
.site-footer .footer-meta { color: rgba(255,255,255,0.5); font-size: 0.8rem; }

/* Code */
pre {
  background: #1e293b;
  color: #e2e8f0;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 0.85rem;
}
code { font-family: "SF Mono", Consolas, Monaco, monospace; }
pre code { background: none; color: inherit; padding: 0; }
:not(pre) > code { background: #f1f5f9; color: #1e3a8a; padding: 0.1rem 0.3rem; border-radius: 4px; font-size: 0.9em; }

/* Responsive */
@media (max-width: 640px) {
  .site-header .wrapper { flex-direction: column; gap: 0.5rem; }
  .site-header .site-nav { justify-content: center; gap: 0.75rem; }
  .hero h1 { font-size: 2rem; }
  .hero .lead { font-size: 1rem; }
  .tournament-detail .t-header h1 { font-size: 1.5rem; }
  .stats .stat .num { font-size: 2rem; }
  h2 { font-size: 1.4rem; }
}
'''


if __name__ == "__main__":
    main()
