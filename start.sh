#!/bin/bash

set -Eeuo pipefail

cd "$(dirname "$0")"

uv run src/op_mcp_server.py "$@"
