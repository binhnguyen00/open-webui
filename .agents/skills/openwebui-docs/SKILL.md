---
name: openwebui-docs
description: >-
  Search and retrieve official Open WebUI documentation, guides, and API references.
  Activate this skill whenever the user asks about Open WebUI architecture, features, configuration,
  environment variables, Docker deployment, pipelines, functions, tools, integrations, OAuth/SSO, or troubleshooting.
---

# Open WebUI Documentation Skill

This skill allows the agent to search and fetch up-to-date, machine-readable official documentation from [docs.openwebui.com](https://docs.openwebui.com).

## 1. Entry Points & Endpoints

| Resource | URL | Purpose |
| :--- | :--- | :--- |
| **Search API** | `https://docs.openwebui.com/api/search?q=<QUERY>` | Deterministic keyword search returning JSON with scores and direct markdown links |
| **Search Script** | `[search.py](./scripts/search.py)` | Local CLI helper script to execute search directly and format results |
| **Markdown Pages** | `https://docs.openwebui.com/<path>.md` | Pure Markdown representation of any docs page (fast, token-efficient) |
| **Curated Index** | `https://docs.openwebui.com/llms.txt` | Compact listing of all documentation pages with short descriptions |
| **Full Corpus** | `https://docs.openwebui.com/llms-full.txt` | All docs concatenated into a single Markdown file |
| **Agent Guide** | `https://docs.openwebui.com/agents.txt` | Official instructions for AI agents interacting with the documentation |

---

## 2. Recommended Workflow

### Step 1: Search the Documentation
When answering questions or configuring Open WebUI, first search for the relevant topic:

- **Option A (Via Helper Script)**:
  ```bash
  python3 .agents/skills/openwebui-docs/scripts/search.py "<KEYWORD>" -n 5
  ```
- **Option B (Direct API Call)**:
  Fetch `https://docs.openwebui.com/api/search?q=<ENCODED_QUERY>` via `read_url_content` or HTTP request with a standard `User-Agent`.

### Step 2: Read Detailed Documentation
From the search results, retrieve the clean Markdown document using `markdown_url` (or by appending `.md` to the canonical URL).
- Use `read_url_content` to fetch the `.md` URL (e.g. `https://docs.openwebui.com/getting-started/env-configuration.md`).
- Do not fetch the raw HTML page if the `.md` version is available.

### Step 3: Presenting Answers & Citations
- Base your technical answers, environment variable names, and configurations on the retrieved Markdown.
- **Citation Rule**: Always cite the canonical HTML URL (e.g., `https://docs.openwebui.com/features/extensibility/mcp`) when linking references for the user. Do not cite the `.md`, `.txt`, or `api/search` endpoints directly in the final response.
