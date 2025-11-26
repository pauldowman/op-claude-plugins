---
name: list-rpc-urls
description: Get RPC URLs for the op-geth or op-node for an OP Stack chain, or for Ethereum or Sepolia
allowed-tools: Bash(skills/list-rpc-urls/list-network-values.sh:*), Bash(skills/list-rpc-urls/list-l1-rpc-urls.sh:*), Bash(skills/list-rpc-urls/list-l2-rpc-urls.sh:*)
---

# List RPC URLs

Get RPC URLs for OP Stack L2 chains (op-geth or op-node) or Ethereum L1 networks (geth or lighthouse/consensus nodes).

## Overview

This skill provides access to RPC URLs for nodes running in the Optimism infrastructure. There are three main use cases:

1. **List available network labels** - Find valid k8s network labels for L2 chains
2. **Get L1 RPC URLs** - Get Ethereum mainnet or Sepolia node URLs
3. **Get L2 RPC URLs** - Get OP Stack chain node URLs (op-geth or op-node)

## Configuration

This skill requires paths to local repositories. Claude should prompt the user for these paths if they are not already known:

- **op_workbench_repo_path**: Path to the op-workbench repository (required for getting RPC URLs)
  - Example: `/Users/username/repos/op-workbench`
  - Can also be set via environment variable: `$OP_WORKBENCH_PATH`
  
- **k8s_repo_path**: Path to the k8s repository (required for listing network labels only)
  - Example: `/Users/username/repos/k8s`
  - Can also be set via environment variable: `$K8S_REPO_PATH`

**When to prompt**: If the user asks for RPC URLs or network labels without providing these paths, Claude should ask the user for the appropriate path(s) and remember them for the current conversation session.

## Usage

### 1. List Available Network Labels

Before querying L2 RPC URLs, use this to discover valid k8s network labels:

```bash
skills/list-rpc-urls/list-network-values.sh <k8s_repo_path>
```

**Output**: Lists all available network labels categorized by environment type (dev, prod, other).

**Example output**:
```
Development environments (-dev): 5
Production environments (-prod): 12
Other environments: 2

Development environments:
  base-sepolia-dev
  mainnet-dev
  ...

Production environments:
  mainnet-prod
  base-mainnet-prod
  ...
```

### 2. Get L1 RPC URLs

Get RPC URLs for Ethereum mainnet or Sepolia nodes:

```bash
skills/list-rpc-urls/list-l1-rpc-urls.sh <network> <node_type> <op_workbench_repo_path>
```

**Parameters**:
- `network`: L1 network name (`mainnet` or `sepolia`)
- `node_type`: Type of node (`geth` for execution layer, or `lighthouse` for consensus layer)
- `op_workbench_repo_path`: Path to op-workbench repository

**Examples**:
```bash
# Get Ethereum mainnet geth URLs
skills/list-rpc-urls/list-l1-rpc-urls.sh mainnet geth /path/to/op-workbench

# Get Sepolia lighthouse/consensus URLs
skills/list-rpc-urls/list-l1-rpc-urls.sh sepolia lighthouse /path/to/op-workbench
```

### 3. Get L2 RPC URLs

Get RPC URLs for OP Stack L2 chain nodes:

```bash
./list-l2-rpc-urls.sh <k8s_network_label> <node_type> <op_workbench_repo_path>
```

**Parameters**:
- `k8s_network_label`: The network label from k8s (use list-network-values.sh to find valid labels)
- `node_type`: Type of node (`op-geth` for execution layer, or `op-node` for rollup node)
- `op_workbench_repo_path`: Path to op-workbench repository

**Examples**:
```bash
# Get op-node URLs for mainnet production
./list-l2-rpc-urls.sh mainnet-prod op-node /path/to/op-workbench

# Get op-geth URLs for Base Sepolia development
./list-l2-rpc-urls.sh base-sepolia-dev op-geth /path/to/op-workbench
```

## Workflow

A typical workflow to get L2 RPC URLs:

1. First, list available networks: `./list-network-values.sh <k8s_repo_path>`
2. Choose a network label from the output
3. Get node URLs: `./list-l2-rpc-urls.sh <network_label> <node_type> <op_workbench_repo_path>`

## Node Types

### L1 (Ethereum)
- `geth`: Execution layer node (for transaction execution and state)
- `lighthouse`: Consensus layer node (for beacon chain and consensus)

### L2 (OP Stack)
- `op-geth`: Execution layer node (modified geth for OP Stack)
- `op-node`: Rollup node (handles L1 data derivation and sequencing)
