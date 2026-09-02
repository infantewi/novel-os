# -*- coding: utf-8 -*-
"""Atomic Commit Gate for Memory transactions."""

from __future__ import annotations
import os
import json
from pathlib import Path
from typing import Dict, Any, List


class AtomicCommitGate:
    """Guarantees atomic memory state persistence without half-written states."""

    def __init__(self, store_file: Path):
        self.store_file = Path(store_file)

    def read_store(self) -> List[Dict[str, Any]]:
        if not self.store_file.exists():
            return []
        try:
            with open(self.store_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def commit(self, records: List[Dict[str, Any]], simulate_failure: bool = False) -> bool:
        self.store_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self.store_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)

            if simulate_failure:
                raise IOError("Simulated storage failure during memory commit")

            os.replace(temp_file, self.store_file)
            return True
        except Exception:
            if temp_file.exists():
                temp_file.unlink()
            return False
