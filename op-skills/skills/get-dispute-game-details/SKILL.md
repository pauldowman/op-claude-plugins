---
name: get-dispute-game-details
description: Get details about a specific dispute game contract
allowed-tools: Bash(cast:*)
---

# Get Dispute Game Details

Get details about a specific dispute game contract.

## Prerequisites

This skill requires the `cast` command from Foundry. If not available, Claude should suggest running the `check-op-stack-skill-setup` skill or provide installation instructions.

## Overview

Dispute games are contracts deployed on L1 (mainnet or sepolia), not L2. Each is a proxy contract.

## Steps

1. Use the `list-rpc-urls` skill to find the RPC URL to use.
1. Determine the contract name based on dispute game type:
   - `FaultDisputeGame` (permissionless)
   - `PermissionedDisputeGame` (permissioned)
   - `SuperFaultDisputeGame` (interop-enabled permissionless)
   - `SuperPermissionedDisputeGame` (interop-enabled permissioned)
2. Get the ABI
3. Call methods using `cast call <GAME_ADDRESS> "<METHOD>()" --rpc-url <L1_RPC_URL>`
4. For constants, use the `get-dispute-game-constants` skill
5. For more context, see Optimism specs using the `get-specs-documentation` skill
