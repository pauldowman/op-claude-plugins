---
name: get-prestates
description: Fetch standard prestates configuration from the Optimism Superchain Registry
allowed-tools: Bash(./get-prestates.sh:*)
---

# Get Standard Prestates

Fetch standard prestates configuration from the Optimism Superchain Registry.

## Usage

```bash
./get-prestates.sh
```

## Output

Returns prestates configuration in TOML format, including:
- `latest_stable`: Latest stable version
- `latest_rc`: Latest release candidate
- Prestate hashes for different types (cannon64, interop, etc.)
