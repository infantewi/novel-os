# -*- coding: utf-8 -*-
"""OpenViking Adapter Facade."""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Optional
from .client import OpenVikingClient
from .retrieval import HierarchicalRetrieval
from .context_assembler import ContextAssembler
from .health import HealthMonitor
from .uri_mapper import VikingURIMapper


class OpenVikingAdapter:
    """Master facade for OpenViking storage, retrieval, and context assembly."""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.client = OpenVikingClient(storage_root=self.project_root / ".openviking" / "storage")
        self.retrieval = HierarchicalRetrieval(self.client)
        self.assembler = ContextAssembler(self.retrieval)
        self.health = HealthMonitor()
        self.uri_mapper = VikingURIMapper()

    def ingest_node(self, uri: str, l0: str, l1: Dict[str, Any], l2: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> bool:
        return self.client.write_node(uri, l0, l1, l2, metadata)

    def query(self, query_str: str, mode: str = "context", limit: int = 5) -> Dict[str, Any]:
        return self.client.search(query=query_str, mode=mode, limit=limit)

    def assemble_context(self, chapter: int, objective: str, location: str, pov: str, active_characters: List[str], active_hooks: List[str]) -> Dict[str, Any]:
        return self.assembler.assemble(chapter, objective, location, pov, active_characters, active_hooks)
