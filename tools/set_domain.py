#!/usr/bin/env python3
"""把自定义域名接到站点上。

用法：
    python tools/set_domain.py www.spr-robomaster.com   # 配置域名
    python tools/set_domain.py --clear                  # 撤销域名，回到 github.io

原理：本站是「Actions 构建后 push gh-pages」的发布方式，GitHub Pages 从
产物根目录的 CNAME 文件读取自定义域名。源码根目录放 CNAME，Jekyll 会原样
拷贝进 _site，所以每次部署都不会丢。

注意：一定要先在阿里云把域名解析配好、并且在 GitHub 的 Pages 设置里填好域名，
再运行本脚本，否则站点会立刻切到一个还打不开的域名上。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CNAME = ROOT / "CNAME"

GITHUB_PAGES_A = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
]
GITHUB_PAGES_AAAA = [
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153",
]
PAGES_HOST = "darkcome6.github.io"


def normalize(value: str) -> str:
    domain = value.strip().lower()
    domain = re.sub(r"^https?://", "", domain).rstrip("/")
    return domain


def valid(domain: str) -> bool:
    if "://" in domain or "/" in domain:
        return False
    return bool(re.fullmatch(r"(?!-)[a-z0-9-]{1,63}(?<!-)(\.(?!-)[a-z0-9-]{1,63}(?<!-))+", domain))


def print_dns(domain: str) -> None:
    apex = domain[4:] if domain.startswith("www.") else domain
    print("\n在阿里云「域名控制台 → 解析设置」里加这些记录（其余全部删掉，不要加泛解析）：\n")
    print(f"  {'类型':<6}{'主机记录':<10}{'记录值'}")
    print(f"  {'-' * 6}{'-' * 10}{'-' * 34}")
    for ip in GITHUB_PAGES_A:
        print(f"  {'A':<6}{'@':<12}{ip}")
    for ip in GITHUB_PAGES_AAAA:
        print(f"  {'AAAA':<6}{'@':<12}{ip}")
    print(f"  {'CNAME':<6}{'www':<12}{PAGES_HOST}")
    print("\n  说明：apex 用 4 条 A + 4 条 AAAA，www 的 CNAME 直接指 github.io。")
    print(f"  想直接用裸域名访问，就把 Pages 设置里的域名填成 {apex}，www 会自动 301 过去。\n")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 1

    arg = sys.argv[1]

    if arg in ("--clear", "-c"):
        if CNAME.is_file():
            CNAME.unlink()
            print("已删除 CNAME。记得同步清掉 GitHub 的 Pages 自定义域名，否则会 404。")
        else:
            print("没有 CNAME 文件，无需操作。")
        return 0

    domain = normalize(arg)
    if not valid(domain):
        print(f"域名格式不对：{arg}\n只写裸域名，例如 www.spr-robomaster.com 或 spr-robomaster.com")
        return 1

    CNAME.write_text(domain + "\n", encoding="utf-8")
    print(f"已写入 CNAME：{domain}")

    print_dns(domain)
    print("接着做：")
    print("  1. 仓库 Settings → Pages → Custom domain 填同一个域名并 Save")
    print("  2. 等证书签发（几分钟到 1 小时），勾选 Enforce HTTPS")
    print("  3. 推送后确认线上 https://<域名> 能打开，再检查一遍站内链接")
    return 0


if __name__ == "__main__":
    sys.exit(main())