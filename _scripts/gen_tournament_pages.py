#!/usr/bin/env python3
"""Auto-generate per-tournament detail pages from tournaments.yml"""

import yaml
import os
from pathlib import Path


# Detailed descriptions for the most famous tournaments
DESCRIPTIONS = {
    "Australian Open": "The first Grand Slam of the year, held annually at Melbourne Park. Played on hard courts (Plexicushion/GreenSet), the tournament features 128-player singles draws and is known for its extreme summer heat, which often leads to dramatic matches. The 2027 edition marks the 50th anniversary of the Open Era at the Australian Open.",
    "Roland Garros": "The second Grand Slam of the year and the most prestigious clay court tournament in the world. Held at Stade Roland-Garros in Paris, it features 128-player singles draws. The 2027 edition will be the first Roland Garros played under the retractable roof on Court Philippe-Chatrier in its final configuration.",
    "The Championships, Wimbledon": "The oldest tennis tournament in the world (founded 1877) and the third Grand Slam of the year. Played on grass courts at the All England Lawn Tennis Club, London. Famous for its strict all-white dress code, strawberries and cream, and the absence of on-court advertising.",
    "US Open": "The fourth and final Grand Slam of the year, held at the USTA Billie Jean King National Tennis Center in Flushing Meadows, New York. The only Grand Slam played with a final-set tiebreak (at 6-6). Known for its rowdy night sessions and Arthur Ashe Stadium (the largest tennis venue in the world).",
    "BNP Paribas Open": "Often called the 'fifth Slam' due to its prestige and massive attendance. Held in Indian Wells, California, it is the largest combined ATP/WTA tournament in the world, with a 96-player singles draw. The 2027 edition features a new retractable roof on Stadium 1.",
    "Miami Open presented by Itaú": "The second of the 'Sunshine Double' Masters 1000 events. Held at Hard Rock Stadium in Miami Gardens, the tournament features a 96-player singles draw and is one of the most-attended tennis events globally.",
    "Rolex Monte-Carlo Masters": "The first clay court Masters 1000 of the season, held at the Monte-Carlo Country Club in Roquebrune-Cap-Martin, Monaco. Famous for its stunning cliffside location overlooking the Mediterranean Sea.",
    "Mutua Madrid Open": "The fourth Masters 1000 of the season, held at the Caja Mágica in Madrid. Known for its distinctive 'moving roof' architecture and high altitude (660m), which makes the ball travel faster.",
    "Internazionali BNL d'Italia": "The fifth and final clay court Masters 1000 before Roland Garros. Held at the Foro Italico in Rome, the tournament's historic Stadio Centrale (now Stadio Nicola Pietrangeli) has hosted countless memorable matches.",
    "National Bank Open presented by Rogers": "The Canadian Masters 1000, alternating annually between Toronto and Montreal. The 2027 edition returns to Toronto. The only ATP Masters 1000 held in Canada.",
    "Cincinnati Open": "Often called the 'Western & Southern Open' (its former sponsor name), this is the oldest tennis tournament in the US still played in its original city (founded 1899). Now held at the Lindner Family Tennis Center in Mason, Ohio.",
    "Rolex Shanghai Masters": "The only Masters 1000 held in China, and the only one played in Asia. Features a 96-player draw and is part of the Asian swing in October.",
    "Rolex Paris Masters": "The final Masters 1000 of the year, held at Bercy (Accor Arena) in Paris. Often called the 'indoor Masters' as it is the only one played on indoor hard courts. A strong performance here is critical for qualifying for the Nitto ATP Finals.",
    "Nitto ATP Finals": "The year-end championship featuring the top 8 singles players and top 8 doubles teams of the ATP Race. The format is round-robin within two groups of 4, followed by semifinals and a final. The 2027 edition returns to Italy after a multi-year run in Turin.",
    "Davis Cup": "The 'World Cup of tennis' — the largest annual international team competition in sport. 16 nations compete in the Qualifiers, with 8 teams advancing to the Finals. The Finals are held over one week in late November.",
    "Laver Cup": "An annual team competition between Team Europe and Team World, founded in 2017 by Roger Federer's management company. Inspired by the Ryder Cup in golf, it features 6 players per team competing over 3 days.",
    "United Cup": "A mixed-team event that launched in 2023, replacing the ATP Cup. Held in Sydney and Perth, it features 18 countries competing in a combined men's/women's format, with ATP, WTA, and ITF ranking points at stake.",
    "Next Gen ATP Finals": "The year-end championship for the top 8 players aged 20 and under. Known for its experimental rules: first-to-4-games sets, no-ad scoring, no lets on serve, and a shot clock. Often called a 'laboratory' for future ATP rule changes.",
    "Boss Open": "An ATP 250 grass court tournament held in Stuttgart, Germany, the week before Wimbledon. A key Wimbledon warm-up event.",
    "Libema Open": "An ATP 250 grass court tournament held in 's-Hertogenbosch, Netherlands. The only grass court event held in the Netherlands.",
    "HSBC Championships": "Held at the Queen's Club in London, this ATP 500 grass court tournament is considered the most prestigious Wimbledon warm-up. Past champions include Andy Murray, Novak Djokovic, and Rafael Nadal.",
    "Terra Wortmann Open": "A prestigious ATP 500 grass court tournament held in Halle, Germany. Roger Federer has won the title 10 times, more than any other player.",
    "Lexus Eastbourne Open": "An ATP 250 grass court tournament held in Eastbourne, England. The final major grass court warm-up before Wimbledon.",
    "Vanda Pharmaceuticals Mallorca Championships": "A relatively new ATP 250 grass court event, held in Santa Ponsa, Mallorca, Spain. Launched in 2021.",
    "China Open": "An ATP 500 hard court tournament held at the National Tennis Center in Beijing. The premier tennis event in China, held during China's National Day 'Golden Week' holiday.",
    "Kinoshita Group Japan Open Tennis Championships": "Japan's most prestigious tennis tournament, an ATP 500 event held at the Ariake Tennis Park in Tokyo. Known for its passionate local fans.",
    "Erste Bank Open": "A prestigious ATP 500 indoor hard court tournament held in Vienna, Austria. One of the most successful indoor events in Europe.",
    "Swiss Indoors Basel": "An ATP 500 indoor hard court tournament held in Basel, Switzerland. Roger Federer's hometown tournament — he won it 10 times.",
    "BNP Paribas Nordic Open": "An ATP 250 indoor hard court event in Stockholm, Sweden. The oldest indoor tennis tournament in the world (founded 1969).",
    "Chengdu Open": "An ATP 250 hard court tournament held in Chengdu, China. One of three ATP events held in China during the Asian swing.",
    "Hangzhou Open": "An ATP 250 hard court tournament held in Hangzhou, China. A newer addition to the ATP calendar, launched in 2023.",
    "Brisbane International presented by ANZ": "An ATP 250 hard court tournament held in Brisbane, Australia. The first event of the Australian summer swing, traditionally used by top players as a warm-up for the Australian Open.",
    "Adelaide International": "An ATP 250 hard court tournament held in Adelaide, Australia. Often features the deepest field of any Australian Open warm-up.",
    "ASB Classic": "An ATP 250 hard court tournament held in Auckland, New Zealand. The southern hemisphere's first event of the year.",
    "Bank of China Hong Kong Tennis Open": "An ATP 250 hard court tournament held in Hong Kong. The only ATP event in Hong Kong.",
    "Qatar ExxonMobil Open": "An ATP 250 hard court tournament held in Doha, Qatar. Has hosted many former world No. 1s in recent years.",
    "Dubai Duty Free Tennis Championships": "An ATP 500 hard court tournament held in Dubai, UAE. The Middle East's most prestigious tennis event.",
    "Open Occitanie": "An ATP 250 indoor hard court tournament held in Montpellier, France. The first European indoor event of the year.",
    "NEXO Dallas Open": "An ATP 500 indoor hard court tournament held in Dallas, Texas. A newer addition to the ATP calendar (launched 2023).",
    "ABN AMRO Open": "An ATP 500 indoor hard court tournament held in Rotterdam, Netherlands. The Netherlands' most prestigious tennis event.",
    "Rio Open presented by Claro": "An ATP 500 clay court tournament held in Rio de Janeiro, Brazil. The only ATP event in South America.",
    "Abierto Mexicano Telcel presentado por HSBC": "An ATP 500 hard court tournament held in Acapulco, Mexico. Famous for its night sessions at the Arena Parque Libaneses.",
    "IEB+ Argentina Open": "An ATP 250 clay court tournament held in Buenos Aires, Argentina. The first South American clay event of the year.",
    "Delray Beach Open": "An ATP 250 hard court tournament held in Delray Beach, Florida. The only ATP event on Florida's Atlantic coast (Miami is on the southeast).",
    "BCI Seguros Chile Open": "An ATP 250 clay court tournament held in Santiago, Chile. The second South American clay event of the year.",
    "Tiriac Open": "An ATP 250 clay court tournament held in Bucharest, Romania. Named after Romanian tennis legend Ion Tiriac.",
    "Grand Prix Hassan II": "An ATP 250 clay court tournament held in Marrakech, Morocco. The only ATP event in Africa.",
    "Fayez Sarofim & Co. U.S. Men's Clay Court Championship": "An ATP 250 clay court tournament held in Houston, Texas. The only ATP clay court event in the United States.",
    "BMW Open by Bitpanda": "An ATP 500 clay court tournament held in Munich, Germany. A key European clay court warm-up.",
    "Barcelona Open Banc Sabadell": "An ATP 500 clay court tournament held at the Real Club de Tenis Barcelona. One of the most historic clay court events in the world, founded in 1953. Rafael Nadal won it 12 times.",
    "Gonet Geneva Open": "An ATP 250 clay court tournament held in Geneva, Switzerland. A newer event (relaunched 2015).",
    "Hamburg Open": "An ATP 500 clay court tournament held at the Rothenbaum Tennis Center in Hamburg. Once a Masters event (until 2008), now an ATP 500.",
    "Mubadala Citi DC Open": "An ATP 500 hard court tournament held in Washington, D.C. The only ATP 500 in the Washington/Baltimore area, serving as a key US Open hard court warm-up.",
    "Mifel Tennis Open by Telcel Oppo": "An ATP 250 hard court tournament held in Los Cabos, Mexico. A newer event (launched 2016).",
    "Winston-Salem Open": "An ATP 250 hard court tournament held in Winston-Salem, North Carolina. The final hard court warm-up before the US Open.",
    "Nordea Open": "An ATP 250 clay court tournament held in Båstad, Sweden. The largest tennis event in Scandinavia.",
    "EFG Swiss Open Gstaad": "An ATP 250 clay court tournament held in Gstaad, Switzerland. A picturesque mountain resort tournament.",
    "Millennium Estoril Open": "An ATP 250 clay court tournament held in Estoril, Portugal. The only ATP clay event in Portugal.",
    "Plava Laguna Croatia Open Umag": "An ATP 250 clay court tournament held in Umag, Croatia. The largest tennis event in Croatia.",
    "Generali Open": "An ATP 250 clay court tournament held in Kitzbühel, Austria. Held in the scenic Tyrolean Alps.",
    "Grand Prix Auvergne-Rhône-Alpes": "An ATP 250 indoor hard court tournament held in Lyon, France. A key Paris Masters warm-up.",
    "BNP Paribas Fortis European Open": "An ATP 250 indoor hard court tournament held in Brussels, Belgium.",
    "Almaty Open": "An ATP 250 indoor hard court tournament held in Almaty, Kazakhstan. A newer event (launched 2020).",
}


