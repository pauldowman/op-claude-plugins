# Cast MCP Server

An MCP (Model Context Protocol) server that provides tools for interacting with the Ethereum blockchain using Cast commands.

## Features

- **cast_call**: Call contract functions (read-only)
- **cast_send**: Send transactions to contracts

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Foundry installed (`curl -L https://foundry.paradigm.xyz | bash`)

## Installation

This project uses uv for fast, modern Python dependency management. Dependencies are automatically managed - no manual virtual environment setup required.

To install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Dependencies will be automatically installed when you run the server.

## Usage

This server is designed to be used with MCP-compatible clients. To use with the Claude app, add the following config to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "op-mcp-server": {
      "command": "<PATH TO THIS REPO>/start.sh",
      "args": ["k8s-repo-path=<PATH TO k8s REPO>", "op-workbench-repo-path=<PATH TO op-workbench REPO>"]
    }
  }
}

Use `logs.sh` to debug.

## Development

### Adding Dependencies
```bash
uv add package_name
```

### Running the Server
```bash
./start.sh
```


## Tools Reference

### cast_call
Make read-only calls to contract functions.

### cast_send
Send transactions to contract functions with ETH value support.