---
name: get-chain-config
description: Get configuration for an OP Stack chain from the Optimism Superchain Registry
allowed-tools: Bash(./get-chain-config.sh:*)
---

# Get Chain Configuration

Get configuration for an OP Stack chain from the Optimism Superchain Registry.

## Usage

```bash
./get-chain-config.sh <l1_chain> <l2_chain>
```

## Parameters

- `l1_chain`: L1 network (e.g., mainnet, sepolia)
- `l2_chain`: L2 chain identifier (e.g., op, base, ink)

## Output

The output is in TOML format and includes chain ID, RPC URLs, contract addresses, hardfork times, and other chain parameters.