def get_description(t):
    """Return a detailed description for the tournament, or a generic one."""
    name = t["tournament"]
    if name in DESCRIPTIONS:
        return DESCRIPTIONS[name]
    # Generic description
    surface = t["surface"]
    city = t["city"]
    cat = t["category"]
    return f"An {cat} tournament held in {city} on {surface} courts. Part of the 2027 ATP Tour calendar."


def country_flag(code):
    """Convert ISO 3166-1 alpha-3 country code to emoji flag (2 Regional Indicators)."""
    try:
        from iso_codes import ALPHA3_TO_ALPHA2
    except ImportError:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        from iso_codes import ALPHA3_TO_ALPHA2
    if not code or code not in ALPHA3_TO_ALPHA2:
        return "🌐"
    code2 = ALPHA3_TO_ALPHA2[code]
    if not code2:
        return "🌐"
    return chr(0x1F1E6 + ord(code2[0]) - ord("A")) + chr(0x1F1E6 + ord(code2[1]) - ord("A"))


def category_emoji(cat):
    return {
        "Grand Slam": "🏆",
        "ATP Masters 1000": "⭐",
        "ATP 500": "🥇",
        "ATP 250": "🎾",
        "ATP Finals": "🏅",
        "Davis Cup": "🌍",
        "United Cup": "🎌",
        "Laver Cup": "🤝",
    }.get(cat, "🎾")


