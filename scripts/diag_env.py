"""Environment diagnostics for MoneySmarts.
Run:  python scripts/diag_env.py
Prints interpreter, virtual environment status, paths, and critical imports.
"""
from __future__ import annotations
import sys, os, platform, site, importlib, re, pathlib

CRITICAL = os.environ.get("MONEYSMARTS_CRITICAL", "pygame").split()

REQ_SPEC = None
REQ_FILE = pathlib.Path(__file__).parent.parent / "pyproject.toml"
if REQ_FILE.exists():
    txt = REQ_FILE.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"requires-python\s*=\s*['\"]([^'\"]+)['\"]", txt)
    if m:
        REQ_SPEC = m.group(1)

def version_tuple(v: str):
    try:
        parts = [int(p) for p in v.split('.') if p.isdigit()]
        while len(parts) < 3:
            parts.append(0)
        return tuple(parts[:3])
    except Exception:
        return (0,0,0)

def spec_allows(py_ver: tuple[int,int,int], spec: str) -> bool:
    # Very small parser for expressions like ">=3.11,<3.13"
    try:
        clauses = [c.strip() for c in spec.split(',') if c.strip()]
        ok = True
        for c in clauses:
            if c.startswith(">="):
                ok &= py_ver >= version_tuple(c[2:])
            elif c.startswith(">"):
                ok &= py_ver > version_tuple(c[1:])
            elif c.startswith("<="):
                ok &= py_ver <= version_tuple(c[2:])
            elif c.startswith("<"):
                ok &= py_ver < version_tuple(c[1:])
            elif c.startswith("=="):
                ok &= py_ver == version_tuple(c[2:])
        return ok
    except Exception:
        return True

def main():
    print("=== MoneySmarts Environment Diagnostics ===")
    print(f"Python Executable : {sys.executable}")
    print(f"Version           : {sys.version.split()[0]}")
    print(f"Platform          : {platform.platform()}")
    base = getattr(sys, "base_prefix", sys.prefix)
    in_venv = sys.prefix != base
    print(f"sys.prefix        : {sys.prefix}")
    print(f"sys.base_prefix   : {base}")
    print(f"In virtualenv     : {in_venv}")
    if not in_venv:
        print("WARNING: Not inside a virtual environment (.venv).")
    if REQ_SPEC:
        py_ver = sys.version_info[:3]
        allowed = spec_allows(py_ver, REQ_SPEC)
        print(f"Project requires  : {REQ_SPEC}")
        print(f"Version allowed   : {allowed}")
        if not allowed:
            print("WARNING: Current interpreter is outside the supported range; dependency install or runtime issues may occur.")
            print("ACTION: Install a supported Python and recreate the venv, e.g.:\n  1. winget install Python.Python.3.12 -s winget\n  2. Remove old venv: rmdir /s /q .venv (CMD) or Remove-Item -Recurse -Force .venv (PowerShell)\n  3. Recreate: py -3.12 -m venv .venv\n  4. Activate: .venv\\Scripts\\activate (CMD) or . .venv/Scripts/Activate.ps1 (PowerShell)\n  5. Install deps: python -m pip install -e .[dev]")
    print(f"Working Dir       : {os.getcwd()}")
    print("First 5 sys.path entries:")
    for p in sys.path[:5]:
        print("  -", p)
    try:
        sp = site.getsitepackages()
    except Exception:
        sp = []
    if sp:
        print("Site Packages:")
        for s in sp:
            print("  *", s)
    print("PATH (first 3):")
    for seg in os.environ.get("PATH", "").split(os.pathsep)[:3]:
        print("  -", seg)
    print("\nCritical imports:")
    for name in CRITICAL:
        if not name:
            continue
        try:
            importlib.import_module(name)
            print(f"  {name:<15} OK")
        except Exception as e:
            print(f"  {name:<15} FAIL - {e.__class__.__name__}: {e}")
    print("=== End Diagnostics ===")

if __name__ == "__main__":
    main()
