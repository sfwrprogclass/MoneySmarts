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

def _list_images_recursive(root: str):
    """Recursively list all image files under a directory."""
    image_files = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if _is_image(fname):
                image_files.append(os.path.join(dirpath, fname))
    return image_files

def discover_buildings() -> List[BuildingDef]:
    buildings: List[BuildingDef] = []
    # Directories
    ex_bld_dir = os.path.join(IMAGES_DIR, 'buildings', 'exteriors')
    ex_misc_dir = os.path.join(IMAGES_DIR, 'exteriors')
    int_bld_dir = os.path.join(IMAGES_DIR, 'buildings', 'interiors')
    int_misc_dir = os.path.join(IMAGES_DIR, 'interiors')

    # Gather exteriors (both dirs, recursively)
    exterior_files = []
    for d in (ex_bld_dir, ex_misc_dir):
        exterior_files.extend(_list_images_recursive(d))
    # Map normalized name -> list of exteriors
    exterior_index = {}
    for path in exterior_files:
        base = os.path.splitext(os.path.basename(path))[0]
        exterior_index.setdefault(_norm(base), []).append(path)

    # Gather interiors with preference order (hd > mobile > normal, recursively)
    interior_candidates = {}
    for d in (int_bld_dir, int_misc_dir):
        for f in _list_images_recursive(d):
            low = os.path.basename(f).lower()
            if 'interior' not in low:
                continue
            full = f
            base = low
            # Derive logical key
            key = base
            for suffix in ('_interior_hd','_interior_mobile','_interior'):
                if key.endswith('.png'):
                    key = key[:-4]
                if key.endswith(suffix):
                    key = key[:-len(suffix)]
            key_norm = _norm(key)
            # Preference order: hd > mobile > normal
            if key_norm not in interior_candidates or 'hd' in base:
                interior_candidates[key_norm] = full

    # Build BuildingDef list
    for key_norm, exteriors in exterior_index.items():
        btype = _classify(key_norm)
        display_name = SPECIAL_TITLES.get(btype, key_norm.title())
        exterior_path = exteriors[0] if exteriors else None
        interior_path = interior_candidates.get(key_norm)
        buildings.append(BuildingDef(
            key=key_norm,
            display_name=display_name,
            exterior_path=exterior_path,
            interior_path=interior_path,
            btype=btype
        ))
    return buildings

def discover_roads() -> list:
    road_dir = os.path.join(IMAGES_DIR, 'buildings', 'exteriors', 'modernexteriors-win', 'Modern_Exteriors_48x48')
    road_tiles = []
    for root, _, files in os.walk(road_dir):
        for f in files:
            if 'road' in f.lower() and _is_image(f):
                road_tiles.append(os.path.join(root, f))
    return road_tiles

def discover_vehicles() -> list:
    vehicle_dir = os.path.join(IMAGES_DIR, 'buildings', 'exteriors', 'modernexteriors-win', 'Modern_Exteriors_48x48', 'ME_Theme_Sorter_48x48', '10_Vehicles_Singles_48x48')
    vehicles = []
    for f in _list_images_recursive(vehicle_dir):
        vehicles.append(f)
    return vehicles

def discover_shopping_centers() -> list:
    shop_dir = os.path.join(IMAGES_DIR, 'buildings', 'exteriors', 'modernexteriors-win', 'Modern_Exteriors_48x48', 'ME_Theme_Sorter_48x48', '9_Shopping_Center_and_Markets_Singles_48x48')
    shops = []
    for f in _list_images_recursive(shop_dir):
        shops.append(f)
    return shops

# --- Asset discovery caches ---
_asset_cache = {}

# --- Caching wrappers ---
def cached_discover_buildings():
    if 'buildings' not in _asset_cache:
        _asset_cache['buildings'] = discover_buildings()
    return _asset_cache['buildings']

def cached_discover_roads():
    if 'roads' not in _asset_cache:
        _asset_cache['roads'] = discover_roads()
    return _asset_cache['roads']

def cached_discover_vehicles():
    if 'vehicles' not in _asset_cache:
        _asset_cache['vehicles'] = discover_vehicles()
    return _asset_cache['vehicles']

def cached_discover_shopping_centers():
    if 'shopping_centers' not in _asset_cache:
        _asset_cache['shopping_centers'] = discover_shopping_centers()
    return _asset_cache['shopping_centers']

__all__ = ['BuildingDef','discover_buildings','discover_roads','discover_vehicles','discover_shopping_centers',
           'cached_discover_buildings','cached_discover_roads','cached_discover_vehicles','cached_discover_shopping_centers']
