#!/bin/bash

# Script to get chain configuration from Optimism superchain registry
# Usage: get-chain-config.sh <l1_chain> <l2_chain>
# Example: get-chain-config.sh mainnet op
# Note: Outputs raw TOML format

set -euo pipefail

if [ $# -ne 2 ]; then
    echo "Error: Missing required arguments" >&2
    echo "Usage: $0 <l1_chain> <l2_chain>" >&2
    echo "Example: $0 mainnet op" >&2
    exit 1
fi

L1_CHAIN="$1"
L2_CHAIN="$2"

URL="https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/main/superchain/configs/${L1_CHAIN}/${L2_CHAIN}.toml"

# Fetch and output the TOML file
curl -sf "$URL" || {
    HTTP_CODE=$?
    if [ $HTTP_CODE -eq 22 ]; then
        echo "Error: Chain configuration not found for ${L1_CHAIN}/${L2_CHAIN}" >&2
        exit 1
    else
        echo "Error: Failed to fetch chain configuration" >&2
        exit 1
    fi
}
