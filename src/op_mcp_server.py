#!/usr/bin/env python3

import argparse
import asyncio
import subprocess
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import httpx
import toml
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server


class OpMcpServer:
    """MCP Server for interacting with, or getting information about, OP Stack blockchains."""
    
    def __init__(self, k8s_repo_path: Optional[str] = None, op_workbench_repo_path: Optional[str] = None, cast_command: Optional[str] = None):
        self.server = Server("op-mcp-server")
        self.k8s_repo_path = k8s_repo_path
        self.op_workbench_repo_path = op_workbench_repo_path
        self.cast_command = cast_command or "cast"
        self.setup_handlers()
    
    def _discover_recipes(self) -> Dict[str, str]:
        """Discover all recipes and return a dict mapping recipe name to description."""
        recipes_dir = Path("recipes")
        recipes = {}
        
        if not recipes_dir.exists() or not recipes_dir.is_dir():
            return recipes
        
        try:
            for md_file in recipes_dir.glob("*.md"):
                recipe_name = md_file.stem  # filename without .md extension
                
                # Read first line for description
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        # Strip the "# " prefix if present
                        description = first_line.lstrip("# ").strip() if first_line.startswith("#") else first_line
                        recipes[recipe_name] = description
                except Exception:
                    # If we can't read the description, use a default
                    recipes[recipe_name] = f"Recipe: {recipe_name}"
        except Exception:
            # If there's any error discovering recipes, return empty dict
            pass
        
        return recipes

    def setup_handlers(self):
        """Setup MCP handlers for commands."""
        
        @self.server.list_tools()
        async def list_tools() -> List[types.Tool]:
            """List available tools."""
            tools = [

                types.Tool(
                    name="check_setup",
                    description="Check that this MCP server is set up correctly. Only run this tool if there's a reason to believe the server is not set up correctly.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_chain_config_from_superchain_registry",
                    description="Get information about OP Stack chains from Optimism Superchain Registry. E.g. chain id, explorer url, contract addresses, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "l1_chain": {
                                "type": "string",
                                "description": "L1 chain (e.g. mainnet, sepolia)"
                            },
                            "l2_chain": {
                                "type": "string",
                                "description": "L2 chain identifier (e.g. op, base, ink)"
                            }
                        },
                        "required": ["l1_chain", "l2_chain"]
                    }
                ),
                types.Tool(
                    name="list_k8s_network_labels",
                    description="List the possible values for k8s network (e.g. mainnet-prod, mainnet-dev, sepolia-prod, sepolia-dev, base-mainnet-prod, base-mainnet-dev, base-sepolia-prod, base-sepolia-dev, ink-sepolia-prod, ink-sepolia-dev, etc.)",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="list_l1_rpc_urls",
                    description="Use op-workbench to list RPC URLs for a specific Ethereum L1 network.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "network": {
                                "type": "string",
                                "description": "Network (e.g. mainnet, sepolia)"
                            },
                            "node_type": {
                                "type": "string", 
                                "description": "Node type (geth or lighthouse)",
                                "enum": ["geth", "lighthouse"]
                            }
                        },
                        "required": ["network", "node_type"]
                    }
                ),
                types.Tool(
                    name="list_l2_rpc_urls",
                    description="Use op-workbench to list RPC URLs for a specific OP Stack L2 network, k8s network label and node type. E.g. list_l2_rpc_urls(k8s_network_label='mainnet-prod', node_type='op-node') or list_l2_rpc_urls(k8s_network_label='base-sepolia-dev', node_type='op-geth')",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "k8s_network_label": {
                                "type": "string",
                                "description": "Kubernetes network label (which we get from the list_k8s_network_labels tool)"
                            },
                            "node_type": {
                                "type": "string", 
                                "description": "Node type (op-node or op-geth)",
                                "enum": ["op-node", "op-geth", "op-supervisor"]
                            }
                        },
                        "required": ["k8s_network_label", "node_type"]
                    }
                ),
                types.Tool(
                    name="cast",
                    description="Generic cast command - run cast with custom arguments. For the value of --rpc-url, use the list_l1_rpc_urls or list_l2_rpc_urls tool.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "args": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "Array of arguments to pass to cast command (e.g. ['--help'], ['balance', '0x123...', '--rpc-url', 'https://...'])"
                            }
                        },
                        "required": ["args"]
                    }
                ),
                types.Tool(
                    name="get_abi",
                    description="Get the ABI for a contract from Optimism's contracts-bedrock snapshots",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "contract_name": {
                                "type": "string",
                                "description": "Name of the contract (e.g. L1StandardBridge, OptimismPortal)"
                            },
                            "tag": {
                                "type": "string",
                                "description": "Optional git tag to fetch from (e.g. 'op-contracts/v4.0.0-rc.8'). If not provided, uses develop branch."
                            }
                        },
                        "required": ["contract_name"]
                    }
                ),
                types.Tool(
                    name="dispute_game_constants",
                    description="Fetch Optimism's Types.sol file, which defines the dispute game constants.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tag": {
                                "type": "string",
                                "description": "Optional git tag to fetch from (e.g. 'op-contracts/v4.0.0-rc.8'). If not provided, uses develop branch."
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="standard_prestates",
                    description="Fetch standard prestates configuration from the Optimism Superchain Registry.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="specs",
                    description="Fetch documentation pages from the Optimism specs repository. Specify a page or omit the page argument to get the table of contents.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "string",
                                "description": "Page to fetch (e.g. 'SUMMARY.md', 'protocol/deposits.md'). Defaults to 'SUMMARY.md' if not provided."
                            }
                        },
                        "required": []
                    }
                ),
            ]
            
            # Dynamically add recipe tools
            recipes = self._discover_recipes()
            for recipe_name, description in recipes.items():
                tools.append(
                    types.Tool(
                        name=recipe_name,
                        description=description,
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    )
                )
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[types.TextContent]:
            """Handle tool calls."""
            try:
                if name == "check_setup":
                    return await self.check_setup(arguments)
                elif name == "get_chain_config_from_superchain_registry":
                    return await self.get_chain_config_from_superchain_registry(arguments)
                elif name == "list_k8s_network_labels":
                    return await self.list_k8s_network_labels(arguments)
                elif name == "list_l1_rpc_urls":
                    return await self.list_l1_rpc_urls(arguments)
                elif name == "list_l2_rpc_urls":
                    return await self.list_l2_rpc_urls(arguments)
                elif name == "cast":
                    return await self.cast(arguments)
                elif name == "get_abi":
                    return await self.get_abi(arguments)
                elif name == "dispute_game_constants":
                    return await self.dispute_game_constants(arguments)
                elif name == "standard_prestates":
                    return await self.standard_prestates(arguments)
                elif name == "specs":
                    return await self.specs(arguments)
                else:
                    # Check if this is a recipe tool
                    recipes = self._discover_recipes()
                    if name in recipes:
                        return await self.get_recipe_content(name)
                    else:
                        raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def run_command(self, cmd: List[str], cwd: Optional[str] = None) -> str:
        """Run a command and return its output."""
        clean_env = os.environ.copy()
        removed_vars = []
        
        venv_vars_to_remove = ['VIRTUAL_ENV', 'PYTHONPATH']
        for var in venv_vars_to_remove:
            if var in clean_env:
                removed_vars.append(f"{var}={clean_env[var]}")
                clean_env.pop(var)
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=cwd,
                env=clean_env,
                timeout=60
            )
            
            if result.returncode != 0:
                return f"Command failed with code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
            
            return result.stdout
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error running command: {str(e)}"
    

    async def check_setup(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Check that repository paths are configured and working correctly."""
        results = []
        
        # Check if paths are configured
        if not self.k8s_repo_path:
            results.append("❌ k8s_repo_path not configured. Please set k8s-repo-path in arguments.")
        if not self.op_workbench_repo_path:
            results.append("❌ op_workbench_repo_path not configured. Please set op-workbench-repo-path in arguments.")
        
        if not self.k8s_repo_path or not self.op_workbench_repo_path:
            return [types.TextContent(type="text", text="\n".join(results))]
        
        # Check if k8s repo path exists
        if os.path.exists(self.k8s_repo_path) and os.path.isdir(self.k8s_repo_path):
            results.append(f"✅ k8s repo path exists: {self.k8s_repo_path}")
        else:
            results.append(f"❌ k8s repo path does not exist or is not a directory: {self.k8s_repo_path}")
        
        # Check if op-workbench repo path exists
        if os.path.exists(self.op_workbench_repo_path) and os.path.isdir(self.op_workbench_repo_path):
            results.append(f"✅ op-workbench repo path exists: {self.op_workbench_repo_path}")
        else:
            results.append(f"❌ op-workbench repo path does not exist or is not a directory: {self.op_workbench_repo_path}")
            return [types.TextContent(type="text", text="\n".join(results))]
        
        # Check if poetry is installed and available, it's needed by op-workbench
        try:
            cmd = ["poetry", "--version"]
            output = await self.run_command(cmd)
            
            if "Command failed" in output or "Error running command" in output:
                results.append(f"❌ Poetry is not installed or not available in PATH:\n{output}; PATH: {os.environ.get('PATH')}")
            else:
                results.append(f"✅ Poetry is available: {output.strip()}")
        except Exception as e:
            results.append(f"❌ Error checking poetry availability: {str(e)}")
        
        # Try to run ./op --help in the op-workbench directory
        try:
            cmd = ["./op", "--help"]
            output = await self.run_command(cmd, cwd=self.op_workbench_repo_path)
            
            if "Command failed" in output or "Error running command" in output:
                results.append(f"❌ Failed to run ./op --help in op-workbench directory:\n{output}")
            else:
                results.append(f"✅ Successfully ran ./op --help in op-workbench directory")
                results.append(f"\nOutput:\n{output}")
        except Exception as e:
            results.append(f"❌ Error running ./op --help: {str(e)}")

        # Check if cast is installed and available
        try:
            cmd = [self.cast_command, "--version"]
            output = await self.run_command(cmd)
            
            if "Command failed" in output or "Error running command" in output:
                results.append(f"❌ Cast is not installed or not available (using '{self.cast_command}'):\n{output}")
            else:
                results.append(f"✅ Cast is available (using '{self.cast_command}'): {output.strip()}")
        except Exception as e:
            results.append(f"❌ Error checking cast availability: {str(e)}")

        return [types.TextContent(type="text", text="\n".join(results))]

    async def get_chain_config_from_superchain_registry(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Get chain configuration from Optimism superchain registry."""
        l1_chain = args["l1_chain"]
        l2_chain = args["l2_chain"]
        
        url = f"https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/main/superchain/configs/{l1_chain}/{l2_chain}.toml"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse the TOML content
                chain_config = toml.loads(response.text)
                
                # Format as JSON for better readability
                formatted_config = json.dumps(chain_config, indent=2)
                
                return [types.TextContent(type="text", text=formatted_config)]
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return [types.TextContent(type="text", text=f"Chain configuration not found for {l1_chain}/{l2_chain}")]
            else:
                return [types.TextContent(type="text", text=f"HTTP error {e.response.status_code}: {e.response.text}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error fetching chain info: {str(e)}")]

    async def list_k8s_network_labels(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """List network values using the list_network_values.sh script."""
        if not self.k8s_repo_path:
            return [types.TextContent(type="text", text="Error: k8s_repo_path not configured. Please set k8s-repo-path in server arguments.")]
        
        if not os.path.exists(self.k8s_repo_path) or not os.path.isdir(self.k8s_repo_path):
            return [types.TextContent(type="text", text=f"Error: k8s_repo_path does not exist or is not a directory: {self.k8s_repo_path}")]
        
        try:
            cmd = ["./scripts/list_network_values.sh", self.k8s_repo_path]
            output = await self.run_command(cmd)
            
            if "Command failed" in output or "Error running command" in output:
                return [types.TextContent(type="text", text=f"Error running list_network_values.sh:\n{output}")]
            else:
                return [types.TextContent(type="text", text=output)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error running list_network_values.sh: {str(e)}")]

    async def list_l1_rpc_urls(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Use op-workbench to list RPC URLs for a specific Ethereum L1 network."""
        network = args["network"]
        node_type = args["node_type"]
        if not self.op_workbench_repo_path:
            return [types.TextContent(type="text", text="Error: op_workbench_repo_path not configured. Please set op-workbench-repo-path in server arguments.")]
        
        if not os.path.exists(self.op_workbench_repo_path) or not os.path.isdir(self.op_workbench_repo_path):
            return [types.TextContent(type="text", text=f"Error: op_workbench_repo_path does not exist or is not a directory: {self.op_workbench_repo_path}")]
    
        
        try:
            cmd = ["bash", "-c", f"./op urls all | grep {network}-l1 | grep {node_type}"]
            output = await self.run_command(cmd, cwd=self.op_workbench_repo_path)
            
            if "Command failed" in output or "Error running command" in output:
                return [types.TextContent(type="text", text=f"Error running op urls command:\n{output}")]
            else:
                return [types.TextContent(type="text", text=output)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error running op urls command: {str(e)}")]


    async def list_l2_rpc_urls(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Use op-workbench to list RPC URLs for a specific OP Stack L2 network and node type."""
        if not self.op_workbench_repo_path:
            return [types.TextContent(type="text", text="Error: op_workbench_repo_path not configured. Please set op-workbench-repo-path in server arguments.")]
        
        if not os.path.exists(self.op_workbench_repo_path) or not os.path.isdir(self.op_workbench_repo_path):
            return [types.TextContent(type="text", text=f"Error: op_workbench_repo_path does not exist or is not a directory: {self.op_workbench_repo_path}")]
        
        k8s_network_label = args["k8s_network_label"]
        node_type = args["node_type"]
        
        try:
            cmd = ["./op", "urls", "all", f"--network={k8s_network_label}", node_type]
            output = await self.run_command(cmd, cwd=self.op_workbench_repo_path)
            
            if "Command failed" in output or "Error running command" in output:
                return [types.TextContent(type="text", text=f"Error running op urls command:\n{output}")]
            else:
                return [types.TextContent(type="text", text=output)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error running op urls command: {str(e)}")]

    async def cast(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Generic cast command - run cast with custom arguments."""
        cast_args = args["args"]
        
        cmd = [self.cast_command] + cast_args
        
        output = await self.run_command(cmd)
        return [types.TextContent(type="text", text=output)]

    async def get_abi(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Get the ABI for a contract from Optimism's contracts-bedrock snapshots."""
        contract_name = args["contract_name"]
        tag = args.get("tag")
        
        if tag:
            url = f"https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/tags/{tag}/packages/contracts-bedrock/snapshots/abi/{contract_name}.json"
        else:
            url = f"https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/snapshots/abi/{contract_name}.json"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse the JSON content to validate it
                abi_json = response.json()
                
                # Format as JSON for better readability
                formatted_abi = json.dumps(abi_json, indent=2)
                
                return [types.TextContent(type="text", text=formatted_abi)]
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return [types.TextContent(type="text", text=f"ABI not found for contract '{contract_name}'")]
            else:
                return [types.TextContent(type="text", text=f"HTTP error {e.response.status_code}: {e.response.text}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error fetching ABI for '{contract_name}': {str(e)}")]

    async def dispute_game_constants(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Fetch the dispute game constants from Optimism's Types.sol file."""
        tag = args.get("tag")
        
        if tag:
            url = f"https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/tags/{tag}/packages/contracts-bedrock/src/dispute/lib/Types.sol"
        else:
            url = f"https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/src/dispute/lib/Types.sol"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                return [types.TextContent(type="text", text=response.text)]
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return [types.TextContent(type="text", text=f"Types.sol file not found (tag: {tag if tag else 'develop'})")]
            else:
                return [types.TextContent(type="text", text=f"HTTP error {e.response.status_code}: {e.response.text}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error fetching Types.sol file: {str(e)}")]

    async def standard_prestates(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Fetch standard prestates configuration from the Optimism Superchain Registry."""
        url = "https://raw.githubusercontent.com/ethereum-optimism/superchain-registry/refs/heads/main/validation/standard/standard-prestates.toml"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse the TOML content
                prestates_config = toml.loads(response.text)
                
                # Format as JSON for better readability
                formatted_config = json.dumps(prestates_config, indent=2)
                
                return [types.TextContent(type="text", text=formatted_config)]
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return [types.TextContent(type="text", text="Standard prestates configuration not found.")]
            else:
                return [types.TextContent(type="text", text=f"HTTP error {e.response.status_code}: {e.response.text}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error fetching standard prestates: {str(e)}")]

    async def specs(self, args: Dict[str, Any]) -> Sequence[types.TextContent]:
        """Fetch documentation pages from the Optimism specs repository."""
        page = args.get("page", "SUMMARY.md")
        url = f"https://raw.githubusercontent.com/ethereum-optimism/specs/refs/heads/main/specs/{page}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                return [types.TextContent(type="text", text=response.text)]
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return [types.TextContent(type="text", text=f"Documentation page '{page}' not found.")]
            else:
                return [types.TextContent(type="text", text=f"HTTP error {e.response.status_code}: {e.response.text}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error fetching documentation page '{page}': {str(e)}")]

    async def get_recipe_content(self, recipe_name: str) -> Sequence[types.TextContent]:
        """Get the contents of a specific recipe from the recipes directory."""
        recipes_dir = Path("recipes")
        
        if not recipes_dir.exists() or not recipes_dir.is_dir():
            return [types.TextContent(type="text", text=f"Error: recipes directory does not exist: {recipes_dir.absolute()}")]
        
        recipe_file = recipes_dir / f"{recipe_name}.md"
        
        if not recipe_file.exists():
            return [types.TextContent(type="text", text=f"Error: recipe '{recipe_name}' not found. File does not exist: {recipe_file}")]
        
        try:
            with open(recipe_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return [types.TextContent(type="text", text=content)]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error reading recipe '{recipe_name}': {str(e)}")]


async def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MCP Server for interacting with OP Stack blockchains",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "args",
        nargs="*",
        help="Arguments in key=value format (e.g., k8s-repo-path=/path/to/repo, cast-command=/usr/local/bin/cast)"
    )
    
    args = parser.parse_args()
    
    # Parse key=value arguments
    parsed_args = argparse.Namespace()
    parsed_args.k8s_repo_path = None
    parsed_args.op_workbench_repo_path = None
    parsed_args.cast_command = None
    
    for arg in args.args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            if key == "k8s-repo-path":
                parsed_args.k8s_repo_path = value
            elif key == "op-workbench-repo-path":
                parsed_args.op_workbench_repo_path = value
            elif key == "cast-command":
                parsed_args.cast_command = value
            else:
                # Ignore unknown arguments for forward compatibility
                pass
        else:
            # Ignore non-key=value arguments
            pass
    
    return parsed_args


async def main():
    """Main entry point for the MCP server."""
    args = await parse_arguments()
    
    op_mcp_server = OpMcpServer(
        k8s_repo_path=args.k8s_repo_path,
        op_workbench_repo_path=args.op_workbench_repo_path,
        cast_command=args.cast_command
    )
    
    async with stdio_server() as (read_stream, write_stream):
        await op_mcp_server.server.run(
            read_stream, 
            write_stream,
            op_mcp_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())