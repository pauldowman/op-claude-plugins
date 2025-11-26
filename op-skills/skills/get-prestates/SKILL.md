---
name: get-prestates
description: Fetch standard prestates configuration from the Optimism Superchain Registry
allowed-tools: WebFetch(domain:raw.githubusercontent.com)
---

# Get Standard Prestates

Fetch standard prestates configuration from the Optimism Superchain Registry by fetching the URL directly.

## Instructions

Fetch the prestates configuration from:
```
https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/refs/heads/main/validation/standard/standard-prestates.toml
```

## Output

Returns prestates configuration in TOML format, including:
- `latest_stable`: Latest stable version
- `latest_rc`: Latest release candidate
- Prestate hashes for different types (cannon64, interop, etc.)
