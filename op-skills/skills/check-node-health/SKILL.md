---
name: check-node-health
description: Check the health of op-geth, op-node, or L1 geth nodes
allowed-tools: Bash(cast:*)
---

# Check Node Health

Check the health of op-geth, op-node, or L1 geth nodes.

## Prerequisites

This skill requires the `cast` command from Foundry. If `cast` is not available, Claude should:
1. Inform the user that Foundry needs to be installed
2. Suggest running the `check-op-stack-skill-setup` skill to verify installation
3. Provide installation instructions: `curl -L https://foundry.paradigm.xyz | bash`

## Steps

### 1. Get RPC URL

Use the `list-rpc-urls` skill to find the RPC URL to use.

### 2. Basic Health Check

**For op-geth or L1 geth:**
```bash
cast block-number --rpc-url <RPC_URL>
```

**For op-node:**
```bash
cast rpc optimism_syncStatus --rpc-url <RPC_URL>
```

### 3. Advanced Health Check

**For op-geth or L1 geth:**
```bash
cast rpc eth_syncing --rpc-url <RPC_URL>
```
Should return `false` if fully synced.

**For op-node:**
```bash
# Get latest block from op-geth
LATEST=$(cast block-number --rpc-url <OP_GETH_RPC_URL>)
# Convert to hex
LATEST_HEX=$(cast 2h $LATEST)
# Check output at that block
cast rpc optimism_outputAtBlock $LATEST_HEX --rpc-url <OP_NODE_RPC_URL>
```
