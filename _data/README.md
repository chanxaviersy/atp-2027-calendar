# Tournaments Data

This directory contains the structured tournament data used by the Jekyll site.

## Files

- `tournaments.yml` — Master dataset of all 60+ ATP Tour 2027 events
- `notes.yml` — Legend for the superscript numbers (e.g. SUNDAY START, SATURDAY FINAL)

## Data Schema

Each tournament entry contains:

```yaml
- week: 1                          # Calendar week number
  start_date: 2027-01-01           # ISO 8601 date
  end_date: 2027-01-04             # ISO 8601 date (same week, inferred)
  city: "Perth, Sydney"            # Host city
  tournament: "United Cup"         # Official tournament name
  surface: "H"                     # H=Hard, CL=Clay, G=Grass, IH=Indoor Hard
  category: "United Cup"           # Grand Slam, ATP Masters 1000, ATP 500, ATP 250, ATP Finals, Laver Cup, Davis Cup
  draws: 18                        # Draw size (teams for United Cup)
  notes: ["6"]                     # Reference to footnotes (e.g. FRIDAY START)
  url: "https://..."               # Official tournament website
  country: "AUS"                   # ISO 3166-1 alpha-3 country code
```

## Updating the Calendar

When the ATP publishes updates (typically 2-3 times per year), edit `tournaments.yml` and re-commit. GitHub Pages will auto-rebuild.

## Sources

- **Calendar data**: [ATP Tour 2027 Calendar (PDF, 14 January 2026 update)](https://www.atptour.com/en/scores/current-calendar)
- **Live rankings**: [ATP Rankings](https://www.atptour.com/en/rankings/singles)
- **Tournament websites**: Linked individually in each event's detail page
