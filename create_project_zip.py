"""Utility script to create a distributable zip of the MoneySmarts project.

Excludes common transient / heavy folders and files.
Run: python create_project_zip.py
"""
from __future__ import annotations
import os, zipfile, fnmatch

EXCLUDE_DIRS = {'.git', '.idea', '__pycache__', '_build', '.mypy_cache', '.pytest_cache'}
EXCLUDE_GLOBS = [
    '*.pyc', '*.pyo', '*.pyd', '*.log', 'savegame*.dat'
]
ZIP_NAME = 'MoneySmarts_project.zip'


def should_exclude_file(path: str) -> bool:
    base = os.path.basename(path)
    for pattern in EXCLUDE_GLOBS:
        if fnmatch.fnmatch(base, pattern):
            return True
    return False


def build_zip(root: str = '.'):  # pragma: no cover - simple IO wrapper
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zf:
        for cur_root, dirs, files in os.walk(root):
            # Normalize path parts and filter excluded dirs in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                full_path = os.path.join(cur_root, f)
                if full_path == os.path.abspath(__file__):
                    continue
                if should_exclude_file(full_path):
                    continue
                arcname = os.path.relpath(full_path, root)
                zf.write(full_path, arcname)
    return ZIP_NAME


def main():  # pragma: no cover
    zip_path = build_zip()
    size = os.path.getsize(zip_path)
    print(f"Created {zip_path} ({size} bytes)")


if __name__ == '__main__':
    main()

