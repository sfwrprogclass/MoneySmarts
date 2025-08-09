# Building Images System

This document explains how to add and use building images in the Money Smarts game.

## Overview

The game now supports displaying actual images for building exteriors and interiors, with automatic fallback to simple pygame drawings when images are not available.

## Supported Building Types

The game supports four building types, each with exterior and interior images:

1. **Small Starter Home** - A modest entry-level home
2. **Mid-size Family Home** - A comfortable family residence  
3. **Large Luxury Home** - A spacious high-end property
4. **Urban Condo** - A modern city condominium

## Image Files

Building images should be placed in the following directory structure:

```
assets/
└── images/
    └── buildings/
        ├── exteriors/
        │   ├── starter_home.png
        │   ├── family_home.png
        │   ├── luxury_home.png
        │   └── urban_condo.png
        └── interiors/
            ├── starter_home_interior.png
            ├── family_home_interior.png
            ├── luxury_home_interior.png
            └── urban_condo_interior.png
```

## Image Guidelines

- **Format**: PNG is recommended for best quality and transparency support
- **Exterior Size**: 400x300 pixels (will be scaled to display size)
- **Interior Size**: 600x400 pixels (will be scaled to display size)
- **Game Resolution**: Images are optimized for display at 1024x768
- **Fallback**: If images are missing, the game automatically falls back to simple geometric drawings

## How It Works

### Image Manager

The `ImageManager` class handles:
- Loading images from the file system
- Caching images for performance
- Automatic scaling to requested sizes
- Graceful fallback when images are not found

### HousingScreen Integration

The `HousingScreen` now includes:
- **State 0 (House Selection)**: Shows a preview of the currently selected house
- **State 2 (Confirmation)**: Displays both exterior and interior images side by side
- **Fallback Drawing**: Uses simple pygame primitives when images are unavailable

### Usage Example

```python
from moneySmartz.image_manager import image_manager

# Load an exterior image
exterior_image = image_manager.get_building_image(
    'Small Starter Home', 'exterior', size=(200, 150)
)

# Load an interior image
interior_image = image_manager.get_building_image(
    'Large Luxury Home', 'interior', size=(300, 200)
)

# Both will return None if the image file doesn't exist
```

## Adding New Building Types

To add new building types:

1. Add the building definition to `BUILDING_IMAGES` in `constants.py`:
```python
BUILDING_IMAGES = {
    # ... existing buildings ...
    "New Building Type": {
        "exterior": "new_building.png",
        "interior": "new_building_interior.png"
    }
}
```

2. Add the building option to the HousingScreen's `house_options` list

3. Create the corresponding image files in the assets directory

## Adding Images from ZIP Files

The original issue mentioned several ZIP files with modern building images. To use these:

1. Extract the ZIP files to a temporary directory
2. Select appropriate images for each building type
3. Rename and resize them according to the guidelines above
4. Place them in the correct asset directories

## Future Enhancements

Potential improvements to the image system:
- Support for multiple image variations per building type
- Animated building images
- Seasonal variations
- Interior room-specific images
- Car and other asset images
- Dynamic image loading based on player preferences

## Technical Details

- Images are loaded once and cached for performance
- The system gracefully handles missing files
- All image operations are thread-safe
- The fallback drawing system maintains visual consistency
- Images support transparency (PNG alpha channel)