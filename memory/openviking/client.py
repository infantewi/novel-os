# -*- coding: utf-8 -*-
"""OpenViking In-Process / Remote Client Wrapper."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import OpenVikingConfig
from .uri_mapper import VikingURIMapper


class OpenVikingClient:
    """Provides high-performance hierarchical storage and indexing for OpenViking."""

    def __init__(self, config: Optional[OpenVikingConfig] = None, storage_root: Optional[Path] = None):
        self.config = config or OpenVikingConfig()
        default_root = Path(__file__).resolve().parents[2]
        self.storage_root = storage_root or (default_root / self.config.local_storage_dir)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_root / "viking_index.json"
        self._memory_store: Dict[str, Dict[str, Any]] = self._load_index()

    def _load_index(self) -> Dict[str, Dict[str, Any]]:
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_index(self) -> None:
        temp_f = self.index_file.with_suffix(".tmp")
        with open(temp_f, "w", encoding="utf-8") as f:
            json.dump(self._memory_store, f, ensure_ascii=False, indent=2)
        temp_f.replace(self.index_file)

    def write_node(self, uri: str, l0_abstract: str, l1_overview: Dict[str, Any], l2_details: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> bool:
        node = {
            "uri": uri,
            "l0_abstract": l0_abstract,
            "l1_overview": l1_overview,
            "l2_details": l2_details,
            "metadata": metadata or {},
        }
        self._memory_store[uri] = node
        self._save_index()
        return True

    def get_node(self, uri: str) -> Optional[Dict[str, Any]]:
        return self._memory_store.get(uri)

    def find(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        q_tokens = [w.strip() for w in query.lower().split() if w.strip()]
        for uri, node in self._memory_store.items():
            abstract = node.get("l0_abstract", "").lower()
            if any(t in abstract or t in uri.lower() for t in q_tokens):
                results.append({"uri": uri, "score": 1.0, "l0_abstract": node.get("l0_abstract")})
            if len(results) >= limit:
                break
        return results

    def search(self, query: str, mode: str = "standard", limit: int = 10) -> Dict[str, Any]:
        matched_nodes = []
        q_tokens = [w.strip() for w in query.lower().split() if w.strip()]

        for uri, node in self._memory_store.items():
            abstract = node.get("l0_abstract", "")
            overview_str = json.dumps(node.get("l1_overview", {}), ensure_ascii=False)
            details_str = json.dumps(node.get("l2_details", {}), ensure_ascii=False)

            score = 0.0
            for t in q_tokens:
                if t in abstract.lower():
                    score += 0.6
                if t in overview_str.lower():
                    score += 0.3
                if t in details_str.lower():
                    score += 0.1

            if score > 0:
                matched_nodes.append({
                    "uri": uri,
                    "score": round(score, 3),
                    "l0_abstract": abstract,
                    "l1_overview": node.get("l1_overview"),
                    "l2_details": node.get("l2_details") if mode == "context" else {}
                })

        matched_nodes.sort(key=lambda x: x["score"], reverse=True)
        top_matches = matched_nodes[:limit]

        return {
            "query": query,
            "mode": mode,
            "total_matches": len(matched_nodes),
            "results": top_matches
        }
