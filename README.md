# 中国石油大学 SPR 战队官网

基于 [Lab Website Template](https://greene-lab.gitbook.io/lab-website-template-docs) 的 Jekyll 站点。

- 源码分支：`main`（**只改这里**）
- 构建产物：`gh-pages`，由 GitHub Actions 自动生成，手改会被覆盖
- 线上地址：<https://darkcome6.github.io/SPR_WEBSITE>

## 本地预览

```bash
bundle install
bundle exec jekyll serve --baseurl ""
```

打开 <http://localhost:4000>。需要 Ruby 3.1（与 CI 一致）。

## 想改什么，改哪里

| 想改的内容 | 改这里 |
| --- | --- |
| 站点标题、描述、slogan、页头背景/视频、社交链接 | `_config.yaml` |
| 当前赛季 | `_config.yaml` 的 `season` |
| 成员 | `_members/<姓名>.md` |
| 获奖 | `_awards/<奖项>.md` |
| 比赛记录 | `_events/<场次>.md` |
| 新闻 / 技术博文 | `_news/`、`_posts/`（文件名 `YYYY-MM-DD-xxx.md`） |
| 项目 / 专利 | `_projects/`、`_patents/` |
| 首页文案 | `index.md` |
| 成果页文案和图表 | `research/index.md` |
| 导航顺序 | 对应页面 front matter 的 `nav.order` |
| 配色 | `_styles/-theme.css` |
| 组件结构 | `_includes/`、`_layouts/` |

`_styles/` 和 `_scripts/` 下的文件会被自动注入页面，新增文件无需改模板。

## 每年换届怎么做

1. 改 `_config.yaml`：
   ```yaml
   season:
     current: "25"      # 成员页展示的赛季号
     events_year: 2025  # 首页「近期赛程」的年份
   ```
2. 给新成员建 `_members/<姓名>.md`，`seasons` 写赛季号数组：
   ```yaml
   ---
   name: 张三
   image: images/member_photo/张三.webp
   role: 机械组组员
   type: 普通队员
   seasons: [25]        # 参加过哪些赛季
   echelon: 25          # 梯队（入队赛季）
   time: '25'           # 展示用的参赛时间
   grade: 2024
   affiliation: 机械与储运工程学院
   ---
   ```
3. 老成员只需在 `seasons` 里加上新赛季，`time` 同步更新。
4. 新赛季的 `_events`、`_awards` 正常新增即可，不用改任何模板。
5. 跑一遍校验，确认没有静默失效：

```bash
python tools/validate_content.py
```

## 内容校验

`tools/validate_content.py` 会检查：

- `_config.yaml` 的 title/season/links 是否被占位文本污染
- 成员必填字段、`seasons` 是否合法、头像是否存在且不过大
- 奖项里引用的成员姓名是否写错（毕业成员默认只告警，`--strict` 视为错误）
- 赛程必填字段与日期格式
- 页面里是否有写死的根路径（换域名会失效）

PR 会自动运行（`.github/workflows/validate-content.yaml`）。收尾阶段建议 `--strict`。

## 文档

模板完整文档：<https://greene-lab.gitbook.io/lab-website-template-docs>