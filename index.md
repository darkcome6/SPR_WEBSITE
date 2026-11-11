---
---

{% assign season = site.season.current %}

# 中国石油大学 SPR 战队

中国石油大学 RoboMaster 团队（SPR 战队）是中国石油大学机械与储运工程学院最耀眼的团队之一，是一个以参加 RoboMaster 机器人比赛为主、以培养队员全面综合水平为目标的综合型团队。

<div class="stats">
  <div class="stats-item">
    <span class="stats-value">{{ site.data.seasons | size }}</span>
    <span class="stats-label">个赛季</span>
  </div>
  <div class="stats-item">
    <span class="stats-value">{{ site.members | size }}</span>
    <span class="stats-label">名成员</span>
  </div>
  <div class="stats-item">
    <span class="stats-value">{{ site.awards | size }}</span>
    <span class="stats-label">项荣誉</span>
  </div>
  <div class="stats-item">
    <span class="stats-value">{{ site.events | size }}</span>
    <span class="stats-label">场比赛</span>
  </div>
</div>

{%
  include button.html
  type="docs"
  text="Bilibili"
  icon="fa-brands fa-bilibili"
  link="https://space.bilibili.com/475402455"
%}
{%
  include button.html
  type="github"
  text="GitHub"
  link="https://github.com/darkcome6/SPR_WEBSITE"
%}
{%
  include button.html
  type="docs"
  text="微信公众号"
  icon="fa-brands fa-weixin"
  link="https://mp.weixin.qq.com/s/Zrk4PRRGSimJG9bVDj3Zsg"
%}

{% include section.html %}

## 一代代 SPR

从第一支队伍到现在，每个赛季都留下一批人、一批车、一批故事。

{% include timeline.html %}

{% include section.html %}

## 20{{ season }} 赛季的我们

{% include member-wall.html limit=30 %}

{%
  include button.html
  link="team"
  text="查看全部成员"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% include section.html %}

## 近期赛程

更多赛程请查看[历史赛程]({{ "/events" | relative_url }})

{% assign events_year = site.season.events_year %}
{% capture f_events_year %}date: {{ events_year }}{% endcapture %}
{% include list.html data="events" component="events" style="rich" filters=f_events_year %}

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