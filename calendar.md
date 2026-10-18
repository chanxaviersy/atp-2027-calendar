---
layout: base
---
<div class="calendar">
  <h1>📅 2027 ATP Tour Calendar</h1>
  <p class="lead">Complete season schedule grouped by month. Click any event for full details.</p>

  {% assign months = "January,February,March,April,May,June,July,August,September,October,November,December" | split: "," %}
  {% for month_name in months %}
    {% assign month_num = forloop.index %}
    {% assign events_in_month = site.data.tournaments | where_exp: "t", "t.start_date contains '-'" | where_exp: "t", "t.start_date | slice: 5, 2 == month_num | append: ''" %}
    {% comment %} Filter properly: get events whose month matches {% endcomment %}
    {% assign filtered = "" | split: "" %}
    {% for t in site.data.tournaments %}
      {% assign t_month = t.start_date | slice: 5, 2 | integer %}
      {% if t_month == month_num %}
        {% assign filtered = filtered | push: t %}
      {% endif %}
    {% endfor %}

    {% if filtered.size > 0 %}
    <section class="month-section">
      <h2>{{ month_name }} 2027</h2>
      <div class="tournament-grid">
        {% assign sorted = filtered | sort: 'start_date' %}
        {% for t in sorted %}
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
            {% assign start_d = t.start_date | date: "%b %-d" %}
            {% assign end_d = t.end_date | date: "%b %-d" %}
            🗓️ {{ start_d }} – {{ end_d }}
          </p>
          <a href="{{ '/tournaments/' | append: t.tournament | slugify | append: '/' | relative_url }}" class="card-link">Details →</a>
        </div>
        {% endfor %}
      </div>
    </section>
    {% endif %}
  {% endfor %}
</div>
