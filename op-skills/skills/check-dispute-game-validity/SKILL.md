---
name: check-dispute-game-validity
description: Check if a dispute game's root claim matches the actual output root
allowed-tools: Bash(cast:*)
---

## Prerequisites

This skill requires the `cast` command from Foundry. If not available, Claude should suggest running the `check-op-stack-skill-setup` skill or provide installation instructions.

## Steps

1. Use the `list-rpc-urls` skill to find the RPC URL to use.
2. Get `rootClaim` from the dispute game: `cast call <GAME_ADDRESS> "rootClaim()" --rpc-url <L1_RPC_URL>`
3. Get `l2BlockNumber` from the dispute game: `cast call <GAME_ADDRESS> "l2BlockNumber()" --rpc-url <L1_RPC_URL>`
4. Convert L2 block to hex: `cast 2h <L2_BLOCK_NUMBER>`
5. Get output root from op-node:
```bash
cast rpc optimism_outputAtBlock <L2_BLOCK_HEX> --rpc-url <OP_NODE_RPC_URL>
```
6. Compare `outputRoot` from step 4 with `rootClaim` from step 1
   - If they match: game is valid
   - If they don't match: game is invalid
