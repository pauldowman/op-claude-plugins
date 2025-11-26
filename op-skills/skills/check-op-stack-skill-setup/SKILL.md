---
name: check-op-stack-skill-setup
description: Verify that required tools and repository paths are configured correctly for OP Stack skills
allowed-tools: Bash(cast:*), Bash(curl:*), Bash(ls:*), Bash(echo:*)
---

## What to Check

### Optional Repository Paths
The following paths can be specified with env vars. If the env vars are not set, prompt the user for the values, and tell them that they can set the env vars.
- **op-workbench**: Path to op-workbench repository (for RPC URL lookups) can optionally be specified with the env var `$OP_WORKBENCH_PATH`
- **k8s repository**: Path to k8s repository (for network label lookups) can optionally be specified with the env var `$K8S_REPO_PATH`

## Verification Steps

```bash
# Check required tools
cast --version
curl --version

# Verify repository paths exist
ls -ld "$OP_WORKBENCH_PATH"
ls -ld "$K8S_REPO_PATH"

# Check op-workbench
cd "$OP_WORKBENCH_PATH"
./op --help

```

## Common Issues

- **cast not found**: Install Foundry.
- **op-workbench not working**: Ensure dependencies are installed with `mise`, and that the mise config is trusted.
