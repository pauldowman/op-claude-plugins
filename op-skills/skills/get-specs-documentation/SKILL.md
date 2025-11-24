---
name: get-specs-documentation
description: Fetch documentation pages from the Optimism specs repository
allowed-tools: Bash(./get-specs-page.sh:*)
---

# Get Specs Documentation

Fetch documentation pages from the Optimism specs repository.

## Usage

```bash
./get-specs-page.sh [page]
```

## Parameters

- `page`: Page path (e.g., protocol/deposits.md, fault-proof/index.md). Defaults to SUMMARY.md (table of contents).

## Output

The output is in Markdown format.
