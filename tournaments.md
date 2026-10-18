---
layout: base
title: All Tournaments
---

# 🏟️ All 66 Tournaments

Browse every event on the 2027 ATP calendar. Each card links to the official tournament website and a detailed event page.

<div class="filter-bar">
  <strong>Filter by category:</strong>
  {% assign categories = "Grand Slam,ATP Masters 1000,ATP 500,ATP 250,ATP Finals,Davis Cup,United Cup,Laver Cup" | split: "," %}
  {% for cat in categories %}
    <a href="#{{ cat | slugify }}" class="filter-pill">{{ cat }}</a>
  {% endfor %}
</div>

{% for cat in categories %}
  {% assign events = site.data.tournaments | where: "category", cat | sort: "start_date" %}
  {% if events.size > 0 %}
  <section id="{{ cat | slugify }}" class="category-section">
    <h2>{{ cat }} ({{ events.size }})</h2>
    <div class="tournament-grid">
      {% for t in events %}
      <div class="tournament-card cat-{{ t.category | downcase | replace: ' ', '-' }}">
        <div class="card-header">
          <span class="cat-badge">{{ t.category }}</span>
          <span class="surface-badge">{{ t.surface }}</span>
        </div>
        <h3>
          {% if t.url != "" %}
            <a href="{{ t.url }}" target="_blank" rel="noopener">{{ t.tournament }}</a>
          {% else %}
            {{ t.tournament }}
          {% endif %}
        </h3>
        <p class="card-meta">
          <span class="city">📍 {{ t.city }}</span>
          {% if t.draws %}<span class="draws">👥 {{ t.draws }}</span>{% endif %}
        </p>
        <p class="card-dates">
          🗓️ {{ t.start_date | date: "%b %-d" }} – {{ t.end_date | date: "%b %-d, %Y" }}
        </p>
        <a href="{{ '/tournaments/' | append: t.tournament | slugify | append: '/' | relative_url }}" class="card-link">Details →</a>
      </div>
      {% endfor %}
    </div>
  </section>
  {% endif %}
{% endfor %}
