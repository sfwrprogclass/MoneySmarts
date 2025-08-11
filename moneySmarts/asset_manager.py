"""
AssetManager for preloading and managing game assets with error handling.
"""
import os
import pygame
import logging

class AssetManager:
    def __init__(self, asset_root="assets"):
        self.asset_root = asset_root
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, path, key=None):
        full_path = os.path.join(self.asset_root, path)
        try:
            image = pygame.image.load(full_path)
            if key is None:
                key = path
            self.images[key] = image
            return image
        except Exception as e:
            logging.error(f"Failed to load image '{full_path}': {e}")
            return None

    def get_image(self, key):
        return self.images.get(key)

    def load_sound(self, path, key=None):
        full_path = os.path.join(self.asset_root, path)
        try:
            sound = pygame.mixer.Sound(full_path)
            if key is None:
                key = path
            self.sounds[key] = sound
            return sound
        except Exception as e:
            logging.error(f"Failed to load sound '{full_path}': {e}")
            return None

    def get_sound(self, key):
        return self.sounds.get(key)

    def load_font(self, path, size, key=None):
        full_path = os.path.join(self.asset_root, path)
        try:
            font = pygame.font.Font(full_path, size)
            if key is None:
                key = f"{path}:{size}"
            self.fonts[key] = font
            return font
        except Exception as e:
            logging.error(f"Failed to load font '{full_path}': {e}")
            return None

    def get_font(self, key):
        return self.fonts.get(key)

    def get_asset_value(self, asset_type, name, years_owned=0):
        """
        Calculate the current value of an asset (vehicle or building) based on depreciation.
        """
        from moneySmarts.constants import VEHICLE_IMAGES, BUILDING_DATA
        if asset_type == "vehicle" and name in VEHICLE_IMAGES:
            base = VEHICLE_IMAGES[name]["base_value"]
            rate = VEHICLE_IMAGES[name]["depreciation_rate"]
            return max(500, int(base * ((1 - rate) ** years_owned)))
        elif asset_type == "building" and name in BUILDING_DATA:
            base = BUILDING_DATA[name]["base_value"]
            rate = BUILDING_DATA[name]["depreciation_rate"]
            return max(10000, int(base * ((1 - rate) ** years_owned)))
        return None

    def get_asset_costs(self, asset_type, name):
        """
        Return annual costs for maintenance, insurance, and taxes (if building).
        """
        from moneySmarts.constants import VEHICLE_IMAGES, BUILDING_DATA
        if asset_type == "vehicle" and name in VEHICLE_IMAGES:
            v = VEHICLE_IMAGES[name]
            return {
                "maintenance": v["maintenance_cost"],
                "insurance": v["insurance_cost"]
            }
        elif asset_type == "building" and name in BUILDING_DATA:
            b = BUILDING_DATA[name]
            return {
                "maintenance": b["maintenance_cost"],
                "insurance": b["insurance_cost"],
                "property_tax": b["property_tax"]
            }
        return None
