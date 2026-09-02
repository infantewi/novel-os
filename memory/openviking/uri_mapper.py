# -*- coding: utf-8 -*-
"""Viking URI Namespace Mapper."""

from __future__ import annotations
from typing import Dict, Any


class VikingURIMapper:
    """Maps novel entities and chapters to standardized viking:// URIs."""

    BASE_NAMESPACE = "viking://resources/novel"

    NAMESPACES = {
        "canon": f"{BASE_NAMESPACE}/canon",
        "characters": f"{BASE_NAMESPACE}/characters",
        "relationships": f"{BASE_NAMESPACE}/relationships",
        "events": f"{BASE_NAMESPACE}/events",
        "timeline": f"{BASE_NAMESPACE}/timeline",
        "locations": f"{BASE_NAMESPACE}/locations",
        "foreshadow": f"{BASE_NAMESPACE}/foreshadow",
        "knowledge_boundary": f"{BASE_NAMESPACE}/knowledge-boundary",
        "chapters": f"{BASE_NAMESPACE}/chapters",
        "state": f"{BASE_NAMESPACE}/state",
        "outlines": f"{BASE_NAMESPACE}/outlines",
        "memory": f"{BASE_NAMESPACE}/memory",
    }

    @classmethod
    def get_chapter_uri(cls, chapter_id: int) -> str:
        return f"{cls.NAMESPACES['chapters']}/{chapter_id:03d}"

    @classmethod
    def get_character_uri(cls, character_name: str) -> str:
        return f"{cls.NAMESPACES['characters']}/{character_name}"

    @classmethod
    def get_entity_uri(cls, category: str, entity_name: str) -> str:
        base = cls.NAMESPACES.get(category, f"{cls.BASE_NAMESPACE}/{category}")
        return f"{base}/{entity_name}"
