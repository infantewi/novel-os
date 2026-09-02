# -*- coding: utf-8 -*-
"""Create robust desktop shortcut for Obsidian opening the Novel Vault."""

from pathlib import Path
import pythoncom
from win32com.shell import shell
import json

# Ensure obsidian.json registers NOVEL_OS_VAULT as the default open vault
cfg_path = Path("C:/Users/hairaito/AppData/Roaming/obsidian/obsidian.json")
if cfg_path.exists():
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        vaults = data.get("vaults", {})
        found = False
        for vid, vinfo in vaults.items():
            if vinfo.get("path") == r"D:\Ai work\novel\NOVEL_OS_VAULT":
                vinfo["open"] = True
                found = True
            else:
                vinfo["open"] = False
        if not found:
            vaults["34c799b081046e22"] = {
                "path": r"D:\Ai work\novel\NOVEL_OS_VAULT",
                "ts": 1788358300000,
                "open": True
            }
        data["vaults"] = vaults
        cfg_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"Warning updating obsidian.json: {e}")

desktop = Path("C:/Users/hairaito/Desktop")
for p in desktop.glob("*Obsidian*"):
    p.unlink(missing_ok=True)

# Create standard Windows .lnk shortcut
link = pythoncom.CoCreateInstance(
    shell.CLSID_ShellLink, None,
    pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
)
link.SetPath(r"C:\Program Files\Obsidian\Obsidian.exe")
link.SetArguments(r"obsidian://open?vault=34c799b081046e22")
link.SetWorkingDirectory(r"D:\Ai work\novel\NOVEL_OS_VAULT")
link.SetDescription("\u6253\u5f00\u90fd\u5e02\u4ed9\u5c0a\u5c0f\u8bf4\u6b63\u6587\u4e0e\u5de5\u4f5c\u533a")
link.SetIconLocation(r"C:\Program Files\Obsidian\Obsidian.exe", 0)

persist_file = link.QueryInterface(pythoncom.IID_IPersistFile)
target_path = str(desktop / "\u6b63\u6587 - Obsidian.lnk")
persist_file.Save(target_path, 0)

print(f"Shortcut created successfully at: {target_path}")
print(f"Exists: {Path(target_path).exists()}, Size: {Path(target_path).stat().st_size} bytes")
