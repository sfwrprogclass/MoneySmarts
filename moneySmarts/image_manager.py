"""
Image management utilities for the Money Smarts game.
"""

import pygame
import os
import logging
from moneySmarts.constants import EXTERIORS_DIR, INTERIORS_DIR, BUILDING_IMAGES

class ImageManager:
    """
    Manages loading and caching of game images.
    """
    def __init__(self):
        self.image_cache = {}
        self._display_initialized = False
    def _ensure_display(self):
        if not self._display_initialized:
            try:
                pygame.display.set_mode((1, 1), pygame.NOFRAME)
                self._display_initialized = True
            except pygame.error:
                pass
    def load_image(self, filepath, size=None):
        """
        Load an image from file with optional resizing.
        Args:
            filepath (str): Path to the image file
            size (tuple): Optional size tuple (width, height) to resize image
        Returns:
            pygame.Surface: Loaded image surface, or None if file not found
        """
        self._ensure_display()
        abs_path = os.path.abspath(filepath)
        cache_key = abs_path if size is None else f"{abs_path}_{size}"

        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        try:
            if os.path.exists(abs_path):
                image = pygame.image.load(abs_path)
                # Check for corrupt image (surface size 0)
                if image.get_width() == 0 or image.get_height() == 0:
                    logging.error(f"Corrupt image file: {abs_path}")
                    return None
                # Resize if requested
                if size:
                    image = pygame.transform.scale(image, size)
                # Convert for better performance
                if image.get_alpha():
                    image = image.convert_alpha()
                else:
                    image = image.convert()
                # Cache the image
                self.image_cache[cache_key] = image
                return image
            else:
                logging.warning(f"Image file not found: {abs_path}")
                return None
        except pygame.error as e:
            logging.error(f"Error loading image {abs_path}: {e}")
            return None

# Singleton instance for easy import
image_manager = ImageManager()
