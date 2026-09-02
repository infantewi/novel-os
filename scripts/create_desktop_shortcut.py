# -*- coding: utf-8 -*-
"""Create desktop shortcut for Obsidian opening the Novel Vault."""

from pathlib import Path
import pythoncom
from win32com.shell import shell

desktop = Path("C:/Users/hairaito/Desktop")
for p in desktop.glob("*Obsidian*"):
    p.unlink(missing_ok=True)

link = pythoncom.CoCreateInstance(
    shell.CLSID_ShellLink, None,
    pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
)
link.SetPath(r"C:\Program Files\Obsidian\Obsidian.exe")
link.SetArguments(r"obsidian://open?path=D:\Ai work\novel\NOVEL_OS_VAULT")
link.SetWorkingDirectory(r"D:\Ai work\novel\NOVEL_OS_VAULT")
link.SetDescription("\u6253\u5f00\u90fd\u5e02\u4ed9\u5c0a\u5c0f\u8bf4\u6b63\u6587\u4e0e\u5de5\u4f5c\u533a")
link.SetIconLocation(r"C:\Program Files\Obsidian\Obsidian.exe", 0)

persist_file = link.QueryInterface(pythoncom.IID_IPersistFile)
# \u6b63\u6587 = "正文"
target_path = str(desktop / "\u6b63\u6587 - Obsidian.lnk")
persist_file.Save(target_path, 0)

print(f"Shortcut created: {Path(target_path).exists()}")
print(f"Raw Path: {target_path}")
print(f"Unicode Escaped: {target_path.encode('unicode_escape')}")
