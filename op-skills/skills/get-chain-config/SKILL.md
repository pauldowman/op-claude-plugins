---
name: get-chain-config
description: Get configuration for an OP Stack chain from the Optimism Superchain Registry
allowed-tools: Bash(curl:*)
---

1. Determine L1_CHAIN, which will be `mainnet` or `sepolia`
2. Determine L2_CHAIN, which will be a lowercase identifier, probably using `-` for the separator, for example `op`, `base`, `unichain` or `arena-z`.
3. Fetch https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/main/superchain/configs/{L1_CHAIN}/{L2_CHAIN}.toml which is a TOML formatted file containing chain config info, such as chain ID, RPC URLs, contract addresses, hardfork times, and other chain parameters.
