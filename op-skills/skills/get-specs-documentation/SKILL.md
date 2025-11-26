---
name: get-specs-documentation
description: Fetch documentation pages from the Optimism specs repository
allowed-tools: WebFetch(domain:raw.githubusercontent.com)
---

# Get Specs Documentation

Fetch documentation pages from the Optimism specs repository by fetching URLs directly.

## Instructions

Fetch the documentation page from:
```
https://raw.githubusercontent.com/ethereum-optimism/specs/refs/heads/main/specs/{page}
```

Where `{page}` is the page path (e.g., `protocol/deposits.md`, `fault-proof/index.md`). If no page is specified, use `SUMMARY.md` (table of contents).

## Output

The output is in Markdown format.
