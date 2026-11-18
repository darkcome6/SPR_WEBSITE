---
---

{% assign season = site.season.current %}
{% assign current_season = site.data.seasons | where: "season", season | first %}
{% assign season_year = current_season.year | default: season %}

# 中国石油大学（北京）SPR 战队

SPR 战队隶属于中国石油大学（北京），是学校面向 RoboMaster 机甲大师赛组建的学生科技创新团队，成立于 2004 年。战队下设机械、电控、算法、视觉、运营等多个部门，形成了完整的机器人研发与项目管理体系。

战队立足工程实践，独立完成多类竞赛机器人的机械结构设计、嵌入式控制与视觉算法开发，致力于培养兼具动手能力与工程素养的复合型科技人才。

<div class="stats">
  <div class="stats-item">
    <span class="stats-value">{{ site.data.seasons | size }}</span>
    <span class="stats-label">个赛季</span>
  </div>
  <div class="stats-item">
    <span class="stats-value">{{ site.members | size }}</span>
    <span class="stats-label">名成员</span>
  </div>
  {% if site.awards.size > 0 %}
  <div class="stats-item">
    <span class="stats-value">{{ site.awards | size }}</span>
    <span class="stats-label">项荣誉</span>
  </div>
  {% endif %}
  {% if site.events.size > 0 %}
  <div class="stats-item">
    <span class="stats-value">{{ site.events | size }}</span>
    <span class="stats-label">场比赛</span>
  </div>
  {% endif %}
</div>
{%
  include button.html
  type="docs"
  text="Bilibili"
  icon="fa-brands fa-bilibili"
  link="https://space.bilibili.com/1489728412"
%}
{%
  include button.html
  type="github"
  text="GitHub"
  link="https://github.com/darkcome6/SPR_WEBSITE"
%}
{%
  include button.html
  link="contact"
  text="微信公众号：SPR机器人队"
  icon="fa-brands fa-weixin"
  style="bare"
  flip=true
%}

{% include section.html %}

## 一代代 SPR

从第一支队伍到现在，每个赛季都留下一批人、一批车、一批故事。

{% include timeline.html %}

{% include section.html %}

## {{ season_year }} 赛季的我们

{% include member-wall.html %}

{%
  include button.html
  link="team"
  text="查看全部成员"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% assign events_year = site.season.events_year %}
{% capture f_events_year %}date: {{ events_year }}{% endcapture %}
{% assign season_events = site.events | data_filter: f_events_year %}

{% if season_events.size > 0 %}
{% include section.html %}

## 近期赛程

更多赛程请查看[历史赛程]({{ "/events" | relative_url }})

{% include list.html data="events" component="events" style="rich" filters=f_events_year %}
{% endif %}

{% include section.html %}

## 继续了解

{% capture text %}

分区赛与全国赛的成绩、历年高光时刻与获奖记录，都汇总在成果页。

{%
  include button.html
  link="research"
  text="我们的成果"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/cheer.jpg"
  link="research"
  title="成果与荣誉"
  text=text
%}


{% capture text %}

备赛、比赛、团建的影像与故事，以及战队的最新动态。

{%
  include button.html
  link="news"
  text="最新动态"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/news.jpeg"
  link="news"
  title="记忆与动态"
  flip=true
  style="bare"
  text=text
%}