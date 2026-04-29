"""Indexer: scans docs/ and builds a searchable index."""

import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class DocEntry:
    path: str
    size: int
    preview: str
    product: str
    category: str


class DocIndex:
    """Builds and queries an index of all documentation files."""

    def __init__(self, docs_dir):
        self.docs_dir = Path(docs_dir)
        self.entries = []
        self._built = False

    def build(self):
        self.entries = []
        for root, _dirs, files in os.walk(self.docs_dir):
            for fname in files:
                if not fname.endswith((".md", ".txt")):
                    continue
                fpath = Path(root) / fname
                rel = fpath.relative_to(self.docs_dir)
                parts = rel.parts
                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")
                    size = len(content.encode("utf-8"))
                    preview = content[:200].replace("\n", " ").strip()
                    product = parts[0] if len(parts) > 1 else "root"
                    category = "/".join(parts[1:-1]) if len(parts) > 2 else "root"
                    self.entries.append(DocEntry(
                        path=str(rel), size=size, preview=preview,
                        product=product, category=category,
                    ))
                except Exception:
                    pass
        self._built = True
        return self.entries

    def save(self, index_path):
        index_path = Path(index_path)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(
            [asdict(e) for e in self.entries], indent=2, ensure_ascii=False
        ))

    def load(self, index_path):
        data = json.loads(Path(index_path).read_text())
        self.entries = [DocEntry(**d) for d in data]
        self._built = True

    def search(self, query, product=None, max_results=10):
        if not self._built:
            raise RuntimeError("Index not built")
        words = query.lower().split()
        scored = []
        for entry in self.entries:
            if product and product != "all" and entry.product != product:
                continue
            path_lower = entry.path.lower()
            preview_lower = entry.preview.lower()
            score = 0
            for word in words:
                if word in path_lower:
                    score += 3
                if word in preview_lower:
                    score += 1
            if score > 0:
                scored.append((score, entry))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:max_results]]

    def catalog(self, product=None):
        result = {}
        for entry in self.entries:
            if product and product != "all" and entry.product != product:
                continue
            key = f"{entry.product}/{entry.category}"
            result.setdefault(key, []).append(entry)
        return result
