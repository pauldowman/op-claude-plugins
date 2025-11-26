---
name: get-dispute-game-constants
description: Fetch dispute game constants from Optimism's Types.sol file
allowed-tools: Bash(curl:*)
---

# Get Dispute Game Constants

Fetch dispute game constants from Optimism's Types.sol file by fetching the URL directly.

## Instructions

Fetch the Types.sol file from:
- For a specific tag: `https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/tags/{tag}/packages/contracts-bedrock/src/dispute/lib/Types.sol`
- For develop branch: `https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/src/dispute/lib/Types.sol`

Where `{tag}` is a git tag (e.g., `op-contracts/v4.0.0-rc.8`). If no tag is specified, use the develop branch.

## Output

Returns the Types.sol file which defines:
- GameStatus enum
- GameType constants
- BondDistribution types
- Other dispute game type definitions
