---
title: 历史团队成员
---
{%- comment -%}
归档页链接由 _data/seasons.yaml 的 url 字段驱动：
把某个赛季的 url 填成 team/<赛季>-season/，并复制一份归档页即可。
{%- endcomment -%}
* [所有队员]({{ "/team/all" | relative_url }})

{% for s in site.data.seasons %}
{% if s.url and s.url != "" %}
* [{{ s.year }} 赛季团队成员]({{ s.url | relative_url }})
{% endif %}
{% endfor %}