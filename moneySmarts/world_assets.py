"""Dynamic world asset discovery for overworld building generation.
Scans images/interiors & buildings/exteriors to assemble building defs.

Naming conventions supported:
  interiors: <name>_interior_hd.png (primary) OR <name>_interior.png
  exteriors: assets/images/buildings/exteriors/<name>.png OR
             assets/images/exteriors/<name>.png
Fallback: rectangle placeholder if exterior missing.
Special display name mapping & type detection for known functional buildings
(bank, shop, jobcenter, school, housing).
"""
from __future__ import annotations
import os
import re
from dataclasses import dataclass
from typing import List, Optional
from moneySmarts.images import IMAGES_DIR, get_image_path

SPECIAL_TITLES = {
    'bank': 'Bank',
    'shop': 'Shop',
    'store': 'Shop',
    'jobcenter': 'Job Center',
    'career': 'Job Center',
    'school': 'School',
    'edu': 'School',
    'class': 'School',
    'housing': 'Housing Office',
    'home': 'Home'
}

SPECIAL_TYPES = set(['bank','shop','jobcenter','school','housing','home'])

@dataclass
class BuildingDef:
    key: str
    display_name: str
    exterior_path: Optional[str]
    interior_path: Optional[str]
    btype: str = 'generic'  # bank/shop/jobcenter/school/housing/home/generic

    @property
    def is_functional(self) -> bool:
        return self.btype in SPECIAL_TYPES

def _listdir_safe(path: str):
    try:
        return os.listdir(path)
    except OSError:
        return []

def _is_image(fname: str) -> bool:
    return fname.lower().endswith(('.png','.jpg','.jpeg','.gif'))

def _norm(name: str) -> str:
    return re.sub(r'[^a-z0-9]+','', name.lower())

def _classify(key_norm: str) -> str:
    if 'bank' in key_norm: return 'bank'
    if 'shop' in key_norm or 'store' in key_norm: return 'shop'
    if 'job' in key_norm or 'career' in key_norm: return 'jobcenter'
    if 'school' in key_norm or 'edu' in key_norm or 'class' in key_norm: return 'school'
    if 'housing' in key_norm or 'realtor' in key_norm or 'estate' in key_norm: return 'housing'
    if 'home' in key_norm or 'house' in key_norm or 'condo' in key_norm: return 'home'
    return 'generic'

def discover_buildings() -> List[BuildingDef]:
    buildings: List[BuildingDef] = []
    # Directories
    ex_bld_dir = os.path.join(IMAGES_DIR, 'buildings', 'exteriors')
    ex_misc_dir = os.path.join(IMAGES_DIR, 'exteriors')
    int_bld_dir = os.path.join(IMAGES_DIR, 'buildings', 'interiors')
    int_misc_dir = os.path.join(IMAGES_DIR, 'interiors')

    # Gather exteriors (both dirs)
    exterior_files = []
    for d in (ex_bld_dir, ex_misc_dir):
        for f in _listdir_safe(d):
            if _is_image(f):
                exterior_files.append(os.path.join(d, f))
    # Map normalized name -> list of exteriors
    exterior_index = {}
    for path in exterior_files:
        base = os.path.splitext(os.path.basename(path))[0]
        exterior_index.setdefault(_norm(base), []).append(path)

    # Gather interiors with preference order (hd > mobile > normal)
    interior_candidates = {}
    for d in (int_bld_dir, int_misc_dir):
        for f in _listdir_safe(d):
            if not _is_image(f):
                continue
            low = f.lower()
            if 'interior' not in low:
                continue
            full = os.path.join(d, f)
            base = low
            # Derive logical key
            key = base
            for suffix in ('_interior_hd','_interior_mobile','_interior'):
                if key.endswith('.png'):
                    key = key[:-4]
                if key.endswith(suffix):
                    key = key[:-len(suffix)]
            norm_key = _norm(key)
            rank = 0 if '_hd' in low else (1 if '_mobile' in low else 2)
            best = interior_candidates.get(norm_key)
            if not best or rank < best['rank']:
                interior_candidates[norm_key] = {'path': full, 'rank': rank, 'raw': f}

    used_exteriors = set()

    # Pair interiors to best exterior (exact or fuzzy match)
    for norm_key, data in interior_candidates.items():
        interior_path = data['path']
        exterior_path = None
        # Exact normalized match
        if norm_key in exterior_index:
            exterior_path = exterior_index[norm_key][0]
            used_exteriors.add(exterior_path)
        else:
            # Fuzzy contains
            for ek, paths in exterior_index.items():
                if ek and norm_key and (ek in norm_key or norm_key in ek):
                    exterior_path = paths[0]
                    used_exteriors.add(exterior_path)
                    break
        # Derive original key for display
        raw_name = data['raw']
        base = os.path.splitext(raw_name)[0]
        display_base = re.sub(r'_?interior(_hd|_mobile)?','', base, flags=re.IGNORECASE)
        key_norm = norm_key or _norm(display_base)
        btype = _classify(key_norm)
        display = SPECIAL_TITLES.get(key_norm, display_base.replace('_',' ').title())
        buildings.append(BuildingDef(key=key_norm or display_base.lower(), display_name=display, exterior_path=exterior_path, interior_path=interior_path, btype=btype))

    # Add leftover exteriors without interiors
    for norm_key, paths in exterior_index.items():
        # pick first path
        path = paths[0]
        if path in used_exteriors:
            continue
        # Avoid duplicates by key
        if any(b.key == norm_key for b in buildings):
            continue
        btype = _classify(norm_key)
        display = SPECIAL_TITLES.get(norm_key, norm_key.replace('_',' ').title())
        buildings.append(BuildingDef(key=norm_key, display_name=display, exterior_path=path, interior_path=None, btype=btype))

    # Stable ordering: functional first, then others A-Z
    priority = {'bank':0,'shop':1,'jobcenter':2,'school':3,'housing':4,'home':5,'generic':9}
    buildings.sort(key=lambda b: (priority.get(b.btype, 8), b.display_name.lower()))
    return buildings

__all__ = ['BuildingDef','discover_buildings']
