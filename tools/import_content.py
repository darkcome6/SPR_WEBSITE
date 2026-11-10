#!/usr/bin/env python3
"""把 data-inbox/*.csv 转换成 Jekyll 集合需要的 Markdown 文件。

默认只做演练（不写文件），确认无误后加 --write 真正写入。

用法:
    python tools/import_content.py              # 演练，列出将生成/覆盖的文件
    python tools/import_content.py --write      # 真正写入
    python tools/import_content.py --write --only members,awards

约定:
    - 多值字段用 | 分隔，例如 seasons: 24|25、members: 张三|李四
    - 空单元格表示该字段不写入 front matter
    - 生成后会提示运行 tools/validate_content.py 检查内容
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "data-inbox"

MULTI_VALUE_FIELDS = {"seasons", "members", "tags"}
BOOL_FIELDS = {"award"}
INT_FIELDS = {"echelon", "grade", "red_score", "blue_score"}
LINK_FIELDS = {
    "github": "github",
    "link_home": "home-page",
    "link_scholar": "google-scholar",
}
SAFE_NAME_RE = re.compile(r'[\\/:*?"<>|\r\n\t]')


def log(message: str) -> None:
    print(message)


def clean_name(value: str) -> str:
    """把值变成可用作文件名的字符串。"""
    name = SAFE_NAME_RE.sub("-", value.strip())
    name = re.sub(r"\s+", " ", name).strip(" .-")
    return name or "untitled"


def split_multi(value: str) -> list:
    return [part.strip() for part in str(value).split("|") if part.strip()]


def convert_value(field: str, value: str):
    text = str(value).strip()
    if text == "":
        return None
    if field in MULTI_VALUE_FIELDS:
        items = split_multi(text)
        if field in ("seasons", "echelon"):
            parsed = []
            for item in items:
                parsed.append(int(item) if item.isdigit() else item)
            return parsed
        return items
    if field in BOOL_FIELDS:
        return text.lower() in ("true", "1", "yes", "y", "是")
    if field in INT_FIELDS:
        return int(text) if text.lstrip("-").isdigit() else text
    return text


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = []
        for raw in csv.DictReader(handle):
            row = {}
            for key, value in raw.items():
                if key is None:
                    own = raw.get("__extra__")
                    log(f"  ! {path.name} 有一行字段数多于表头，多余部分已忽略: {own}")
                    continue
                if isinstance(value, list):
                    value = value[0] if value else ""
                row[key.strip()] = (value or "").strip()
            if any(row.values()):
                rows.append(row)
        return rows


def build_front_matter(row: dict, field_order: list[str], skip: set[str]) -> dict:
    data: dict = {}
    for field in field_order:
        if field in skip:
            continue
        if field not in row:
            continue
        value = convert_value(field, row[field])
        if value is None or value == []:
            continue
        data[field] = value
    return data


def write_page(path: Path, front: dict, body: str, dry_run: bool) -> str:
    header = yaml.dump(
        front,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=None,
        width=10000,
    )
    content = f"---\n{header}---\n"
    if body.strip():
        content += "\n" + body.strip() + "\n"
    action = "覆盖" if path.exists() else "新建"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return action


def unique_path(directory: Path, stem: str, used: set) -> Path:
    """同名文件自动加序号，避免同名记录互相覆盖。"""
    candidate = directory / f"{stem}.md"
    index = 2
    while candidate in used:
        candidate = directory / f"{stem} ({index}).md"
        index += 1
    used.add(candidate)
    return candidate


def import_members(dry_run: bool) -> int:
    rows = read_csv(INBOX / "members.csv")
    order = [
        "name", "image", "role", "type", "seasons", "echelon", "time",
        "grade", "affiliation", "description", "award",
    ]
    used: set = set()
    count = 0
    for row in rows:
        name = row.get("name", "").strip()
        if not name:
            log("  ! members.csv 有一行缺少 name，已跳过")
            continue
        front = build_front_matter(row, order, skip=set())
        links = {
            target: row[column].strip()
            for column, target in LINK_FIELDS.items()
            if row.get(column, "").strip()
        }
        if links:
            front["links"] = links
        path = unique_path(ROOT / "_members", clean_name(name), used)
        action = write_page(path, front, row.get("body", ""), dry_run)
        log(f"  {action} _members/{path.name}")
        count += 1
    return count


def import_awards(dry_run: bool) -> int:
    rows = read_csv(INBOX / "awards.csv")
    order = ["name", "type", "prize", "date", "members", "description"]
    used: set = set()
    count = 0
    for row in rows:
        name = row.get("name", "").strip()
        if not name:
            log("  ! awards.csv 有一行缺少 name，已跳过")
            continue
        front = build_front_matter(row, order, skip=set())
        path = unique_path(ROOT / "_awards", clean_name(name), used)
        action = write_page(path, front, row.get("body", ""), dry_run)
        log(f"  {action} _awards/{path.name}")
        count += 1
    return count


def import_events(dry_run: bool) -> int:
    rows = read_csv(INBOX / "events.csv")
    order = [
        "name", "red", "blue", "red_score", "blue_score",
        "red_logo", "blue_logo", "date", "link",
    ]
    used: set = set()
    count = 0
    for row in rows:
        name = row.get("name", "").strip()
        if not name:
            log("  ! events.csv 有一行缺少 name，已跳过")
            continue
        front = build_front_matter(row, order, skip=set())
        path = unique_path(ROOT / "_events", clean_name(name), used)
        action = write_page(path, front, row.get("body", ""), dry_run)
        log(f"  {action} _events/{path.name}")
        count += 1
    return count


def import_collection(csv_name: str, folder: str, order: list[str], dry_run: bool) -> int:
    rows = read_csv(INBOX / csv_name)
    used: set = set()
    count = 0
    for row in rows:
        name = (row.get("name") or row.get("title") or "").strip()
        if not name:
            log(f"  ! {csv_name} 有一行缺少 name/title，已跳过")
            continue
        front = build_front_matter(row, order, skip=set())
        path = unique_path(ROOT / folder, clean_name(name), used)
        action = write_page(path, front, row.get("body", ""), dry_run)
        log(f"  {action} {folder}/{path.name}")
        count += 1
    return count


def import_news(dry_run: bool) -> int:
    rows = read_csv(INBOX / "news.csv")
    used: set = set()
    count = 0
    for row in rows:
        title = row.get("title", "").strip()
        date = row.get("date", "").strip()
        if not title:
            log("  ! news.csv 有一行缺少 title，已跳过")
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            log(f"  ! news.csv「{title}」的 date 需为 YYYY-MM-DD，已跳过")
            continue
        front = {"title": title, "date": date}
        if row.get("author", "").strip():
            front["author"] = row["author"].strip()
        tags = split_multi(row.get("tags", ""))
        if tags:
            front["tags"] = tags
        path = unique_path(ROOT / "_news", f"{date}-{clean_name(title)[:40]}", used)
        action = write_page(path, front, row.get("body", row.get("summary", "")), dry_run)
        log(f"  {action} _news/{path.name}")
        count += 1
    return count


def report_site() -> None:
    rows = read_csv(INBOX / "site.csv")
    if not rows:
        return
    log("\nsite.csv 需要手工应用到 _config.yaml / contact，当前值：")
    for row in rows:
        log(f"  {row.get('key', ''):<22} {row.get('value', '')}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="把 data-inbox 的 CSV 转成 Jekyll 内容文件")
    parser.add_argument("--write", action="store_true", help="真正写入文件（默认仅演练）")
    parser.add_argument(
        "--only",
        default="",
        help="只处理指定集合，逗号分隔：members,awards,events,news,projects,patents",
    )
    args = parser.parse_args()
    dry_run = not args.write
    only = {item.strip() for item in args.only.split(",") if item.strip()}

    def selected(name: str) -> bool:
        return not only or name in only

    if not INBOX.is_dir():
        log(f"找不到 {INBOX}")
        return 1

    log("演练模式（不会写文件），加 --write 才会真正写入\n" if dry_run else "写入模式\n")

    total = 0
    if selected("members"):
        log("members:")
        total += import_members(dry_run)
    if selected("awards"):
        log("awards:")
        total += import_awards(dry_run)
    if selected("events"):
        log("events:")
        total += import_events(dry_run)
    if selected("news"):
        log("news:")
        total += import_news(dry_run)
    if selected("projects"):
        log("projects:")
        total += import_collection(
            "projects.csv", "_projects", ["name", "type", "date", "members", "description"], dry_run
        )
    if selected("patents"):
        log("patents:")
        total += import_collection(
            "patents.csv", "_patents", ["name", "ID", "type", "members"], dry_run
        )

    report_site()
    log(f"\n共处理 {total} 条记录")
    if dry_run:
        log("确认无误后执行: python tools/import_content.py --write")
    else:
        log("下一步: python tools/validate_content.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
