#!/bin/bash
# Update documentation from Jart-OS sources
set -e

BASE="$(cd "$(dirname "$0")/.." && pwd)"
JART="/Users/$(whoami)/Code/Jart-OS"

echo "Updating docs from Jart-OS..."

if [ -d "$JART/qwen-realtime" ]; then
  cp $JART/qwen-realtime/*.md $BASE/docs/qwen-realtime-official/ 2>/dev/null || true
  echo "  Updated qwen-realtime-official"
fi

if [ -d "$JART/xiaomi-realtime" ]; then
  cp $JART/xiaomi-realtime/*.md $BASE/docs/xiaomi-realtime-official/ 2>/dev/null || true
  echo "  Updated xiaomi-realtime-official"
fi

# Re-index
echo "Re-indexing..."
PYTHONPATH=. python3 -c "
from src.indexer import DocIndex
idx = DocIndex('docs')
entries = idx.build()
idx.save('index/docs-index.json')
print(f'Indexed {len(entries)} files, {sum(e.size for e in entries)} bytes')
"

echo "Done!"
