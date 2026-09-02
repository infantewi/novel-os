# -*- coding: utf-8 -*-
"""Hierarchical Retrieval Engine with Rerank and Trajectory Tracking."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from .client import OpenVikingClient


@dataclass
class RetrievalTrace:
    trace_id: str
    query: str
    intent: str
    candidates_count: int
    l0_hits: List[str]
    l1_escalated: List[str]
    l2_escalated: List[str]
    rerank_scores: Dict[str, float]
    final_uris: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class HierarchicalRetrieval:
    """Orchestrates L0 -> L1 -> L2 progressive resolution with rerank and full trace tracking."""

    def __init__(self, client: OpenVikingClient):
        self.client = client

    def retrieve(self, query: str, intent: str = "GENERAL", max_l2_nodes: int = 3) -> Dict[str, Any]:
        search_res = self.client.search(query=query, mode="standard", limit=20)
        results = search_res.get("results", [])

        l0_hits = [r["uri"] for r in results]
        l1_escalated = [r["uri"] for r in results[:5]]
        l2_escalated = [r["uri"] for r in results[:max_l2_nodes]]

        rerank_scores = {r["uri"]: r["score"] for r in results[:max_l2_nodes]}

        l0_payload = [r["l0_abstract"] for r in results]
        l1_payload = [r["l1_overview"] for r in results[:5] if r.get("l1_overview")]
        l2_payload = []
        for uri in l2_escalated:
            node = self.client.get_node(uri)
            if node:
                l2_payload.append(node.get("l2_details", {}))

        trace = RetrievalTrace(
            trace_id=f"TRACE-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            query=query,
            intent=intent,
            candidates_count=len(results),
            l0_hits=l0_hits,
            l1_escalated=l1_escalated,
            l2_escalated=l2_escalated,
            rerank_scores=rerank_scores,
            final_uris=l2_escalated
        )

        return {
            "l0": l0_payload,
            "l1": l1_payload,
            "l2": l2_payload,
            "trace": trace
        }
