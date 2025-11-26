# OP Stack Skills

Claude Code skills for working with OP Stack blockchains.

## Prerequisites

- [Foundry](https://book.getfoundry.sh/getting-started/installation) (`cast` command)
- [op-workbench](https://github.com/ethereum-optimism/op-workbench) for RPC URL lookups

## Installation

```

# Run Claude Code
claude

# Add the marketplace
/plugin marketplace add /path/to/op-claude-plugins

# Install the plugin
/plugin install op-skills@op-claude-plugins

# Verify installation
/plugin list
```

Restart Claude Code after installation. Test by asking: "Check the OP Stack skill setup".

## Configuration

Some skills require configuration, such as paths to local repositories. Claude will prompt you for this information when needed, but you can also set env vars:

- **Repository paths**: Skills that query RPC URLs need paths to `op-workbench` and `k8s` repositories
  - Claude will ask for these paths when you first use related skills
  - You can also set environment variables: `$OP_WORKBENCH_PATH` and `$K8S_REPO_PATH`
  
- **Tool requirements**: Most skills use the `cast` command from Foundry
  - If not installed, Claude will provide installation instructions
  - Run the `check-op-stack-skill-setup` skill to verify your environment

## Available Skills

See the [skills](./tree/main/op-skills/skills) directory for a list of the available skills.
