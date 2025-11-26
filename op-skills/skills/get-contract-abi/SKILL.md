---
name: get-contract-abi
description: Get the ABI for Optimism contracts from the contracts-bedrock snapshots
allowed-tools: WebFetch(domain:raw.githubusercontent.com)
---

# Get Contract ABI

Get the ABI for Optimism contracts from the contracts-bedrock snapshots by fetching the URL directly.

## Instructions

Fetch the contract ABI from:
- For a specific tag: `https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/tags/{tag}/packages/contracts-bedrock/snapshots/abi/{contract_name}.json`
- For develop branch: `https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/snapshots/abi/{contract_name}.json`

Where:
- `{contract_name}` is the name of the contract (e.g., `L1StandardBridge`, `OptimismPortal`, `FaultDisputeGame`)
- `{tag}` is an optional git tag (e.g., `op-contracts/v4.0.0-rc.8`). If no tag is specified, use the develop branch.

## Output

The output is in JSON format.
