---
title: 历史赛程
---
{% if site.events.size > 0 %}
{% assign years = site.events | group_by_exp: "e", "e.date | date: '%Y'" | sort: "name" | reverse %}

{% for year in years %}
{% capture f_year %}date: {{ year.name }}{% endcapture %}

## {{ year.name }} 年

{% include list.html data="events" component="events" style="rich" filters=f_year %}
{% endfor %}

{% else %}
暂无赛程记录。
{% endif %}