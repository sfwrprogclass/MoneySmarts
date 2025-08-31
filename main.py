"""
Money Smartz: Financial Life Simulator

This is the main entry point for the Money Smartz game.
It initializes the game and starts the main game loop.
"""

import sys
# --- Python version guard (pygame wheels not yet for 3.14; project targets 3.11/3.12) ---
if not ((3, 11) <= sys.version_info < (3, 13)):
    print(f"Unsupported Python version {sys.version.split()[0]} detected.\n"
          f"Use Python 3.11 or 3.12. (Current pyproject requires >=3.11,<3.13)\n"
          f"Fix: Install Python 3.12, recreate venv, then: pip install -r requirements.txt")
    sys.exit(1)

# Delay pygame import until after version check for clearer messaging
try:
    import pygame
except ModuleNotFoundError:
    print("pygame not installed. In an activated venv run: pip install -r requirements.txt")
    sys.exit(1)

import traceback
import logging
from moneySmarts import Game, GUIManager
from moneySmarts.screens import TitleScreen
from moneySmarts.exceptions import GameError

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

def main():
    """
    Main function that initializes and runs the game.
    Sets up error logging and handles uncaught exceptions.
    """
    # Set up logging
    logging.basicConfig(
        filename='money_smarts.log',
        level=logging.ERROR,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    try:
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        try:
            pygame.mixer.init()
        except Exception:
            print("Warning: Audio mixer init failed - continuing without sound.")

        # Make the window resizable (use constants)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Money Smartz")

        # Create a game instance
        game = Game()
        game.screen = screen  # Pass screen to game if needed

        # Create a GUI manager
        gui_manager = GUIManager(game)
        game.gui_manager = gui_manager

        # Set initial screen
        gui_manager.set_screen(TitleScreen(game))

        # Main game loop
        gui_manager.run()
    except GameError as ge:
        logging.error(f"Game error: {ge}")
        print(f"A game error occurred: {ge}")
    except Exception:
        logging.error("Uncaught exception:", exc_info=True)
        print("An unexpected error occurred. Please check money_smarts.log for details.")
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
