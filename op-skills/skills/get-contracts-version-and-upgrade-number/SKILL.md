---
name: get-contracts-version-and-upgrade-number
description: Get the op-contracts version number and the upgrade number for an OP Stack chain
allowed-tools: Bash(cast:*, curl:*)
---

1. Get the L1 node RPC URL using the `get-rpc-urls` skill.
2. Find the `SystemConfigProxy` address for the chain using the `get-chain-config` skill.
3. Using `cast implementation`, find the address of the implementation contract.
5. The TOML file at https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/refs/heads/main/validation/standard/standard-versions-{L1_NETWORK}.toml contains a mapping that will show which op-contracts release tag contains the address of the implementation contract, where L1_NETWORK is either `mainnet` or `sepolia`.
    - The section header (e.g. `["op-contracts/vX.Y.Z"]`) is the overall contracts version (corresponding to a git tag in the optimism repo)
    - The comment above gives the upgrade number, AKA release version (e.g. "Upgrade 17").

