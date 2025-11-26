---
name: check-op-node-safe-head-db
description: Check whether the safe head database is enabled in an op-node instance
allowed-tools: Bash(cast:*)
---

## Prerequisites

This skill requires the `cast` command from Foundry. If not available, Claude should suggest running the `check-op-stack-skill-setup` skill or provide installation instructions.

## Steps

1. Use the `list-rpc-urls` skill to find the RPC URL to use.
2. Find an L1 block number from ~1 day ago (subtract ~7200 blocks from current)
3. Run `cast rpc optimism_safeHeadAtL1Block <L1_BLOCK_NUMBER> --rpc-url <OP_NODE_RPC_URL>`
4. If a valid result is returned, the safe head DB is enabled
5. If you see "safe head database not enabled" error, it's not enabled
