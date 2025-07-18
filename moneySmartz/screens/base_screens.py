import pygame
import random
import os
from pygame.locals import *
from moneySmartz.constants import *
from moneySmartz.ui import Screen, Button, TextInput
from moneySmartz.sound_manager import SoundManager

class TitleScreen(Screen):
    play_startup_music = True  # Enable music for this screen
    
    def __init__(self, game):
        super().__init__(game)
        
        # Get assets path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(current_dir))
        assets_dir = os.path.join(root_dir, 'assets')
        font_path = os.path.join(assets_dir, PIXEL_FONT)
        title_image_path = os.path.join(assets_dir, TITLE_IMAGE)
        
        # Try to load title image
        self.title_image = None
        try:
            self.title_image = pygame.image.load(title_image_path).convert_alpha()
            # Scale image proportionally
            orig_width, orig_height = self.title_image.get_size()
            scale_factor = min(SCREEN_WIDTH * 0.8 / orig_width, 100 / orig_height)
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            self.title_image = pygame.transform.scale(self.title_image, (new_width, new_height))
        except Exception as e:
            print(f"Could not load title image: {e}")
            self.title_image = None
        
        # Load pixel font or fallback to Arial
        try:
            self.title_font = pygame.font.Font(font_path, FONT_TITLE)
            self.subtitle_font = pygame.font.Font(font_path, FONT_LARGE)
            button_font = font_path
        except Exception as e:
            print(f"Could not load pixel font: {e}")
            self.title_font = pygame.font.SysFont('Arial', FONT_TITLE)
            self.subtitle_font = pygame.font.SysFont('Arial', FONT_LARGE)
            button_font = None

        # Buttons with custom font
        start_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
            200, 50, "Start New Game", 
            font_name=button_font,
            action=self.start_new_game
        )

        quit_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120,
            200, 50, "Quit",
            font_name=button_font,
            action=self.quit_game
        )

        self.buttons = [start_button, quit_button]

        # Background image
        try:
            # Corrected path to assets folder
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up two levels to get to moneySmartz-main
            root_dir = os.path.dirname(os.path.dirname(current_dir))
            assets_dir = os.path.join(root_dir, 'assets')
            image_path = os.path.join(assets_dir, 'title_background.jpg')
            
            # Load and scale background image
            self.bg_image = pygame.image.load(image_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load background image: {e}")
            self.bg_image = None
            # Fallback background color
            self.bg_color = LIGHT_BLUE

        # Coin rain animation setup
        self.coins = []
        self.max_coins = 30  # Maximum number of coins on screen
        self.coin_spawn_rate = 0.5  # Seconds between new coin spawns
        self.coin_spawn_timer = 0
        
        # Logo/Title animation
        self.title_y = -100
        self.title_target_y = SCREEN_HEIGHT // 4
        self.title_speed = 5

        # Subtitle fade-in
        self.subtitle_alpha = 0
        self.subtitle_fade_speed = 2

    def start_new_game(self):
        """Start a new game."""
        from moneySmartz.screens.base_screens import NameInputScreen
        self.game.gui_manager.set_screen(NameInputScreen(self.game))

    def quit_game(self):
        """Quit the game."""
        self.game.gui_manager.running = False

    def update(self):
        """Update the title animation."""
        # Move title down to target position
        if self.title_y < self.title_target_y:
            self.title_y += self.title_speed
            if self.title_y > self.title_target_y:
                self.title_y = self.title_target_y

        # Fade in subtitle after title reaches target
        if self.title_y == self.title_target_y and self.subtitle_alpha < 255:
            self.subtitle_alpha += self.subtitle_fade_speed
            if self.subtitle_alpha > 255:
                self.subtitle_alpha = 255

        # Update coin rain animation
        current_time = pygame.time.get_ticks() / 1000  # Current time in seconds
        
        # Spawn new coins
        if len(self.coins) < self.max_coins and current_time > self.coin_spawn_timer:
            self.coins.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-100, -20),
                'speed': random.uniform(1.5, 3.5),
                'size': random.randint(6, 12),
                'rotation': random.randint(0, 360),
                'rotation_speed': random.uniform(-2, 2)
            })
            self.coin_spawn_timer = current_time + self.coin_spawn_rate
        
        # Update existing coins
        for coin in self.coins[:]:
            coin['y'] += coin['speed']
            coin['rotation'] += coin['rotation_speed']
            
            # Remove coins that have fallen off screen
            if coin['y'] > SCREEN_HEIGHT + 50:
                self.coins.remove(coin)

    def draw(self, surface):
        """Draw the title screen."""
        # Draw background (image or fallback)
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            # Fallback background
            surface.fill(self.bg_color)
            # Draw money-themed background elements
            for i in range(20):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(10, 30)
                alpha = random.randint(20, 100)

                dollar_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(dollar_surface, (0, 200, 0, alpha), (size//2, size//2), size//2)

                font = pygame.font.SysFont('Arial', size)
                text = font.render("$", True, WHITE)
                text_rect = text.get_rect(center=(size//2, size//2))
                dollar_surface.blit(text, text_rect)

                surface.blit(dollar_surface, (x, y))

        # Draw coins (in front of background but behind UI)
        for coin in self.coins:
            # Draw a simple coin (circle with dollar sign)
            pygame.draw.circle(surface, GOLD, (int(coin['x']), int(coin['y'])), coin['size'])
            pygame.draw.circle(surface, DARK_GOLD, (int(coin['x']), int(coin['y'])), coin['size'], 1)
            
            # Draw dollar sign ($) in the center
            font_size = max(6, coin['size'] * 1.2)
            coin_font = pygame.font.SysFont('Arial', int(font_size))
            text = coin_font.render("$", True, DARK_GOLD)
            text_rect = text.get_rect(center=(int(coin['x']), int(coin['y'])))
            surface.blit(text, text_rect)

        # Title
        title_surface = self.title_font.render("MONEY SMARTZ", True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, self.title_y))
        surface.blit(title_surface, title_rect)

        # Subtitle with fade-in
        subtitle_surface = self.subtitle_font.render("Financial Life Simulator", True, (0, 100, 0))
        subtitle_surface.set_alpha(self.subtitle_alpha)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, self.title_y + 60))
        surface.blit(subtitle_surface, subtitle_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
class NameInputScreen(Screen):
    play_startup_music = True  # Enable music for this screen
    
    def __init__(self, game):
        super().__init__(game)
        
        # Get font path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(current_dir))
        assets_dir = os.path.join(root_dir, 'assets')
        font_path = os.path.join(assets_dir, PIXEL_FONT)
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font(font_path, FONT_LARGE)
            input_font = font_path
            button_font = font_path
        except:
            self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
            input_font = None
            button_font = None

        # Text input with custom font
        self.name_input = TextInput(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25,
            300, 50, 
            font_size=FONT_MEDIUM,
            font_name=input_font,
            max_length=20
        )

        # Buttons with custom font
        start_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
            200, 50, "Start Game",
            font_name=button_font,
            action=self.start_game
        )

        back_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120,
            200, 50, "Back",
            font_name=button_font,
            action=self.go_back
        )

        self.buttons = [start_button, back_button]
        
        # Background image
        try:
            # Corrected path to assets folder
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(os.path.dirname(current_dir))
            assets_dir = os.path.join(root_dir, 'assets')
            image_path = os.path.join(assets_dir, 'name_background.png')
            
            # Load and scale background image
            self.bg_image = pygame.image.load(image_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load background image: {e}")
            self.bg_image = None
            # Fallback background color
            self.bg_color = WHITE

    def handle_events(self, events):
        """Handle pygame events."""
        super().handle_events(events)
        self.name_input.update(events)

    def start_game(self):
        """Start the game with the entered name."""
        name = self.name_input.text.strip()
        if name:
            from moneySmartz.models import Player
            self.game.player = Player(name)
            from moneySmartz.screens.base_screens import IntroScreen
            self.game.gui_manager.set_screen(IntroScreen(self.game))

    def go_back(self):
        """Go back to the title screen."""
        from moneySmartz.screens.base_screens import TitleScreen
        self.game.gui_manager.set_screen(TitleScreen(self.game))

    def draw(self, surface):
        """Draw the name input screen."""
        # Draw background (image or fallback)
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            # Fallback background
            surface.fill(self.bg_color)

        # Create a semi-transparent overlay for better readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))  # White with 70% opacity
        surface.blit(overlay, (0, 0))
        
        # Title
        title_surface = self.title_font.render("Enter Your Name", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        surface.blit(title_surface, title_rect)

        # Draw text input
        self.name_input.draw(surface)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class IntroScreen(Screen):
    """
    Introduction screen that explains the game.
    """
    play_startup_music = True  # Enable music for this screen
    
    def __init__(self, game):
        super().__init__(game)
        
        # Get assets path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(current_dir))
        assets_dir = os.path.join(root_dir, 'assets')
        font_path = os.path.join(assets_dir, PIXEL_FONT)
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font(font_path, FONT_LARGE)
            self.text_font = pygame.font.Font(font_path, FONT_MEDIUM)
            button_font = font_path
        except Exception as e:
            print(f"Could not load pixel font: {e}")
            self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
            self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)
            button_font = None

        # Buttons with custom font
        open_account_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 150,
            300, 50,
            "Open Bank Account",
            font_name=button_font,
            action=self.open_bank_account
        )

        skip_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 80,
            300, 50,
            "Skip for Now",
            font_name=button_font,
            action=self.skip_bank_account
        )

        self.buttons = [open_account_button, skip_button]
        
        # Background image
        try:
            # Corrected path to assets folder
            image_path = os.path.join(assets_dir, 'intro_background.png')
            
            # Load and scale background image
            self.bg_image = pygame.image.load(image_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load background image: {e}")
            self.bg_image = None
            # Fallback background color
            self.bg_color = WHITE

    def open_bank_account(self):
        """Open a bank account and continue."""
        from moneySmartz.models import BankAccount
        self.game.player.bank_account = BankAccount()
        self.game.player.bank_account.deposit(50)  # Parents give you $50 to start
        from moneySmartz.screens.base_screens import DebitCardScreen
        self.game.gui_manager.set_screen(DebitCardScreen(self.game))

    def skip_bank_account(self):
        """Skip opening a bank account and continue."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def draw(self, surface):
        """Draw the intro screen."""
        # Draw background (image or fallback)
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            # Fallback background
            surface.fill(self.bg_color)
            
        # Create a semi-transparent overlay for better readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))  # White with 70% opacity
        surface.blit(overlay, (0, 0))

        # Title
        title_surface = self.title_font.render(f"Welcome, {self.game.player.name}!", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        # Introduction text
        intro_lines = [
            "You're a 16-year-old high school student about to embark on your",
            "financial journey through life.",
            "",
            "Your parents suggest that you should open your first bank account.",
            "This will help you manage your money and start building good financial habits.",
            "",
            "Would you like to open a bank account now?"
        ]

        for i, line in enumerate(intro_lines):
            text_surface = self.text_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
            surface.blit(text_surface, text_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class DebitCardScreen(Screen):
    """
    Screen for deciding whether to get a debit card.
    """
    play_startup_music = True  # Enable music for this screen
    
    def __init__(self, game):
        super().__init__(game)
        
        # Get assets path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(current_dir))
        assets_dir = os.path.join(root_dir, 'assets')
        font_path = os.path.join(assets_dir, PIXEL_FONT)
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font(font_path, FONT_LARGE)
            self.text_font = pygame.font.Font(font_path, FONT_MEDIUM)
            self.card_font = pygame.font.Font(font_path, FONT_SMALL)  # Smaller font for card details
            button_font = font_path
        except Exception as e:
            print(f"Could not load pixel font: {e}")
            self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
            self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)
            self.card_font = pygame.font.SysFont('Arial', FONT_SMALL)
            button_font = None
            
        # Card dimensions - stretched vertically
        self.card_width = 270
        self.card_height = 170
        
        # Try to load card image
        self.card_image = None
        try:
            card_image_path = os.path.join(assets_dir, 'card_image.png')
            self.card_image = pygame.image.load(card_image_path).convert_alpha()
            # Stretch to new dimensions
            self.card_image = pygame.transform.scale(self.card_image, (self.card_width, self.card_height))
        except Exception as e:
            print(f"Could not load card image: {e}")
            self.card_image = None

        # Buttons with custom font
        get_card_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 150,
            300, 50,
            "Get Debit Card",
            font_name=button_font,
            action=self.get_debit_card
        )

        skip_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 80,
            300, 50,
            "No Thanks",
            font_name=button_font,
            action=self.skip_debit_card
        )

        self.buttons = [get_card_button, skip_button]
        
        # Background image
        try:
            # Corrected path to assets folder
            image_path = os.path.join(assets_dir, 'debit_background.png')
            
            # Load and scale background image
            self.bg_image = pygame.image.load(image_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load background image: {e}")
            self.bg_image = None
            # Fallback background color
            self.bg_color = WHITE

    def get_debit_card(self):
        """Get a debit card and continue."""
        from moneySmartz.models import Card
        self.game.player.debit_card = Card("Debit")
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def skip_debit_card(self):
        """Skip getting a debit card and continue."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def draw(self, surface):
        """Draw the debit card screen."""
        # Draw background (image or fallback)
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            # Fallback background
            surface.fill(self.bg_color)
            
        # Create a semi-transparent overlay for better readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))  # White with 70% opacity
        surface.blit(overlay, (0, 0))

        # Title
        title_surface = self.title_font.render("Congratulations!", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        # Card position - centered horizontally, at y=150
        card_x = SCREEN_WIDTH // 2 - self.card_width // 2
        card_y = 150
        
        # Draw card image or fallback to drawn rectangle
        if self.card_image:
            surface.blit(self.card_image, (card_x, card_y))
        else:
            # Fallback card drawing
            card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)
            pygame.draw.rect(surface, BLUE, card_rect)
            pygame.draw.rect(surface, BLACK, card_rect, 2)  # Border

        # Calculate text positions with inward padding
        top_padding = 40  # From top of card
        bottom_padding = 40  # From bottom of card
        total_height = self.card_height - top_padding - bottom_padding
        section_height = total_height // 2  # For equidistant spacing
        

        # Player name - positioned in middle
        player_name_y = card_y + top_padding + section_height
        card_name = self.card_font.render(self.game.player.name, True, WHITE)
        card_name_rect = card_name.get_rect(center=(SCREEN_WIDTH // 2, player_name_y))
        surface.blit(card_name, card_name_rect)

        # Card number - positioned inward from bottom
        card_number_y = card_y + self.card_height - bottom_padding
        card_number = self.card_font.render("**** **** **** 1234", True, WHITE)
        card_number_rect = card_number.get_rect(center=(SCREEN_WIDTH // 2, card_number_y))
        surface.blit(card_number, card_number_rect)

        # Explanation text
        text_lines = [
            "You've opened your first checking account!",
            "Your parents deposited $50 to get you started.",
            "",
            "Would you like a debit card with your account?",
            "A debit card allows you to make purchases and withdraw cash",
            "directly from your checking account."
        ]

        for i, line in enumerate(text_lines):
            text_surface = self.text_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 370 + i * 30))
            surface.blit(text_surface, text_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class EndGameScreen(Screen):
    """
    Screen shown at the end of the game.
    """
    play_startup_music = False  # Disable music for this screen    

    def __init__(self, game, reason):
        super().__init__(game)
        self.reason = reason

        # Fonts
        self.title_font = pygame.font.SysFont('Arial', FONT_TITLE)
        self.subtitle_font = pygame.font.SysFont('Arial', FONT_LARGE)
        self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)

        # Calculate final stats
        self.cash = self.game.player.cash
        self.bank_balance = self.game.player.bank_account.balance if self.game.player.bank_account else 0
        self.credit_card_debt = self.game.player.credit_card.balance if self.game.player.credit_card else 0

        self.loan_debt = 0
        for loan in self.game.player.loans:
            self.loan_debt += loan.current_balance

        self.asset_value = 0
        for asset in self.game.player.assets:
            self.asset_value += asset.current_value

        self.net_worth = self.cash + self.bank_balance - self.credit_card_debt - self.loan_debt + self.asset_value

        # Financial rating
        if self.net_worth >= 1000000:
            self.rating = "Financial Wizard"
            self.rating_color = GREEN
        elif self.net_worth >= 500000:
            self.rating = "Financially Secure"
            self.rating_color = LIGHT_GREEN
        elif self.net_worth >= 100000:
            self.rating = "Financially Stable"
            self.rating_color = BLUE
        elif self.net_worth >= 0:
            self.rating = "Breaking Even"
            self.rating_color = YELLOW
        else:
            self.rating = "In Debt"
            self.rating_color = RED

        # Buttons
        quit_button = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT - 80,
            200, 50,
            "Quit Game",
            action=self.quit_game
        )

        self.buttons = [quit_button]

    def quit_game(self):
        """Quit the game."""
        self.game.gui_manager.running = False

    def draw_text(self, surface, text, x, y, center=False, is_title=False):
        """Helper method to draw text."""
        font = self.title_font if is_title else self.text_font
        text_surface = font.render(text, True, BLACK)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        surface.blit(text_surface, text_rect)

    def draw(self, surface):
        """Draw the end game screen."""
        # Background
        surface.fill(WHITE)

        # Title
        if self.reason == "retirement":
            title = "CONGRATULATIONS ON YOUR RETIREMENT!"
            subtitle = f"After {self.game.current_year} years, you've reached retirement age!"
        else:
            title = "GAME OVER"
            subtitle = f"Your financial journey has ended after {self.game.current_year} years."

        title_surface = self.title_font.render(title, True, BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 60))
        surface.blit(title_surface, title_rect)

        subtitle_surface = self.subtitle_font.render(subtitle, True, BLACK)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 110))
        surface.blit(subtitle_surface, subtitle_rect)

        # Financial summary
        summary_title = self.subtitle_font.render("FINAL FINANCIAL SUMMARY", True, BLACK)
        summary_rect = summary_title.get_rect(center=(SCREEN_WIDTH // 2, 170))
        surface.blit(summary_title, summary_rect)

        summary_items = [
            f"Cash: ${self.cash:.2f}",
            f"Bank Balance: ${self.bank_balance:.2f}",
            f"Credit Card Debt: ${self.credit_card_debt:.2f}",
            f"Loan Debt: ${self.loan_debt:.2f}",
            f"Asset Value: ${self.asset_value:.2f}",
            f"Net Worth: ${self.net_worth:.2f}",
            f"Credit Score: {self.game.player.credit_score}"
        ]

        for i, item in enumerate(summary_items):
            text_surface = self.text_font.render(item, True, BLACK)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 210 + i * 30))
            surface.blit(text_surface, text_rect)

        # Family summary
        if self.game.player.family:
            family_title = self.subtitle_font.render("FAMILY", True, BLACK)
            family_rect = family_title.get_rect(center=(SCREEN_WIDTH // 2, 430))
            surface.blit(family_title, family_rect)

            y_pos = 470
            for member in self.game.player.family:
                if member["relation"] == "Spouse":
                    text = f"Spouse: Age {member['age'] + self.game.current_year}"
                else:
                    text = f"{member['relation']}: {member['name']}, Age {member['age'] + self.game.current_year}"

                text_surface = self.text_font.render(text, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                surface.blit(text_surface, text_rect)
                y_pos += 30

        # Financial rating
        rating_title = self.subtitle_font.render("Financial Rating:", True, BLACK)
        rating_rect = rating_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 180))
        surface.blit(rating_title, rating_rect)

        rating_text = self.title_font.render(self.rating, True, self.rating_color)
        rating_text_rect = rating_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 140))
        surface.blit(rating_text, rating_text_rect)

        # Thank you message
        thanks_text = self.text_font.render("Thank you for playing MONEY SMARTZ!", True, BLACK)
        thanks_rect = thanks_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110))
        surface.blit(thanks_text, thanks_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