def surface_emoji(s):
    return {
        "Hard": "🔵",
        "Clay": "🟠",
        "Grass": "🟢",
        "Indoor Hard": "⚫",
        "Various": "🌐",
    }.get(s, "")


def main():
    base = Path("/Users/xavierchan/Documents/atp-2027-calendar")
    data_path = base / "_data" / "tournaments.yml"
    out_dir = base / "tournaments"
    out_dir.mkdir(exist_ok=True)

    with open(data_path) as f:
        tournaments = yaml.safe_load(f)

    print(f"Generating {len(tournaments)} tournament pages...")

    for t in tournaments:
        # Slug from tournament name; fall back to city if name is generic ("TBD")
        base_slug = t["tournament"].lower().replace(" ", "-").replace(",", "").replace("'", "").replace(".", "")
        base_slug = (base_slug
                .replace("é", "e").replace("è", "e").replace("ê", "e")
                .replace("ü", "u").replace("ö", "o").replace("ä", "a")
                .replace("ñ", "n").replace("ç", "c")
                .replace("--", "-").strip("-"))
        # Disambiguate "TBD" entries
        if base_slug == "tbd":
            city_slug = t["city"].lower().replace(" ", "-").replace(",", "").replace(".", "")
            city_slug = (city_slug
                    .replace("é", "e").replace("è", "e").replace("ê", "e")
                    .replace("ü", "u").replace("ö", "o").replace("ä", "a")
                    .replace("ñ", "n").replace("ç", "c")
                    .replace("--", "-").strip("-"))
            if city_slug == "tbd" or city_slug == "multi-city" or city_slug == "italy":
                # Use month + category for uniqueness
                month = str(t["start_date"])[5:7]
                base_slug = f"tbd-{t['category'].lower().replace(' ', '-')}-{month}"
            else:
                base_slug = "tbd-" + city_slug
        slug = base_slug
        out = out_dir / f"{slug}.md"

        desc = get_description(t)
        flag = country_flag(t.get("country", ""))
        cat_emoji = category_emoji(t["category"])
        surf_emoji = surface_emoji(t["surface"])

        # Build the markdown
        content = f"""---
layout: base
title: "{t['tournament']}"
description: "{t['tournament']} - 2027 ATP Tour event in {t['city']}"
permalink: /tournaments/{slug}/
---

<nav class="breadcrumb">
  <a href="{{{{ '/' | relative_url }}}}">Home</a> →
  <a href="{{{{ '/tournaments/' | relative_url }}}}">Tournaments</a> →
  <span>{t['tournament']}</span>
</nav>

<article class="tournament-detail">
  <header class="t-header">
    <div class="t-cat">
      {cat_emoji} <span class="cat-badge cat-{t['category'].lower().replace(' ', '-')}">{t['category']}</span>
    </div>
    <h1>{flag} {t['tournament']}</h1>
    <p class="t-subtitle">{t['city']}, {flag} | Week {t['week']} of 2027</p>
  </header>

  <section class="t-quick-facts">
    <div class="fact"><div class="label">📅 Dates</div><div class="value">{t['start_date']} → {t['end_date']}</div></div>
    <div class="fact"><div class="label">📍 Venue</div><div class="value">{t['city']}</div></div>
    <div class="fact"><div class="label">{surf_emoji} Surface</div><div class="value">{t['surface']}</div></div>
    <div class="fact"><div class="label">🎯 Category</div><div class="value">{t['category']}</div></div>
    <div class="fact"><div class="label">📅 Calendar Week</div><div class="value">Week {t['week']}</div></div>
"""

        if t.get("draws"):
            content += f'    <div class="fact"><div class="label">👥 Draw Size</div><div class="value">{t["draws"]}</div></div>\n'

        content += f"""  </section>

  <section class="t-description">
    <h2>About This Tournament</h2>
    <p>{desc}</p>
  </section>
"""

        if t.get("url"):
            content += f"""
  <section class="t-official">
    <h2>Official Resources</h2>
    <p>
      <a href="{t['url']}" target="_blank" rel="noopener" class="btn btn-primary">
        🌍 Visit Official Tournament Website ↗
      </a>
    </p>
  </section>
"""
        else:
            content += """
  <section class="t-official">
    <h2>Official Resources</h2>
    <p><em>Official website to be announced.</em></p>
  </section>
"""

        # Notes / legend
        if t.get("notes"):
            notes_list = ", ".join([f"`{n}`" for n in t["notes"]])
            content += f"""
  <section class="t-notes">
    <h2>📝 Schedule Notes</h2>
    <p>Codes: {notes_list} (see <a href="{{{{ '/about/' | relative_url }}}}#legend">legend</a>)</p>
  </section>
"""

        # Live rankings link
        content += """
  <section class="t-rankings">
    <h2>📈 Live ATP Rankings</h2>
    <p>Check current ATP rankings to see who's likely to compete:</p>
    <ul>
      <li><a href="https://www.atptour.com/en/rankings/singles" target="_blank" rel="noopener">ATP Singles Rankings ↗</a></li>
      <li><a href="https://www.atptour.com/en/rankings/race-to-turin" target="_blank" rel="noopener">Race to Turin (year-to-date) ↗</a></li>
    </ul>
  </section>

  <section class="t-back">
    <p><a href="{{ '/tournaments/' | relative_url }}">← Back to all tournaments</a></p>
  </section>
</article>
"""
        out.write_text(content)
        print(f"  ✅ {slug}.md")

    print(f"\n✅ Generated {len(tournaments)} tournament pages in {out_dir}")


if __name__ == "__main__":
    main()
