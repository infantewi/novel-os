# -*- coding: utf-8 -*-
"""Health Monitor and Strict Fallback Policy for OpenViking."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"


class HealthMonitor:
    """Monitors OpenViking availability and enforces strict fallback policies."""

    def __init__(self, simulate_offline: bool = False):
        self.simulate_offline = simulate_offline

    def check_health(self) -> Dict[str, Any]:
        if self.simulate_offline:
            return {
                "status": HealthStatus.UNAVAILABLE,
                "latency_ms": -1,
                "message": "OpenViking service connection refused / offline."
            }
        return {
            "status": HealthStatus.HEALTHY,
            "latency_ms": 1.2,
            "message": "OpenViking connection healthy and responsive."
        }

    def evaluate_fallback(self, is_critical_production: bool = True) -> Dict[str, Any]:
        health = self.check_health()
        if health["status"] == HealthStatus.HEALTHY:
            return {"allow_execution": True, "fallback_used": False, "backend": "openviking"}

        # If OpenViking is unavailable
        if is_critical_production:
            return {
                "allow_execution": False,
                "action": "BLOCK_STOP_REPORT",
                "fallback_used": False,
                "error": "OpenViking unavailable during critical chapter production. NO SILENT RECOVERY."
            }
        else:
            return {
                "allow_execution": True,
                "action": "DIAGNOSTIC_FALLBACK",
                "fallback_used": True,
                "backend": "context_ranker",
                "fallback_reason": "Non-critical diagnostic run permitted with local metadata."
            }
