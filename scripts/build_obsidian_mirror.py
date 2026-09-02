# -*- coding: utf-8 -*-
"""Top-level CLI runner to build or update the NOVEL OS -> Obsidian Read-Only Mirror."""

import os
import sys
import yaml
from pathlib import Path

# Ensure UTF-8 stdout on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from obsidian_adapter.exporter import VaultExporter


def main():
    source_root = Path(__file__).resolve().parent.parent
    config_path = source_root / "scripts" / "obsidian_adapter" / "config.yaml"

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        vault_root = Path(cfg.get("vault_root", source_root / "NOVEL_OS_VAULT"))
    else:
        vault_root = source_root / "NOVEL_OS_VAULT"

    temp_root = source_root / "scripts" / "_temp" / "temp_vault"

    print("==================================================")
    print("NOVEL OS V2.3 — OBSIDIAN READ-ONLY MIRROR BUILDER")
    print("==================================================")
    print(f"Source Root: {source_root}")
    print(f"Vault Root:  {vault_root}")
    print(f"Temp Root:   {temp_root}")
    print("--------------------------------------------------")

    exporter = VaultExporter(source_root=source_root, vault_root=vault_root, temp_root=temp_root)
    manifest = exporter.export_all()

    print("--------------------------------------------------")
    print(f"Build Complete. Total Files: {manifest.get('total_files', 0)}")
    print("==================================================")


if __name__ == "__main__":
    main()

