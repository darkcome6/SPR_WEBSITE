# 中国石油大学 SPR 战队官网

基于 [Lab Website Template](https://greene-lab.gitbook.io/lab-website-template-docs) 的 Jekyll 站点。

- 源码分支：`main`（**只改这里**）
- 构建产物：`gh-pages`，由 GitHub Actions 自动生成，手改会被覆盖
- 线上地址：<https://darkcome6.github.io/SPR_WEBSITE>

## 域名与部署

当前使用 GitHub Pages 默认地址：<https://darkcome6.github.io/SPR_WEBSITE>

### 换成自己的域名

只需要买域名，**不需要服务器，也不需要 ICP 备案**（GitHub Pages 托管在境外，
阿里云官方原文：*托管于中国内地服务器的网站需进行 ICP 备案，托管于非中国内地服务器的网站无需进行 ICP 备案*）。
但域名**必须完成实名认证**，否则会被注册局 `serverHold`，解析不生效。

阿里云「云工开物」学生 300 元券**不能用来买域名**（官方规则把「域名 / domain」列入通用券不适用清单），
域名只能现金支付。2026-11 万网价格：`.com` 首年 76 元、续费 90 元；`.cn` 首年 30 元、续费 42 元；
`.top` 首年 14 元、续费 39 元；`.xyz`/`.site`/`.online`/`.tech` 首年 6–12 元但续费 120–254 元。
长期用优先 `.com` 或 `.cn`。

**操作顺序：先在 GitHub 填域名，再去阿里云配 DNS**（跳过这步可能被别人抢注子域）。

1. 买域名并完成实名认证。
2. 仓库 Settings → Pages → *Custom domain* 填 `www.<你的域名>` 并 Save。
   建议用 `www` 作主域名：`www` 不受 GitHub 换 IP 影响，apex 会自动 301 过来。
3. 阿里云 → 域名控制台 → 解析设置（默认免费版云解析够用）。让脚本把记录列出来照着填：

   ```bash
   python tools/set_domain.py www.<你的域名>
   ```

   它会写出 `CNAME` 并打印要加的 9 条记录（`A`/`AAAA` 各 4 条到 `@`，`CNAME` 一条 `www` → `darkcome6.github.io`）。
   其余 parking 记录删掉，**不要**加 `*` 泛解析；多余的 A/CNAME 会挡住证书签发。
4. 回到 Settings → Pages，等证书签发（几分钟到 1 小时）后勾选 *Enforce HTTPS*。
   卡住就 Remove 域名再 Save 一次，重新触发 Let's Encrypt 签发。
5. 提交推送 `CNAME`，确认 `https://www.<你的域名>` 能打开。

撤销域名：`python tools/set_domain.py --clear`，同时清掉 Settings 里的自定义域名。

**为什么要落到仓库里**：本站是「构建后 push `gh-pages`」的发布方式，自定义域名存放在**产物根目录的 `CNAME`** 里，
而每次部署都会重写 `gh-pages`。源码根目录的 `CNAME` 会被 Jekyll 原样拷进 `_site`，所以不会丢；
只在 Settings 里填、仓库里没有 `CNAME` 的话，域名会在下一次部署后静默失效。

（也可以用仓库变量：Settings → Secrets and variables → Actions → Variables 建 `CUSTOM_DOMAIN`，
工作流会用它生成 `_site/CNAME`。两种方式等效，`CNAME` 文件更直观。）

注意：换自定义域名后站点从 `darkcome6.github.io/SPR_WEBSITE/` 变为域名根路径，
旧链接会 404。因为全站统一用 `relative_url`，站内链接会自动跟着变对。

`tools/validate_content.py` 会检查 `CNAME`（如果存在）是否为单行裸域名。

## 国内访问与外部依赖

站点托管在 GitHub Pages（境外 Fastly 节点），**能不能直连取决于运营商和时段**。
换自定义域名不改变这一点：域名解析出来还是同一批 IP，买域名只解决「网址好记」。

要稳定国内访问只能换托管地：境内（必须 ICP 备案，个人备案做「战队官网」容易被驳回）
或香港/新加坡 VPS（免备案，约 24 元/月起，需自建 Nginx/Caddy）。

为了少踩「页面能打开但图表空白、图标变方块」的坑，这些依赖已放进 `_vendor/` 自托管：

| 依赖 | 位置 | 加载范围 |
| --- | --- | --- |
| ECharts 5.5.1 | `_vendor/echarts.min.js` | 只有成果页（有图表的页面）才加载 |
| Font Awesome 6.5.0 | `_vendor/fontawesome/` + `_vendor/webfonts/` | 全站，异步加载 |

仍在用境外 CDN 的部分（失效只影响观感，不影响读内容）：
Google Fonts 的 Barlow / Roboto Mono（会回退到系统字体）、
`unpkg.com` 的 tippy / popper / mark.js（提示框与站内搜索高亮）、
`cdn.jsdelivr.net` 的 pygments 主题（代码块配色）。

`_vendor/` 已在 `_config.yaml` 的 `include` 里，否则下划线开头的目录默认不会被发布。

## 本地预览

```bash
bundle install
bundle exec jekyll serve --baseurl ""
```

打开 <http://localhost:4000>。需要 Ruby 3.1（与 CI 一致）。

## 想改什么，改哪里

| 想改的内容 | 改这里 |
| --- | --- |
| 站点标题、描述、slogan、页头背景、社交链接 | `_config.yaml` |
| 首页封面轮播图 | `_config.yaml` 的 `header-slides`（按顺序循环淡入淡出） |
| 当前赛季 | `_config.yaml` 的 `season` |
| 成员 | `_members/<姓名>.md` |
| 成员分组（顺序/名称） | `_data/groups.yaml` |
| 获奖 | `_awards/<奖项>.md` |
| 比赛记录 | `_events/<场次>.md` |
| 新闻 / 技术博文 | `_news/`、`_posts/`（文件名 `YYYY-MM-DD-xxx.md`） |
| 赛季成绩 / 历史成绩 / 积分榜 | `_data/seasons.yaml` |
| 高光时刻视频 | `_data/highlights.yaml` |
| 机器人介绍 | `projects/index.md` |
| 首页文案 | `index.md` |
| 大创项目 / 专利 | `_projects/`、`_patents/`（当前 `output: false`，不对外展示） |
| 导航顺序 | 对应页面 front matter 的 `nav.order` |
| 配色 | `_styles/-theme.css` |
| 组件结构 | `_includes/`、`_layouts/` |

`_styles/` 和 `_scripts/` 下的文件会被自动注入页面，新增文件无需改模板。

### 成员分组组件

`_includes/group.html` 负责「标题 + 成员列表」，**列表为空时整块不渲染**（避免某赛季某组没人时留下空标题）：

```liquid
{% include group.html title="机械组" filters="role: 机械组" exact_filters=f_season style="small" %}
```

可选参数：`icon`、`style`（`small`/`tiny`）、`data`、`component`。
### 成果页的数据来源

成果页各板块都不写死在页面里，**没有数据时整块自动隐藏**：

| 板块 | 数据来源 | 显示条件 |
| --- | --- | --- |
| 历史成绩 | `_data/seasons.yaml` 的 `rank` / `award` | 至少一个赛季填了其一 |
| 积分榜排名 | `_data/seasons.yaml` 的 `rank_value`（全国赛名次数字） | 至少一个赛季填了 |
| 高光时刻 | `_data/highlights.yaml` | 数组非空 |
| 荣誉奖项 | `_awards/` 集合 | 按 `type` 分区，空分区不显示 |

`_data/seasons.yaml` 同时驱动首页的「一代代 SPR」时间轴，**改一处两边同步**。
新增赛季时在最前面加一条即可：

```yaml
- season: "28"      # 赛季号，与 _members 的 seasons 对应
  year: 2028
  title: 2028 赛季
  rank: 全国赛十六强   # 显示在徽章与历史成绩
  award: 国家级二等奖
  rank_value: 16      # 只用于积分榜趋势图，填全国赛名次数字
  cover: images/2025-team.jpg
  summary: 一句话赛季记忆
  url: team/          # 可点进赛季成员页，留空则不可点
```

高光时刻只需 BV 号：

```yaml
- title: RoboMaster 2025 十六进八
  desc: 三分钟推爆基地
  bvid: BV1xx411c7XX
```

## 每年换届怎么做

1. 改 `_config.yaml`：
   ```yaml
   season:
     current: "27"      # 成员页与首页展示的赛季号
     events_year: 2026  # 首页「近期赛程」的年份
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
5. 需要归档上一赛季成员时，把 `team/23-season/` 复制成 `team/<赛季>-season/`，只改 front matter 的 `season` 和 `title`，再到 `team/history/index.md` 加一行链接。
6. 跑一遍校验，确认没有静默失效：

```bash
python tools/validate_content.py
```

## 本地构建（Windows 用户注意）

`jekyll-last-modified-at` 依赖 `posix-spawn`，**只支持 POSIX，Windows 下无法安装**。
所以在 Windows 上请用 WSL 构建：

```bash
wsl -d Ubuntu-22.04
sudo apt install -y ruby-full build-essential zlib1g-dev libyaml-dev
sudo gem install jekyll -v 4.3.2
cd /mnt/e/code/SPR/SPR_WEBSITE
JEKYLL_NO_BUNDLER_REQUIRE=true jekyll _4.3.2_ build --baseurl /SPR_WEBSITE
```

`JEKYLL_NO_BUNDLER_REQUIRE=true` 是为了跳过 `Gemfile` 里的 `html-proofer`（它要求 Ruby ≥ 3.1，
而 `proofer: false` 时构建根本用不到它）。产物在 `_site/`。

## 批量导入内容

成员/荣誉/赛程等数据可以先填在 `data-inbox/` 的 CSV 里，再一次性转成 Markdown：

```bash
python tools/import_content.py                      # 演练，只列出会生成/覆盖哪些文件
python tools/import_content.py --write              # 真正写入
python tools/import_content.py --write --only members,awards
```

约定：

- 多值字段用 `|` 分隔，例如 `seasons` 写 `24|25`、`members` 写 `张三|李四`
- 空单元格表示该字段不写入 front matter
- 同名记录会自动加序号，不会互相覆盖
- `data-inbox/` 已在 `_config.yaml` 的 `exclude` 中，草稿不会发布到线上
- 导入后务必运行 `tools/validate_content.py` 检查

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

## 素材与许可

- `images/logo.svg` 的狮头剪影取自 [Game Icons](https://game-icons.net/) 的 `lion`
  （作者 Lorc，[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)），
  按本站徽标需要做了缩放与排布；`images/logo_black.png`（站点图标）与
  `images/share.jpg`（分享卡片）由同一剪影生成。
- 其余照片由战队成员拍摄并提供。