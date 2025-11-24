#!/bin/bash

# Script to fetch dispute game constants from Optimism's Types.sol file
# Usage: get-dispute-game-constants.sh [tag]
# Example: get-dispute-game-constants.sh
# Example: get-dispute-game-constants.sh op-contracts/v4.0.0-rc.8

set -euo pipefail

TAG="${1:-}"

if [ -n "$TAG" ]; then
    URL="https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/tags/${TAG}/packages/contracts-bedrock/src/dispute/lib/Types.sol"
else
    URL="https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/src/dispute/lib/Types.sol"
fi

# Fetch the file
RESPONSE=$(curl -sf "$URL" 2>&1) || {
    HTTP_CODE=$?
    if [ $HTTP_CODE -eq 22 ]; then
        TAG_MSG="${TAG:-develop}"
        echo "Error: Types.sol file not found (tag: ${TAG_MSG})" >&2
        exit 1
    else
        echo "Error: Failed to fetch Types.sol: $RESPONSE" >&2
        exit 1
    fi
}

echo "$RESPONSE"
