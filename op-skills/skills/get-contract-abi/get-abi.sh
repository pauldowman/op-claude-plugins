#!/bin/bash

# Script to get contract ABI from Optimism's contracts-bedrock snapshots
# Usage: get-abi.sh <contract_name> [tag]
# Example: get-abi.sh L1StandardBridge
# Example: get-abi.sh OptimismPortal op-contracts/v4.0.0-rc.8

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Error: Missing required argument" >&2
    echo "Usage: $0 <contract_name> [tag]" >&2
    echo "Example: $0 L1StandardBridge" >&2
    echo "Example: $0 OptimismPortal op-contracts/v4.0.0-rc.8" >&2
    exit 1
fi

CONTRACT_NAME="$1"
TAG="${2:-}"

if [ -n "$TAG" ]; then
    URL="https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/tags/${TAG}/packages/contracts-bedrock/snapshots/abi/${CONTRACT_NAME}.json"
else
    URL="https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/snapshots/abi/${CONTRACT_NAME}.json"
fi

# Fetch and format the JSON
RESPONSE=$(curl -sf "$URL" 2>&1) || {
    HTTP_CODE=$?
    if [ $HTTP_CODE -eq 22 ]; then
        echo "Error: ABI not found for contract '${CONTRACT_NAME}'" >&2
        exit 1
    else
        echo "Error: Failed to fetch ABI: $RESPONSE" >&2
        exit 1
    fi
}

echo "$RESPONSE"
