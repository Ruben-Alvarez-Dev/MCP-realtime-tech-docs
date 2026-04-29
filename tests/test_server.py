"""Tests for MCP Realtime Tech Docs server."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.indexer import DocIndex

def test_index_build():
    docs_dir = Path(__file__).parent.parent / "docs"
    if not docs_dir.exists() or not any(docs_dir.iterdir()):
        print("⚠ No docs/ files, skipping")
        return
    idx = DocIndex(docs_dir)
    entries = idx.build()
    assert len(entries) > 0
    print(f"✓ Index built: {len(entries)} entries")

def test_search():
    docs_dir = Path(__file__).parent.parent / "docs"
    if not docs_dir.exists() or not any(docs_dir.iterdir()):
        print("⚠ No docs/ files, skipping")
        return
    idx = DocIndex(docs_dir)
    idx.build()
    results = idx.search("realtime TTS voice")
    assert len(results) > 0
    print(f"✓ Search: {len(results)} results for 'realtime TTS voice'")

def test_catalog():
    docs_dir = Path(__file__).parent.parent / "docs"
    if not docs_dir.exists() or not any(docs_dir.iterdir()):
        print("⚠ No docs/ files, skipping")
        return
    idx = DocIndex(docs_dir)
    idx.build()
    catalog = idx.catalog()
    assert len(catalog) > 0
    print(f"✓ Catalog: {len(catalog)} groups")

if __name__ == "__main__":
    test_index_build()
    test_search()
    test_catalog()
    print("\nAll tests passed ✓")
