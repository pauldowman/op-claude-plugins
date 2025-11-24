---
name: verify-dispute-game-absolute-prestate
description: Verify that a dispute game's absolute prestate matches standard prestates
allowed-tools: Bash(cast:*), Bash(grep:*)
---

# Verify Dispute Game Absolute Prestate

Verify that a dispute game's absolute prestate matches standard prestates.

## Prerequisites

This skill requires the `cast` command from Foundry. If not available, Claude should suggest running the `check-op-stack-skill-setup` skill or provide installation instructions.

## Steps

1. Use the `list-rpc-urls` skill to find the RPC URL to use.
2. Get `absolutePrestate` from the game:
```bash
cast call <GAME_ADDRESS> "absolutePrestate()" --rpc-url <L1_RPC_URL>
```

3. Fetch standard prestates using the `get-prestates` skill

4. Check if the prestate hash matches one in the standard prestates:
   - For 64-bit Cannon: look for "cannon64" type
   - For Interop: look for "interop" type

5. Check if it matches `latest_stable` or `latest_rc` version
