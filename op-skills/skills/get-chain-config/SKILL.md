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

1. Determine L1_CHAIN, which will be `mainnet` or `sepolia`
2. Determine L2_CHAIN, which will be a lowercase identifier, probably using `-` for the separator, for example `op`, `base`, `unichain` or `arena-z`.
3. Fetch https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/main/superchain/configs/{L1_CHAIN}/{L2_CHAIN}.toml which is a TOML formatted file containing chain config info, such as chain ID, RPC URLs, contract addresses, hardfork times, and other chain parameters.
