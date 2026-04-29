#!/bin/bash
# MCP Realtime Tech Docs - Installer
# Usage: curl -sSL https://raw.githubusercontent.com/Ruben-Alvarez-Dev/MCP-realtime-tech-docs/main/scripts/install.sh | bash

set -e

INSTALL_DIR="${MCP_INSTALL_DIR:-/Users/$(whoami)/MCP-servers/MCP-realtime-tech-docs}"
REPO_URL="https://github.com/Ruben-Alvarez-Dev/MCP-realtime-tech-docs"

echo "Installing MCP Realtime Tech Docs..."
echo "Target: $INSTALL_DIR"

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
  echo "Updating existing installation..."
  cd "$INSTALL_DIR"
  git pull
else
  echo "Cloning repository..."
  git clone "$REPO_URL" "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

# Create venv and install
echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -e . 2>&1 | tail -3

# Build index
echo "Building documentation index..."
PYTHONPATH=. python3 -c "
from src.indexer import DocIndex
idx = DocIndex('docs')
entries = idx.build()
idx.save('index/docs-index.json')
print(f'Indexed {len(entries)} files')
"

echo ""
echo "Installation complete!"
echo ""
echo "Add to your Goose config.yaml:"
echo ""
echo "  mcp-realtime-tech-docs:"
echo "    enabled: true"
echo "    type: stdio"
echo "    name: mcp-realtime-tech-docs"
echo "    description: \"Live docs for realtime voice & video (Qwen, Xiaomi MiMo, LiveKit)\""
echo "    display_name: \"Voice & Video Docs MCP\""
echo "    command: $INSTALL_DIR/.venv/bin/python3"
echo "    args:"
echo "      - -m"
echo "      - src.server"
echo "    timeout: 30"
echo "    bundled: false"
echo "    available_tools: []"
echo ""
echo "Then restart Goose."
