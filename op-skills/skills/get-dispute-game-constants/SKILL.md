---
name: get-dispute-game-constants
description: Fetch dispute game constants from Optimism's Types.sol file
allowed-tools: Bash(./get-dispute-game-constants.sh:*)
---

# Get Dispute Game Constants

Fetch dispute game constants from Optimism's Types.sol file.

## Usage

```bash
./get-dispute-game-constants.sh [tag]
```

## Parameters

- `tag`: Optional git tag (e.g., op-contracts/v4.0.0-rc.8). Defaults to develop branch.

## Output

Returns the Types.sol file which defines:
- GameStatus enum
- GameType constants
- BondDistribution types
- Other dispute game type definitions
