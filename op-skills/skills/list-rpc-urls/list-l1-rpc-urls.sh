#!/bin/bash

# Script to list RPC URLs for a specific Ethereum L1 network using op-workbench
# Usage: list-l1-rpc-urls.sh <network> <node_type> <op_workbench_repo_path>
# Example: list-l1-rpc-urls.sh mainnet geth /path/to/op-workbench
# Example: list-l1-rpc-urls.sh sepolia lighthouse /path/to/op-workbench

set -euo pipefail

if [ $# -ne 3 ]; then
    echo "Error: Missing required arguments" >&2
    echo "Usage: $0 <network> <node_type> <op_workbench_repo_path>" >&2
    echo "Example: $0 mainnet geth /path/to/op-workbench" >&2
    echo "Example: $0 sepolia lighthouse /path/to/op-workbench" >&2
    exit 1
fi

NETWORK="$1"
NODE_TYPE="$2"
OP_WORKBENCH_PATH="$3"

if [ ! -d "$OP_WORKBENCH_PATH" ]; then
    echo "Error: op-workbench directory not found: $OP_WORKBENCH_PATH" >&2
    exit 1
fi

# Check if tailscale is available and running
if ! command -v tailscale &> /dev/null; then
    echo "Error: tailscale command not found. Please install Tailscale (or install the Tailscale CLI from the Tailscale app settings dialog)." >&2
    exit 1
fi

TAILSCALE_STATUS=$(tailscale status 2>&1) || {
    echo "Error: Tailscale needs to be running to access RPC URLs." >&2
    exit 1
}

if echo "$TAILSCALE_STATUS" | grep -q "Tailscale is stopped"; then
    echo "Error: Tailscale is stopped. Please start Tailscale to access RPC URLs." >&2
    exit 1
fi

# Change to op-workbench directory and run the command
cd "$OP_WORKBENCH_PATH"

# Check if mise is available
if ! command -v mise &> /dev/null; then
    echo "Error: mise not found in PATH. Please install mise." >&2
    exit 1
fi

# Activate mise to ensure correct environment (Python, etc.)
eval "$(mise activate bash)"

if [ ! -x "./op" ]; then
    echo "Error: ./op script not found or not executable in $OP_WORKBENCH_PATH" >&2
    exit 1
fi

# Run the command and filter results
./op urls all | grep "${NETWORK}-l1" | grep "$NODE_TYPE" || {
    echo "Error: No RPC URLs found for network=$NETWORK, node_type=$NODE_TYPE" >&2
    exit 1
}
