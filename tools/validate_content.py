#!/usr/bin/env python3
"""校验内容集合的 front matter，避免改错字段后页面静默变空白。

用法（仓库根目录执行）:
    python tools/validate_content.py

出错时退出码为 1，可直接用于 CI。
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MEMBER_REQUIRED = ("name", "role", "type", "image")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif"}
MAX_IMAGE_BYTES = 1_500_000

errors: list[str] = []
warnings: list[str] = []


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_front_matter(path: Path) -> tuple[dict | None, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{rel(path)}: 缺少 front matter（文件为空或未以 --- 开头）")
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            raw = "\n".join(lines[1:index])
            try:
                data = yaml.safe_load(raw) or {}
            except yaml.YAMLError as exc:
                errors.append(f"{rel(path)}: front matter 不是合法 YAML — {exc}")
                return None, text
            if not isinstance(data, dict):
                errors.append(f"{rel(path)}: front matter 必须是键值对")
                return None, text
            return data, text
    errors.append(f"{rel(path)}: front matter 没有闭合的 ---")
    return None, text


def as_list(value) -> list:
    if value is None or value == "":
        return []
    return value if isinstance(value, list) else [value]


def check_image(owner: str, value) -> None:
    if not value:
        return
    text = str(value)
    if re.match(r"^https?://", text):
        return
    path = ROOT / text
    if not path.is_file():
        errors.append(f"{owner}: 图片不存在 — {value}")
        return
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        errors.append(f"{owner}: 图片格式不支持 — {value}")
    size = path.stat().st_size
    if size > MAX_IMAGE_BYTES:
        warnings.append(f"{owner}: 图片过大 {size // 1024} KB（建议压缩或转 WebP）— {value}")


def parse_date(value):
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime(value.year, value.month, value.day)
    text = str(value or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m"):
        try:
            return dt.datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def check_date(owner: str, value) -> None:
    if not value:
        errors.append(f"{owner}: 缺少 date")
        return
    if parse_date(value) is None:
        errors.append(f"{owner}: date 格式无法识别 — {value}")


def load_config() -> dict:
    path = ROOT / "_config.yaml"
    if not path.is_file():
        errors.append("_config.yaml 不存在")
        return {}
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        errors.append(f"_config.yaml 不是合法 YAML — {exc}")
        return {}

    title = str(config.get("title") or "")
    if not title.strip():
        errors.append("_config.yaml: title 为空")
    if "DESCRIPTION=" in title or "An engaging" in title:
        errors.append("_config.yaml: title 仍是模板占位文本")

    season = config.get("season") or {}
    if not isinstance(season, dict) or not season.get("current"):
        errors.append("_config.yaml: 缺少 season.current")
    if not season.get("events_year"):
        errors.append("_config.yaml: 缺少 season.events_year")

    links = config.get("links") or {}
    for key, value in links.items():
        if key == "email" and "@" not in str(value):
            errors.append(f"_config.yaml: links.{key} 不是邮箱地址 — {value}")
        if key in ("github",) and not str(value).startswith("http"):
            errors.append(f"_config.yaml: links.{key} 需要完整 URL — {value}")
    return config


def check_members() -> set[str]:
    names: dict[str, str] = {}
    seasons = Counter()
    echelons = Counter()

    for path in sorted((ROOT / "_members").glob("*.md")):
        owner = rel(path)
        data, _ = read_front_matter(path)
        if data is None:
            continue
        for key in MEMBER_REQUIRED:
            if not data.get(key):
                errors.append(f"{owner}: 缺少必填字段 {key}")
        name = str(data.get("name") or "").strip()
        if name:
            if name in names:
                errors.append(f"{owner}: 姓名重复 — {name}（另见 {names[name]}）")
            names[name] = owner

        if "seasons" not in data:
            errors.append(f"{owner}: 缺少 seasons（用于按赛季筛选成员）")
        else:
            values = as_list(data.get("seasons"))
            if not values:
                warnings.append(f"{owner}: seasons 为空，不会出现在任何赛季分组")
            for value in values:
                if not str(value).isdigit():
                    errors.append(f"{owner}: seasons 只能写赛季号（如 24）— {value!r}")
                else:
                    seasons[str(value)] += 1

        echelon = data.get("echelon")
        if echelon in (None, ""):
            warnings.append(f"{owner}: 缺少 echelon（梯队分组会漏掉此人）")
        else:
            echelons[str(echelon)] += 1

        check_image(owner, data.get("image"))

    print(f"成员: {len(names)} 人 | 赛季分布: {dict(sorted(seasons.items()))} | 梯队: {dict(sorted(echelons.items()))}")
    return set(names)


def check_awards(member_names: set[str], strict: bool) -> None:
    count = 0
    missing = 0
    for path in sorted((ROOT / "_awards").glob("*.md")):
        owner = rel(path)
        data, _ = read_front_matter(path)
        if data is None:
            continue
        count += 1
        if not str(data.get("name") or "").strip():
            errors.append(f"{owner}: 缺少 name")
        if not data.get("type"):
            errors.append(f"{owner}: 缺少 type（国家级/国际级/省级/其他）")
        if not data.get("prize"):
            warnings.append(f"{owner}: 缺少 prize")
        check_date(owner, data.get("date"))
        for member in as_list(data.get("members")):
            name = str(member).strip()
            if name and name not in member_names:
                missing += 1
                message = f"{owner}: members 里的「{name}」不在 _members 中（毕业成员可忽略；若为笔误则成员页反查会漏）"
                (errors if strict else warnings).append(message)
    print(f"荣誉: {count} 条 | 关联到非在册成员: {missing} 处")


def check_events(config: dict) -> None:
    count = 0
    years = Counter()
    for path in sorted((ROOT / "_events").glob("*.md")):
        owner = rel(path)
        data, _ = read_front_matter(path)
        if data is None:
            continue
        count += 1
        for key in ("name", "red", "blue", "red_score", "blue_score"):
            if data.get(key) in (None, ""):
                errors.append(f"{owner}: 缺少 {key}")
        check_date(owner, data.get("date"))
        date = parse_date(data.get("date"))
        if date:
            years[date.strftime("%Y")] += 1
    current_year = str((config.get("season") or {}).get("events_year") or "")
    print(f"赛程: {count} 场 | 年份分布: {dict(sorted(years.items()))}")
    if current_year and years.get(current_year, 0) == 0:
        warnings.append(f"season.events_year={current_year} 没有任何赛程，首页会显示空列表")


def check_posts_and_news() -> None:
    for label, folder in (("博文", "_posts"), ("新闻", "_news")):
        count = 0
        for path in sorted((ROOT / folder).glob("*.md")):
            owner = rel(path)
            data, _ = read_front_matter(path)
            if data is None:
                continue
            count += 1
            if not (data.get("title") or data.get("name")):
                errors.append(f"{owner}: 缺少 title")
            if not re.match(r"^\d{4}-\d{2}-\d{2}-", path.name):
                warnings.append(f"{owner}: 文件名建议以 YYYY-MM-DD- 开头")
        print(f"{label}: {count} 篇")


def check_pages() -> None:
    for path in sorted(ROOT.glob("*.md")) + sorted(ROOT.glob("*/index.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\]\((/[^)\s]+)\)", text):
            errors.append(
                f"{rel(path)}: 内部链接写死了根路径 {match.group(1)}，换域名会失效，请改用 relative_url"
            )
        if "SPR_WEBSITE/" in text and "relative_url" not in text:
            errors.append(f"{rel(path)}: 出现写死的 /SPR_WEBSITE/ 路径")
        if "HUSTLYRM" in text:
            warnings.append(f"{rel(path)}: 仍指向狼牙仓库 HUSTLYRM")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    strict = "--strict" in sys.argv[1:]
    config = load_config()
    member_names = check_members()
    check_awards(member_names, strict)
    check_events(config)
    check_posts_and_news()
    check_pages()

    print()
    for message in warnings:
        print(f"WARN  {message}")
    for message in errors:
        print(f"ERROR {message}")
    print(f"\n结果: {len(errors)} 个错误, {len(warnings)} 个警告")
    if not strict and warnings:
        print("提示: 内容收尾阶段可用 python tools/validate_content.py --strict 把警告也当作错误")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
