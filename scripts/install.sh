#!/bin/bash
set -e
INSTALL_DIR="${1:-/Users/MCP-servers/MCP-realtime-tech-docs}"
REPO_URL="https://github.com/Ruben-Alvarez-Dev/MCP-realtime-tech-docs"

echo "🎤 MCP Realtime Tech Docs Installer"
echo "   Installing to: $INSTALL_DIR"
echo ""

if [ -d "$INSTALL_DIR" ]; then
    echo "📦 Updating existing installation..."
    cd "$INSTALL_DIR" && git pull 2>/dev/null || true
else
    echo "📦 Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo "🐍 Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -e . --quiet

echo "📚 Building documentation index..."
python3 -c "
from src.indexer import DocIndex
idx = DocIndex('docs')
entries = idx.build()
idx.save('index/docs-index.json')
print(f'   Indexed {len(entries)} files')
"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Add to Goose config.yaml:"
echo ""
echo "  realtime-tech-docs:"
echo "    enabled: true"
echo "    type: stdio"
echo "    name: realtime-tech-docs"
echo "    command: ${INSTALL_DIR}/.venv/bin/python"
echo "    args:"
echo "      - -m"
echo "      - src.server"
echo "    env:"
echo "      PYTHONPATH: ${INSTALL_DIR}"
echo "    timeout: 30"
echo ""
echo "🎤 6 tools: search_docs, get_doc, get_quickstart, compare_products, get_examples, list_catalog"
