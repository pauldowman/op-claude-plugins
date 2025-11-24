---
name: check-op-stack-skill-setup
description: Verify that required tools and repository paths are configured correctly for OP Stack skills
allowed-tools: Bash(cast:*), Bash(curl:*), Bash(poetry:*), Bash(ls:*)
---

# Check Setup

Verify that required tools and repository paths are configured correctly for OP Stack skills.

## What to Check

### Required Tools
1. **cast** (from Foundry): `cast --version`
2. **curl**: `curl --version`
3. **op-workbench**: Check if `./op --help` works in op-workbench directory

### Optional Repository Paths
- **op-workbench**: Path to op-workbench repository (for RPC URL lookups)
- **k8s repository**: Path to k8s repository (for network label lookups)

## Verification Steps

```bash
# Check required tools
cast --version
curl --version

# Verify repository paths exist
ls -ld /path/to/op-workbench
ls -ld /path/to/k8s-repo

# Check op-workbench (if using)
cd /path/to/op-workbench
./op --help

```

## Common Issues

- **cast not found**: Install Foundry: `curl -L https://foundry.paradigm.xyz | bash`
- **poetry not found**: Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
- **op-workbench not working**: Ensure dependencies are installed with `poetry install` in the op-workbench directory
