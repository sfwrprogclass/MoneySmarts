"""
Image management utilities for the Money Smarts game.
"""

import pygame
import os
from moneySmartz.constants import EXTERIORS_DIR, INTERIORS_DIR, BUILDING_IMAGES


class ImageManager:
    """
    Manages loading and caching of game images.
    """
    
    def __init__(self):
        self.image_cache = {}
        self._display_initialized = False
        
    def _ensure_display(self):
        """Ensure pygame display is initialized for image loading."""
        if not self._display_initialized:
            try:
                # Try to set a display mode
                pygame.display.set_mode((1, 1), pygame.NOFRAME)
                self._display_initialized = True
            except pygame.error:
                # If display mode fails, continue anyway - some operations might still work
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
        
        # Use absolute path from game root
        abs_path = os.path.abspath(filepath)
        
        # Check cache first
        cache_key = f"{abs_path}_{size}" if size else abs_path
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        try:
            if os.path.exists(abs_path):
                image = pygame.image.load(abs_path)
                
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
                # File doesn't exist
                return None
                
        except pygame.error as e:
            print(f"Error loading image {abs_path}: {e}")
            return None
    
    def get_building_image(self, building_name, image_type, size=None):
        """
        Get a specific building image.
        
        Args:
            building_name (str): Name of the building type
            image_type (str): Either 'exterior' or 'interior'
            size (tuple): Optional size tuple (width, height) to resize image
            
        Returns:
            pygame.Surface: Loaded image surface, or None if not found
        """
        if building_name not in BUILDING_IMAGES:
            return None
            
        if image_type not in BUILDING_IMAGES[building_name]:
            return None
            
        filename = BUILDING_IMAGES[building_name][image_type]
        
        if image_type == 'exterior':
            filepath = os.path.join(EXTERIORS_DIR, filename)
        elif image_type == 'interior':
            filepath = os.path.join(INTERIORS_DIR, filename)
        else:
            return None
            
        return self.load_image(filepath, size)
    
    def clear_cache(self):
        """Clear the image cache."""
        self.image_cache.clear()


# Global image manager instance
image_manager = ImageManager()