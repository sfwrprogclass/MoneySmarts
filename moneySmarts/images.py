"""
Centralized image file references for MoneySmarts game.
Change the file name here to update the image everywhere in the game.
"""
import os

IMAGES = {
    "TITLE_BG": "title_background.jpg",
    "BANK_BG": "BankDetails-0004.png",
    "CARD_IMAGE": "card_image.png",
    "DEBIT_BG": "debit_background.png",
    "GRADUATION_CAP": "graduation_cap_pixel.png",
    "HOME_FAMILY": "home_family.png",
    "HOME_LUXURY": "home_luxury.png",
    "HOME_STARTER": "home_starter.png",
    "INTRO_BG": "intro_background.png",
    "JOB_SEARCH_BG": "job search bg.png",
    "LIFE_EVENT_GREEN": "Life-Event-Green.jpg",
    "LIFE_EVENT_RED": "Life-Event-Red.jpg",
    "LOGO": "Money Smarts logo.png",
    "NAME_BG": "name_background.png",
    "START_MENU_BG": "StartMenuBG-Recovered.png",
    "VEHICLE_SEDAN": "vehicle_sedan.png",
    "VEHICLE_SUV": "vehicle_suv.png",
    "VEHICLE_USED": "vehicle_used_car.png",
    "WITHDRAW_BG": "WithdrawalBGV4.png",
    # Add more as needed
}

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

def get_image_path(key):
    """Return the full path to the image file for the given key."""
    return os.path.join(ASSETS_DIR, IMAGES[key])

# Usage example:
# pygame.image.load(get_image_path("TITLE_BG"))

