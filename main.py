"""
Money Smartz: Financial Life Simulator

This is the main entry point for the Money Smartz game.
It initializes the game and starts the main game loop.
"""

import pygame
import sys
import traceback
import logging
from moneySmarts import Game, GUIManager
from moneySmarts.screens import GameScreen, TitleScreen, CreditCardScreen
from moneySmarts.screens.base_screens import NameInputScreen, IntroScreen
from moneySmarts.exceptions import GameError
from moneySmarts.screens.financial_screens import (
    BankAccountScreen, BankDetailsScreen, DepositScreen, WithdrawScreen,
    GetDebitCardScreen, CreditCardDetailsScreen, PayCreditCardScreen,
    LoanDetailsScreen, ExtraLoanPaymentScreen, AssetDetailsScreen,
    JobSearchScreen
)
from moneySmarts.screens.life_event_screens import (
    HighSchoolGraduationScreen, CollegeGraduationScreen,
    CarPurchaseScreen, HousingScreen, FamilyPlanningScreen
)
from moneySmarts.screens.random_event_screens import RandomEventScreen
from moneySmarts.screens.shop_screen import ShopScreen
from moneySmarts.screens.inventory_screen import InventoryScreen
from moneySmarts.screens.home_purchase_screen import HomePurchaseScreen
from moneySmarts.screens.vehicle_purchase_screen import VehiclePurchaseScreen

# GUI Constants (keep only one set, remove duplicates)
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
        pygame.mixer.init()  # Initialize mixer for sound

        # Make window resizable
        screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Money Smartz")

        # Create game instance
        game = Game()
        game.screen = screen  # Pass screen to game if needed

        # Create GUI manager
        gui_manager = GUIManager(game)
        game.gui_manager = gui_manager

        # Set initial screen
        gui_manager.set_screen(TitleScreen(game))

        # Main game loop
        gui_manager.run()
    except GameError as ge:
        logging.error(f"Game error: {ge}")
        print(f"A game error occurred: {ge}")
    except Exception as e:
        logging.error("Uncaught exception:", exc_info=True)
        print("An unexpected error occurred. Please check money_smarts.log for details.")
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
