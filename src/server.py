"""MCP Realtime Tech Docs Server - FastMCP 3.0

Live documentation for realtime voice & video technologies:
- Qwen (Alibaba Cloud): Omni Realtime, CosyVoice TTS, ASR, Models
- Xiaomi MiMo: Omni, TTS, Models, Token Plan API
- LiveKit: Agents, STT, LLM, TTS, Plugins, OpenAI Realtime
"""

from pathlib import Path
from fastmcp import FastMCP
from .indexer import DocIndex

DOCS_DIR = Path(__file__).parent.parent / "docs"
INDEX_PATH = Path(__file__).parent.parent / "index" / "docs-index.json"

index = DocIndex(DOCS_DIR)
if INDEX_PATH.exists():
    index.load(INDEX_PATH)
else:
    index.build()
    index.save(INDEX_PATH)

mcp = FastMCP(
    name="realtime-voice-video-docs",
    version="1.0.0",
    instructions="Live documentation for realtime voice & video technologies: Qwen (Alibaba Cloud), Xiaomi MiMo, and LiveKit. 102 files covering TTS, STT, Realtime APIs, voice cloning, WebRTC, and agents.",
)


@mcp.tool()
def search_docs(query: str, product: str = "all", max_results: int = 10) -> str:
    """Search all realtime voice/video documentation by keywords.
    Args:
        query: Search keywords (e.g. 'realtime API websocket', 'TTS voice cloning')
        product: Filter: 'qwen', 'xiaomi-mimo', 'livekit', or 'all'
        max_results: Maximum results (default 10)
    """
    results = index.search(query, product=product, max_results=max_results)
    if not results:
        return f'No results for "{query}". Try: realtime, TTS, STT, omni, voice, websocket, cosyvoice'
    lines = [f"Found {len(results)} docs for '{query}':"]
    for r in results:
        lines.append(f"- {r.path} ({r.size}B): {r.preview[:100]}")
    return "\n".join(lines)


@mcp.tool()
def get_doc(path: str, max_bytes: int = 50000) -> str:
    """Read full content of a specific document.
    Args:
        path: Document path (from search_docs)
        max_bytes: Max bytes to return (default 50000)
    """
    fpath = DOCS_DIR / path
    if not fpath.exists():
        return f"File not found: {path}"
    content = fpath.read_text(encoding="utf-8", errors="replace")
    if len(content) <= max_bytes:
        return content
    return content[:max_bytes] + f"\n[...truncated, {len(content)} bytes total]"


@mcp.tool()
def get_quickstart(product: str, use_case: str = "") -> str:
    """Get a quickstart guide for a product.
    Args:
        product: qwen-realtime, qwen-tts, qwen-asr, qwen-omni, xiaomi-omni, xiaomi-tts, xiaomi-realtime, livekit-agents, livekit-stt, livekit-realtime
        use_case: Optional use case description
    """
    prefix_map = {
        "qwen-realtime": ["qwen-realtime-official/", "qwen/realtime/"],
        "qwen-tts": ["qwen-realtime-official/04", "qwen/tts-cosyvoice/"],
        "qwen-asr": ["qwen/speech-recognition/"],
        "qwen-omni": ["qwen-realtime-official/00", "qwen-realtime-official/03", "qwen/omni/"],
        "xiaomi-omni": ["xiaomi-realtime-official/00", "xiaomi-realtime-official/02", "xiaomi-mimo/omni/"],
        "xiaomi-tts": ["xiaomi-realtime-official/06", "xiaomi-mimo/tts/"],
        "xiaomi-realtime": ["xiaomi-realtime-official/"],
        "livekit-agents": ["livekit/agents/"],
        "livekit-stt": ["livekit/stt/"],
        "livekit-realtime": ["livekit/realtime/"],
    }
    prefixes = prefix_map.get(product, [])
    if not prefixes:
        return f"No quickstart for {product}. Available: {', '.join(prefix_map.keys())}"
    matching = [e for e in index.entries if any(p in e.path for p in prefixes)]
    if not matching:
        return f"No docs found for {product}"
    matching.sort(key=lambda e: e.size, reverse=True)
    parts = []
    for entry in matching[:3]:
        content = (DOCS_DIR / entry.path).read_text(encoding="utf-8", errors="replace")[:30000]
        parts.append(f"## {entry.path}\n{content}")
    return f"# Quickstart: {product}\n\n" + "\n---\n".join(parts)


@mcp.tool()
def compare_products(products: list[str]) -> str:
    """Compare realtime voice/video products side-by-side.
    Args:
        products: List of products to compare
    """
    sections = []
    for product in products:
        files = index.search(product, max_results=5)
        pricing = [e for e in files if any(k in e.path.lower() for k in ("pricing", "token", "plan"))]
        models = [e for e in files if any(k in e.path.lower() for k in ("model", "arch"))]
        price_info = (DOCS_DIR / pricing[0].path).read_text(encoding="utf-8", errors="replace")[:500] if pricing else "N/A"
        model_info = (DOCS_DIR / models[0].path).read_text(encoding="utf-8", errors="replace")[:500] if models else "N/A"
        sections.append(f"### {product}\nDocs: {len(files)}\nPricing: {price_info[:300]}\nModels: {model_info[:300]}")
    return f"# {' vs '.join(products)}\n\n" + "\n---\n".join(sections)


@mcp.tool()
def get_examples(product: str, feature: str = "") -> str:
    """Get code examples for a product and feature.
    Args:
        product: qwen, xiaomi-mimo, livekit
        feature: TTS, STT, realtime, omni, voice cloning, websocket, agents
    """
    query = f"{product} {feature}".strip()
    results = index.search(query, product=product, max_results=5)
    if not results:
        results = index.search(query, max_results=5)
    if not results:
        return f"No examples for {product}/{feature}"
    example_files = [e for e in results if "example" in e.path.lower() or "code" in e.path.lower()]
    if example_files:
        results = example_files + [e for e in results if e not in example_files]
    parts = []
    for entry in results[:3]:
        content = (DOCS_DIR / entry.path).read_text(encoding="utf-8", errors="replace")[:15000]
        parts.append(f"## {entry.path}\n{content}")
    return f"# Examples: {product}/{feature}\n\n" + "\n---\n".join(parts)


@mcp.tool()
def list_catalog(product: str = "all") -> str:
    """List all available documentation by product and category.
    Args:
        product: Filter: 'qwen', 'xiaomi-mimo', 'livekit', or 'all'
    """
    grouped = index.catalog(product=product)
    lines = []
    total_files = 0
    total_bytes = 0
    for group, entries in sorted(grouped.items()):
        group_size = sum(e.size for e in entries)
        total_files += len(entries)
        total_bytes += group_size
        lines.append(f"## {group} ({group_size // 1024}KB)")
        for e in entries:
            lines.append(f"  - {e.path} ({e.size // 1024}KB)")
    return f"# Catalog ({total_files} files, {total_bytes // 1024 // 1024}MB)\n\n" + "\n".join(lines)


def main():
    mcp.run()


if __name__ == "__main__":
    main()