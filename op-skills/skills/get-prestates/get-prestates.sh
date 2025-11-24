#!/bin/bash

# Script to fetch standard prestates configuration from the Optimism Superchain Registry
# Usage: get-prestates.sh
# Note: Outputs raw TOML format

set -euo pipefail

URL="https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/refs/heads/main/validation/standard/standard-prestates.toml"

# Fetch and output the TOML file
curl -sf "$URL" || {
    HTTP_CODE=$?
    if [ $HTTP_CODE -eq 22 ]; then
        echo "Error: Standard prestates configuration not found" >&2
        exit 1
    else
        echo "Error: Failed to fetch standard prestates" >&2
        exit 1
    fi
}
