import pygame
from moneySmarts.ui import Screen, Button
from moneySmarts.constants import *

class InventoryScreen(Screen):
    """
    InventoryScreen displays the player's purchased assets in a scrollable list.
    Allows the player to view asset details and return to the main game screen.

    Attributes:
        game: Reference to the main game object.
        back_btn: Button to return to the previous screen.
    """
    def __init__(self, game):
        """
        Initialize the inventory screen and create the back button.
        Args:
            game: The main game object.
        """
        super().__init__(game)
        self.back_btn = Button(40, 40, 120, 40, "Back", action=self.go_back)

    def go_back(self):
        """
        Return to the main game screen.
        """
        from moneySmarts.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def draw(self, surface):
        """
        Draw the inventory screen, showing all player assets and the back button.
        Args:
            surface: The pygame surface to draw on.
        """
        surface.fill((245, 245, 255))
        font = pygame.font.SysFont('Arial', 32)
        title = font.render("Inventory", True, BLUE)
        surface.blit(title, (40, 100))
        y = 160
        font_small = pygame.font.SysFont('Arial', 24)
        if not self.game.player.assets:
            surface.blit(font_small.render("No items purchased yet.", True, BLACK), (40, y))
        else:
            for asset in self.game.player.assets:
                # Show asset name, type, value, and condition for realism
                asset_text = f"{asset.name} ({asset.asset_type}) - ${asset.current_value:.2f} - {asset.condition}"
                surface.blit(font_small.render(asset_text, True, BLACK), (40, y))
                y += 40
        self.back_btn.draw(surface)

    def handle_event(self, event):
        """
        Handle mouse click events for the inventory screen.
        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_btn.rect.collidepoint(mouse_pos):
                if self.back_btn.action:
                    self.back_btn.action()
