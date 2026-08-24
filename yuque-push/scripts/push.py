#!/usr/bin/env python3
"""发布 markdown 文档到语雀（upsert：存在则更新，不存在则创建）。

凭证从本技能目录的 .env 读取（YUQUE_TOKEN / YUQUE_NAMESPACE / YUQUE_PARENT_UUID），
也可用 --token/--namespace/--parent-uuid 临时覆盖。

用法:
    python push.py [--file 文档.md]
默认文件: ~/.zcode/workspace/default 下最新的 周报-*.md
"""
import argparse
import glob
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://www.yuque.com/api/v2"
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_WORKSPACE = os.path.expanduser("~/.zcode/workspace/default")


def load_env():
    env = {}
    path = os.path.join(SKILL_DIR, ".env")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip()
    return env


def api(path, token, method="GET", body=None):
    req = urllib.request.Request(
        f"{API_BASE}{urllib.parse.quote(path, safe='/:?=&')}",
        method=method,
        headers={
            "X-Auth-Token": token,
            "User-Agent": "zcode-yuque-push/1.0",
            "Content-Type": "application/json",
        },
        data=json.dumps(body).encode("utf-8") if body is not None else None,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "ignore")
        try:
            return e.code, json.loads(raw or "{}")
        except json.JSONDecodeError:
            return e.code, {"message": raw}


def main():
    env = load_env()
    ap = argparse.ArgumentParser(description="发布文档到语雀")
    ap.add_argument("--file", help="markdown 文件路径（默认：workspace 下最新 周报-*.md）")
    ap.add_argument("--token", default=env.get("YUQUE_TOKEN", ""))
    ap.add_argument("--namespace", default=env.get("YUQUE_NAMESPACE", ""))
    ap.add_argument("--parent-uuid", default=env.get("YUQUE_PARENT_UUID", ""))
    args = ap.parse_args()

    if not (args.token and args.namespace):
        print("缺少凭证：请确认 skill 目录下的 .env 配置了 YUQUE_TOKEN 与 YUQUE_NAMESPACE")
        sys.exit(1)

    if args.file:
        path = args.file
    else:
        matches = sorted(glob.glob(os.path.join(DEFAULT_WORKSPACE, "周报-*.md")))
        if not matches:
            print(f"未在 {DEFAULT_WORKSPACE} 找到 周报-*.md 文件")
            sys.exit(1)
        path = matches[-1]

    with open(path, encoding="utf-8") as f:
        content = f.read()
    title = next((ln[2:].strip() for ln in content.splitlines() if ln.startswith("# ")),
                 os.path.basename(path))
    # slug 仅允许 [\w\-\.]，从文件名提取日期部分，如 周报-2026-08-14 → weekly-report-2026-08-14
    import re
    m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
    slug = f"weekly-report-{m.group(1)}" if m else "weekly-report"

    # 已存在则更新；404 则创建（创建时保留固定 slug 以便下次更新命中；创建后再挂到目标目录，POST 接口本身不支持 parentUuid）
    payload = {"title": title, "slug": slug, "format": "markdown", "body": content}
    status, data = api(f"/repos/{args.namespace}/docs/{slug}", args.token, "PUT", payload)
    if status == 404:
        status, data = api(f"/repos/{args.namespace}/docs", args.token, "POST", payload)
        if status in (200, 201) and args.parent_uuid:
            doc_id = (data.get("data") or {}).get("id")
            st2, r2 = api(f"/repos/{args.namespace}/toc", args.token, "PUT", {
                "action": "appendNode",
                "action_mode": "child",
                "target_uuid": args.parent_uuid,
                "type": "DOC",
                "doc_ids": [doc_id],
            })
            if st2 not in (200, 204):
                print(f"文档已创建但挂载目录失败（HTTP {st2}）：{r2}")
                sys.exit(1)
    if status not in (200, 201):
        print(f"发布失败（HTTP {status}）：{data}")
        sys.exit(1)

    url = (data.get("data") or {}).get("url") if isinstance(data, dict) else None
    print(f"已发布到语雀：{url or data}")


if __name__ == "__main__":
    main()
