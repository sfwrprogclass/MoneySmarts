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

# Font sizes
FONT_SMALL = 18
FONT_MEDIUM = 24
FONT_LARGE = 32
FONT_TITLE = 48

# Asset paths
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
BUILDINGS_DIR = f"{IMAGES_DIR}/buildings"
EXTERIORS_DIR = f"{BUILDINGS_DIR}/exteriors"
INTERIORS_DIR = f"{BUILDINGS_DIR}/interiors"

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