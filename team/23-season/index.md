---
title: 23 赛季成员
season: "23"
---

{%- comment -%}
归档页：只改 front matter 里的 season，其他都不用动。
新增归档时复制本文件到 team/<赛季>-season/index.md，改 season 与 title 即可。
{%- endcomment -%}
{% assign season = page.season %}
{% capture f_season %}seasons: {{ season }}{% endcapture %}
{% capture f_echelon %}echelon: {{ season }}{% endcapture %}
{% capture f_leader %}type: {{ season }}赛季团队负责人{% endcapture %}

# {% include icon.html icon="fa-solid fa-users" %}{{ season }} 赛季团队成员
{% include search-box.html %}
{% include search-info.html %}
历史成员请参考[历届成员]({{ "/team/history" | relative_url }})。

{% include section.html %}

{% include group.html title="指导老师" filters="role: 指导老师" %}

{% include group.html title="团队负责人" exact_filters=f_leader %}

{% include group.html title="机械组" filters="role: 机械组" exact_filters=f_season style="small" %}

{% include group.html title="电路组" filters="role: 电路组" exact_filters=f_season style="small" %}

{% include group.html title="嵌软组" filters="role: 嵌软组" exact_filters=f_season style="small" %}

{% include group.html title="算法组" filters="role: 算法组" exact_filters=f_season style="small" %}

{% include group.html title="运营组" filters="role: 运营组" exact_filters=f_season style="small" %}

{% include group.html title="梯队" exact_filters=f_echelon style="tiny" %}