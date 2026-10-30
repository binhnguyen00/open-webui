#!/usr/bin/env python3
"""
Open WebUI Documentation Search Helper.
Queries https://docs.openwebui.com/api/search?q=<query> and outputs formatted results.
"""

import sys
import json
import urllib.parse
import urllib.request
import argparse

API_ENDPOINT = "https://docs.openwebui.com/api/search"
USER_AGENT = "Antigravity-OpenWebUI-Docs/1.0"


def search_docs(query: str, limit: int = 5):
    encoded_query = urllib.parse.quote(query)
    url = f"{API_ENDPOINT}?q={encoded_query}"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error querying docs API: {e}", file=sys.stderr)
        sys.exit(1)

    results = data.get("results", [])
    count = data.get("count", len(results))

    return count, results[:limit]


def main():
    parser = argparse.ArgumentParser(description="Search Open WebUI Documentation")
    parser.add_argument("query", nargs="+", help="Search query string")
    parser.add_argument("-n", "--limit", type=int, default=5, help="Max results to return (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")

    args = parser.parse_args()
    query_str = " ".join(args.query)

    total_count, results = search_docs(query_str, limit=args.limit)

    if args.json:
        print(json.dumps({"query": query_str, "total": total_count, "results": results}, indent=2, ensure_ascii=False))
        return

    print(f"=== Open WebUI Docs Search: '{query_str}' (Found {total_count} results, showing top {len(results)}) ===\n")
    if not results:
        print("No matching documentation pages found.")
        return

    for idx, item in enumerate(results, start=1):
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        markdown_url = item.get("markdown_url", "")
        snippet = item.get("snippet", "").strip()
        score = item.get("score", 0)

        print(f"{idx}. {title} [Score: {score}]")
        print(f"   Canonical URL : {url}")
        print(f"   Markdown URL  : {markdown_url}")
        if snippet:
            print(f"   Snippet       : {snippet}")
        print()


if __name__ == "__main__":
    main()
