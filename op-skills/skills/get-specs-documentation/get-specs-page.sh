#!/bin/bash

# Script to fetch documentation pages from the Optimism specs repository
# Usage: get-specs-page.sh [page]
# Example: get-specs-page.sh
# Example: get-specs-page.sh protocol/deposits.md

set -euo pipefail

PAGE="${1:-SUMMARY.md}"

URL="https://raw.githubusercontent.com/ethereum-optimism/specs/refs/heads/main/specs/${PAGE}"

# Fetch the page
RESPONSE=$(curl -sf "$URL" 2>&1) || {
    HTTP_CODE=$?
    if [ $HTTP_CODE -eq 22 ]; then
        echo "Error: Documentation page '${PAGE}' not found" >&2
        exit 1
    else
        echo "Error: Failed to fetch documentation page: $RESPONSE" >&2
        exit 1
    fi
}

echo "$RESPONSE"
