---
title: 成员
nav:
  order: 3
  tooltip: 关于我们
---

{%- comment -%}
每年换届只改 _config.yaml 里的 season.current，本页不需要改动。
{%- endcomment -%}
{% assign season = site.season.current %}
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

{% include section.html background="images/background.jpg" dark=true %}

从 SPR 走出的优秀人才，他们在各自领域取得了优异的成绩，是 SPR 战队的骄傲和榜样。

{% include section.html %}

# 杰出人物

{% include list_portrait.html data="members" component="portrait" filters="type: 杰出人物" %}