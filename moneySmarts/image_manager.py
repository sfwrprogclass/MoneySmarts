"""
Image management utilities for the Money Smarts game.
"""

import pygame
import os
import logging
import shutil
from moneySmarts.constants import EXTERIORS_DIR, INTERIORS_DIR, BUILDING_IMAGES

class ImageManager:
    """
    Manages loading and caching of game images.
    """
    def __init__(self):
        self.image_cache = {}
        self.image_mod_times = {}
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

        # Hot swap: reload if file changed
        mod_time = os.path.getmtime(abs_path) if os.path.exists(abs_path) else None
        if cache_key in self.image_cache:
            if mod_time and self.image_mod_times.get(cache_key) == mod_time:
                return self.image_cache[cache_key]
            # File changed, reload
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
                self.image_mod_times[cache_key] = mod_time
                return image
            else:
                logging.warning(f"Image file not found: {abs_path}")
                return None
        except pygame.error as e:
            logging.error(f"Error loading image {abs_path}: {e}")
            return None

    @staticmethod
    def export_images_for_unity(source_dir, export_dir):
        """
        Copy all PNG/JPG images from source_dir to export_dir for Unity use.
        """
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, source_dir)
                    dst_path = os.path.join(export_dir, rel_path)
                    dst_folder = os.path.dirname(dst_path)
                    if not os.path.exists(dst_folder):
                        os.makedirs(dst_folder)
                    shutil.copy2(src_path, dst_path)

def automate_unity_export():
    """
    Automatically export all images in assets/images to assets/unity_export for Unity use.
    """
    source_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
    export_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'unity_export')
    export_dir = os.path.abspath(export_dir)
    image_manager.export_images_for_unity(source_dir, export_dir)
    print(f"Exported images for Unity to: {export_dir}")

# Singleton instance for easy import
image_manager = ImageManager()

# Optionally, run on import or provide a CLI entry point
if __name__ == "__main__":
    automate_unity_export()
