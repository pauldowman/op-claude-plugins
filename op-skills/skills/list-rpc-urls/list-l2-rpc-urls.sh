#!/bin/bash

# Script to list RPC URLs for a specific OP Stack L2 network using op-workbench

set -euo pipefail

if [ $# -ne 3 ]; then
    echo "Error: Missing required arguments" >&2
    echo "Usage: $0 <k8s_network_label> <node_type> <op_workbench_repo_path>" >&2
    echo "Example: $0 mainnet-prod op-node /path/to/op-workbench" >&2
    echo "Example: $0 base-sepolia-dev op-geth /path/to/op-workbench" >&2
    exit 1
fi

K8S_NETWORK_LABEL="$1"
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

if ! gcloud auth application-default print-access-token &>/dev/null; then
    echo "Error: gcloud is not logged in. Please run 'gcloud auth application-default login' to authenticate." >&2
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

# Run the command
./op urls all --network="$K8S_NETWORK_LABEL" "$NODE_TYPE" || {
    echo "Error: Failed to get RPC URLs for network=$K8S_NETWORK_LABEL, node_type=$NODE_TYPE" >&2
    exit 1
}
