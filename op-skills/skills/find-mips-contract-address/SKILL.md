---
name: find-mips-contract-address
description: Find the MIPS contract address used by dispute games on an OP Stack chain
allowed-tools: Bash(cast:*)
---

# Find MIPS Contract Address

Find the MIPS contract address used by dispute games on an OP Stack chain.

## Prerequisites

This skill requires the `cast` command from Foundry. If not available, Claude should suggest running the `check-op-stack-skill-setup` skill or provide installation instructions.

## Steps

Navigate from SystemConfigProxy to find the MIPS contract:

1. Use the `list-rpc-urls` skill to find the RPC URL to use.
2. Get DisputeGameFactory address: `cast call <SYSTEM_CONFIG_PROXY> "disputeGameFactory()" --rpc-url <RPC_URL>`
3. Get FaultDisputeGame address: `cast call <DISPUTE_GAME_FACTORY> "gameImpls(uint32)" 0 --rpc-url <RPC_URL>`
4. Get MIPS contract address: `cast call <FAULT_DISPUTE_GAME> "vm()" --rpc-url <RPC_URL>`

For PermissionedDisputeGame, use the same process but call `gameImpls(1)` instead of `gameImpls(0)` in step 2.
