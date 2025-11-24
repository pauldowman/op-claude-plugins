---
name: list-recent-dispute-games
description: List dispute games created in the last 24 hours on an OP Stack chain
allowed-tools: Bash(cast:*)
---

# List Recent Dispute Games

List dispute games created in the last 24 hours on an OP Stack chain.

## Prerequisites

This skill requires the `cast` command from Foundry. If not available, Claude should suggest running the `check-op-stack-skill-setup` skill or provide installation instructions.

## Steps

1. Use the `list-rpc-urls` skill to find the RPC URL to use.
2. Get DisputeGameFactoryProxy address from the superchain registry (on L1)
3. Calculate starting block: `latest_block - (86400 / block_time)`
   - 86400 seconds in 24 hours
   - Block time is available from superchain registry
4. Check the DisputeGameFactory ABI to find the signature for the `DisputeGameCreated` event
5. Get logs for DisputeGameCreated events:
```bash
cast logs --from-block <START_BLOCK> \
  --address <DISPUTE_GAME_FACTORY> \
  <DISPUTE_GAME_CREATED_SIGNATURE> \
  --rpc-url <L1_RPC_URL>
```
6. Topic 1 (second array item) contains the dispute game address
