---
title: 成果
nav:
  order: 1
  tooltip: 比赛成绩与荣誉
---

{%- comment -%}
本页各板块均按 _data 自动渲染，无数据时整块隐藏：
  历史成绩    _data/seasons.yaml 的 rank / award
  积分榜排名  _data/seasons.yaml 的 rank_value
  高光时刻    _data/highlights.yaml
  荣誉奖项    _awards 集合
{%- endcomment -%}
{% assign history = site.data.seasons | where_exp: "s", "s.rank != nil or s.award != nil" %}
{% assign rank_chart = site.data.seasons | where_exp: "s", "s.rank_value != nil" %}

# {% include icon.html icon="fa-solid fa-microscope" %}我们的成果

{% if history.size > 0 %}
## 历史成绩

{% include history.html %}

{% include section.html %}
{% endif %}

{% if rank_chart.size > 0 %}
## 积分榜排名

{% include rank-chart.html %}

{% include section.html %}
{% endif %}

{% if site.data.highlights.size > 0 %}
## 高光时刻

{% include highlights.html %}

{% include section.html %}
{% endif %}

## 荣誉奖项

{% include search-box.html %}
{% include search-info.html %}

{% assign awards_total = site.awards | size %}

{% if awards_total > 0 %}
根据不完全统计，SPR 战队已经获得了总计 {{ awards_total }} 项奖项。

{% include award-wall.html %}
{% else %}
暂无奖项记录。
{% endif %}