# -*- coding: utf-8 -*-
"""Provenance Tracker and Memory Versioning Manager for NOVEL OS V2.2."""

from __future__ import annotations
import hashlib
from typing import Dict, Any, List
from .memory_delta import MemoryDelta, Provenance, MemoryLifecycle


class ProvenanceTracker:
    """Tracks origin chapter, cryptographic hash, and lifecycle versioning."""

    @staticmethod
    def seal_provenance(delta: MemoryDelta, author: str = "MASTER_ORCHESTRATOR") -> Provenance:
        content_bytes = f"{delta.entity}:{delta.claim}:{delta.source_chapter}".encode("utf-8")
        h = hashlib.sha256(content_bytes).hexdigest()
        prov = delta.provenance
        prov.source_hash = h
        prov.created_by = author
        prov.approved_by = "HUMAN_AUTHORIZED_PIPELINE"
        return prov
