---
name: get-contract-abi
description: Get the ABI for Optimism contracts from the contracts-bedrock snapshots
allowed-tools: Bash(./get-abi.sh:*)
---

# Get Contract ABI

Get the ABI for Optimism contracts from the contracts-bedrock snapshots.

## Usage

```bash
./get-abi.sh <contract_name> [tag]
```

## Parameters

- `contract_name`: Name of the contract (e.g., L1StandardBridge, OptimismPortal, FaultDisputeGame)
- `tag`: Optional git tag (e.g., op-contracts/v4.0.0-rc.8). Defaults to develop branch.

## Output

The output is in JSON format.
