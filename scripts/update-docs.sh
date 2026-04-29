#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="${SCRIPT_DIR}/../docs"
JART_OS="/Users/ruben/Code/Jart-OS"

echo "📚 Updating realtime voice/video documentation..."
if [ -d "${JART_OS}/qwen-realtime" ]; then
    echo "  → Copying Qwen docs from Jart-OS..."
    cp -r "${JART_OS}/qwen-realtime/"* "${DOCS_DIR}/qwen/" 2>/dev/null || true
fi
if [ -d "${JART_OS}/xiaomi-realtime" ]; then
    echo "  → Copying Xiaomi docs from Jart-OS..."
    cp -r "${JART_OS}/xiaomi-realtime/"* "${DOCS_DIR}/xiaomi-mimo/" 2>/dev/null || true
fi
echo "  → Rebuilding index..."
cd "${SCRIPT_DIR}/.."
python3 -c "
from src.indexer import DocIndex
idx = DocIndex('docs')
entries = idx.build()
idx.save('index/docs-index.json')
print(f'   Indexed {len(entries)} files')
"
echo "✅ Documentation updated!"
