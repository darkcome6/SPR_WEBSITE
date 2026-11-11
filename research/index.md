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
{% assign national_awards_count = 0 %}
{% assign international_awards_count = 0 %}
{% assign provincial_awards_count = 0 %}
{% assign other_awards_count = 0 %}
{% for award in site.awards %}
{% if award.type == "国家级" %}
{% assign national_awards_count = national_awards_count | plus: 1 %}
{% elsif award.type == "国际级" %}
{% assign international_awards_count = international_awards_count | plus: 1 %}
{% elsif award.type == "省级" %}
{% assign provincial_awards_count = provincial_awards_count | plus: 1 %}
{% else %}
{% assign other_awards_count = other_awards_count | plus: 1 %}
{% endif %}
{% endfor %}

{% assign awards_count =  national_awards_count | plus: international_awards_count | plus: provincial_awards_count | plus: other_awards_count %}

根据不完全统计，SPR 战队已经获得了总计 {{awards_count}} 项奖项。
<table>
<tr>
  <td>国家级奖项</td>
  <td>国际级奖项</td>
  <td>省级奖项</td>
  <td>其他奖项</td>
</tr>
<tr>
  <td>{{national_awards_count}}</td>
  <td>{{international_awards_count}}</td>
  <td>{{provincial_awards_count}}</td>
  <td>{{other_awards_count}}</td>
</tr>
</table>

{% if national_awards_count > 0 %}
### 国家级
{% include list.html data="awards" component="awards" style="rich" filters="type: 国家级" %}
{% endif %}

{% if international_awards_count > 0 %}
### 国际级
{% include list.html data="awards" component="awards" style="simple" filters="type: 国际级" %}
{% endif %}

{% if provincial_awards_count > 0 %}
### 省级
{% include list.html data="awards" component="awards" style="simple" filters="type: 省级" %}
{% endif %}

{% if other_awards_count > 0 %}
### 其他类型
{% include list.html data="awards" component="awards" style="simple" filters="type: 其他" %}
{% endif %}