import os

# Assets directory (canonical)
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')

# Assets
PIXEL_FONT = "pixelated_font.ttf"  # Name of your font file
TITLE_IMAGE = "title_background.jpg"  # Title image file name

#Gold Coin
GOLD = (212, 175, 55)
DARK_GOLD = (150, 120, 40)

# GUI Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 255)
LIGHT_BLUE = (100, 180, 255)
GREEN = (0, 200, 0)
LIGHT_GREEN = (100, 255, 100)
RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)

# Modern theme (new)
PRIMARY = (56, 97, 251)          # Indigo blue
PRIMARY_HOVER = (76, 117, 255)
PRIMARY_TEXT = WHITE

ACCENT = (0, 196, 140)           # Teal/green accent
ACCENT_HOVER = (0, 216, 160)

DANGER = (232, 65, 66)
WARNING = (255, 168, 0)
SUCCESS = (34, 197, 94)

# Background gradient
BG_TOP = (245, 247, 250)
BG_BOTTOM = (225, 230, 240)

CARD_BG = (250, 252, 255)
CARD_BORDER = (220, 226, 235)
SHADOW = (0, 0, 0, 50)

# Font sizes
FONT_SMALL = 18
FONT_MEDIUM = 24
FONT_LARGE = 32
FONT_TITLE = 48

# Asset paths (derived from ASSETS_DIR)
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
BUILDINGS_DIR = os.path.join(IMAGES_DIR, 'buildings')
EXTERIORS_DIR = os.path.join(BUILDINGS_DIR, 'exteriors')
INTERIORS_DIR = os.path.join(BUILDINGS_DIR, 'interiors')

# Building image filenames
BUILDING_IMAGES = {
    "Small Starter Home": {
        "exterior": "starter_home.png",
        "interior": "starter_home_interior.png"
    },
    "Mid-size Family Home": {
        "exterior": "family_home.png",
        "interior": "family_home_interior.png"
    },
    "Large Luxury Home": {
        "exterior": "luxury_home.png",
        "interior": "luxury_home_interior.png"
    },
    "Urban Condo": {
        "exterior": "urban_condo.png",
        "interior": "urban_condo_interior.png"
    }
}

# Vehicle image filenames and financial data
VEHICLE_IMAGES = {
    "Used Car": {
        "image": "vehicle_used_car.png",
        "base_value": 5000,
        "depreciation_rate": 0.15,
        "maintenance_cost": 400,
        "insurance_cost": 600
    },
    "Sedan": {
        "image": "vehicle_sedan.png",
        "base_value": 18000,
        "depreciation_rate": 0.18,
        "maintenance_cost": 600,
        "insurance_cost": 900
    },
    "SUV": {
        "image": "vehicle_suv.png",
        "base_value": 25000,
        "depreciation_rate": 0.20,
        "maintenance_cost": 800,
        "insurance_cost": 1200
    }
}

# Building financial data
BUILDING_DATA = {
    "Small Starter Home": {
        "base_value": 120000,
        "depreciation_rate": 0.01,
        "maintenance_cost": 1200,
        "insurance_cost": 800,
        "property_tax": 1800
    },
    "Mid-size Family Home": {
        "base_value": 220000,
        "depreciation_rate": 0.012,
        "maintenance_cost": 1800,
        "insurance_cost": 1200,
        "property_tax": 3200
    },
    "Large Luxury Home": {
        "base_value": 450000,
        "depreciation_rate": 0.015,
        "maintenance_cost": 3500,
        "insurance_cost": 2500,
        "property_tax": 7000
    },
    "Urban Condo": {
        "base_value": 180000,
        "depreciation_rate": 0.011,
        "maintenance_cost": 1000,
        "insurance_cost": 900,
        "property_tax": 2200
    }
}
