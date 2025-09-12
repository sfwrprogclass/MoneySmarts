import os
import json

# Configuration
ASSET_ROOT = os.path.join(os.path.dirname(__file__), 'assets', 'images')
LDTK_OUT = os.path.join(os.path.dirname(__file__), 'auto_generated.ldtk')
TILE_SIZE = 48  # Change if your tiles are a different size

# Helper to find all tileset images

def find_tilesets(asset_root):
    if not os.path.exists(asset_root):
        print(f"ERROR: Asset folder not found: {asset_root}")
        return []
    tilesets = []
    for root, dirs, files in os.walk(asset_root):
        for fname in files:
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                rel_path = os.path.relpath(os.path.join(root, fname), os.path.dirname(__file__))
                tilesets.append({
                    'rel_path': rel_path.replace('\\', '/'),
                    'name': fname.split('.')[0]
                })
    return tilesets

# Build LDtk project JSON

def build_ldtk_project(tilesets):
    ldtk = {
        "jsonVersion": "1.6.0",
        "defaultGridSize": TILE_SIZE,
        "defaultLevelWidth": 40,
        "defaultLevelHeight": 20,
        "levels": [
            {
                "identifier": "Overworld",
                "iid": "level_1",
                "worldX": 0,
                "worldY": 0,
                "pxWid": 40 * TILE_SIZE,
                "pxHei": 20 * TILE_SIZE,
                "layerInstances": [],
            }
        ],
        "defs": {
            "tilesets": [],
            "layers": [
                {
                    "type": "Tiles",
                    "identifier": "Terrain",
                    "gridSize": TILE_SIZE,
                },
                {
                    "type": "Tiles",
                    "identifier": "Buildings",
                    "gridSize": TILE_SIZE,
                },
                {
                    "type": "Tiles",
                    "identifier": "Roads",
                    "gridSize": TILE_SIZE,
                }
            ],
            "entities": []
        }
    }
    # Add tilesets
    for i, ts in enumerate(tilesets):
        ldtk['defs']['tilesets'].append({
            "identifier": ts['name'],
            "relPath": ts['rel_path'],
            "uid": 1000 + i,
            "tileGridSize": TILE_SIZE,
            "pxWid": TILE_SIZE,  # You can update this to actual image size if needed
            "pxHei": TILE_SIZE
        })
    return ldtk

if __name__ == '__main__':
    print("Scanning asset root:", ASSET_ROOT)
    tilesets = find_tilesets(ASSET_ROOT)
    if not tilesets:
        print("No tilesets found. Please check your asset folder path and contents.")
    else:
        ldtk_project = build_ldtk_project(tilesets)
        with open(LDTK_OUT, 'w') as f:
            json.dump(ldtk_project, f, indent=2)
        print(f'LDtk project generated: {LDTK_OUT}')
        print('Open this file in LDtk to start editing your world!')
