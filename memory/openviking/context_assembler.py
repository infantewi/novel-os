# -*- coding: utf-8 -*-
"""Context Assembler 2.0 for NOVEL OS V2.2."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from .retrieval import HierarchicalRetrieval


class ContextAssembler:
    """Assembles structured Context Contract v2.2 packages."""

    def __init__(self, retrieval_engine: HierarchicalRetrieval):
        self.retrieval = retrieval_engine

    def assemble(self, chapter: int, objective: str, location: str, pov: str, active_characters: List[str], active_hooks: List[str]) -> Dict[str, Any]:
        query = f"Chapter {chapter} {location} {pov} {' '.join(active_characters)} {objective}"
        retrieval_res = self.retrieval.retrieve(query=query, intent="CHAPTER_PREPARATION")

        trace = retrieval_res["trace"]

        return {
            "l0": {
                "chapter": chapter,
                "location": location,
                "pov": pov,
                "active_characters": active_characters,
                "objective": objective,
                "abstracts": retrieval_res["l0"][:5]
            },
            "l1": {
                "overviews": retrieval_res["l1"],
                "active_hooks": active_hooks
            },
            "l2": {
                "details": retrieval_res["l2"]
            },
            "canon_facts": [f"陆辰境界：筑基初期 (液态真元)", "本命法宝：惊鸿剑 (下品灵器)"],
            "state_facts": [f"当前锚定章节: {chapter-1} 完结，当前目标: Chapter {chapter}"],
            "timeline_facts": ["秋季正午十二点整，公海决战"],
            "character_facts": {c: "Active" for c in active_characters},
            "relationship_facts": {"孙侯": "Hostile/Defeated", "巴颂": "Hostile/Active"},
            "foreshadow_facts": active_hooks,
            "knowledge_boundary": {
                "protagonist_knowledge": "Known: 洪门与黑巫教联合伏击",
                "unrevealed_facts": "Unknown: 北美黑水潜伏坐标"
            },
            "retrieval_trace": {
                "trace_id": trace.trace_id,
                "candidates": trace.candidates_count,
                "l0_count": len(trace.l0_hits),
                "l1_count": len(trace.l1_escalated),
                "l2_count": len(trace.l2_escalated),
                "final_uris": trace.final_uris
            },
            "provenance": {
                "source_system": "OpenViking Context Assembler 2.0",
                "version": "2.2.0"
            }
        }
