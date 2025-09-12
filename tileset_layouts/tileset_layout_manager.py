# -*- coding: utf-8 -*-
"""
Tileset Layout Manager
Compatible with Python 2.7+

This script helps define and export tileset layouts for RPG Maker or other engines.
"""
import os
import json
from PIL import Image

TILESET_SRC_DIR = os.path.join(os.path.dirname(__file__), '../assets/images')
LAYOUT_EXPORT_PATH = os.path.join(os.path.dirname(__file__), 'tileset_layouts.json')

# Example: Define a tileset layout as a grid of image filenames
# You can expand this to support more complex layouts or metadata

def scan_tileset_images(src_dir):
    images = []
    for fname in os.listdir(src_dir):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append(fname)
    return images

def create_simple_grid_layout(images, grid_width=8):
    layout = []
    for i in range(0, len(images), grid_width):
        row = images[i:i+grid_width]
        layout.append(row)
    return layout

def export_layout(layout, out_path):
    with open(out_path, 'w') as f:
        json.dump(layout, f, indent=2)
    print('Tileset layout exported to {}'.format(out_path))

if __name__ == '__main__':
    images = scan_tileset_images(TILESET_SRC_DIR)
    layout = create_simple_grid_layout(images)
    export_layout(layout, LAYOUT_EXPORT_PATH)

