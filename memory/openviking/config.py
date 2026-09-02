# -*- coding: utf-8 -*-
"""Configuration for OpenViking Adapter."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class OpenVikingConfig:
    enabled: bool = True
    base_uri: str = "viking://resources/novel"
    local_storage_dir: str = ".openviking/storage"
    max_l0_items: int = 20
    max_l1_items: int = 15
    max_l2_items: int = 5
    health_check_timeout_seconds: float = 2.0
    embedding_dimension: int = 1536
    rerank_model: str = "openviking-rerank-v1"
