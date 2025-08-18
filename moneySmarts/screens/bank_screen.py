import pygame
from moneySmarts.constants import *
from moneySmarts.screens import GameScreen
from moneySmarts.ui import Screen, Button
from moneySmarts.screens.financial_screens import DepositScreen, WithdrawScreen, BankAccountScreen, SavingsDetailsScreen, BankDetailsScreen
import os

BANKING_MENU_BUTTONS = [
    {"Deposit", DepositScreen},
    {"Withdraw", WithdrawScreen},
    {"View Balance", BankAccountScreen},
    {"View Savings", SavingsDetailsScreen},
    {"Open Account", BankDetailsScreen},
    {"Back", GameScreen}
]

class BankScreen(Screen):
    """
    Main bank screen with banking options and buttons.
    """
    play_startup_music = False
    def __init__(self, game):
        super().__init__(game)
        # Use a larger, bold font for the title and balances
        font_path = os.path.join(ASSETS_DIR, 'fonts', 'pixelated_font.ttf') if os.path.exists(os.path.join(ASSETS_DIR, 'fonts', 'pixelated_font.ttf')) else None
        self.title_font = pygame.font.Font(font_path, 64) if font_path else pygame.font.SysFont('Arial', 64, bold=True)
        self.balance_font = pygame.font.Font(font_path, 40) if font_path else pygame.font.SysFont('Arial', 40, bold=True)
        self.text_font = pygame.font.Font(font_path, 32) if font_path else pygame.font.SysFont('Arial', 32)
        self.buttons = []
        self.create_buttons()
        self.status_message = None
        self.status_color = WHITE
        self.prev_mouse_pressed = False

    def create_buttons(self):
        win_width = SCREEN_WIDTH
        win_height = SCREEN_HEIGHT
        button_specs = [
            ("Deposit", self.go_to_deposit),
            ("Withdraw", self.go_to_withdraw),
            ("Deposit to Savings", self.go_to_deposit_savings),
            ("View Balance", self.go_to_view_balance),
            ("View Savings", self.go_to_view_savings),
            ("Open Account", self.go_to_open_account),
            ("Back", self.go_back)
        ]
        start_y = 120  # Start near the top
        self.buttons = []
        for i, (label, callback) in enumerate(button_specs):
            print(f"[DEBUG] Creating button '{label}' with callback {callback}")
            btn = Button(
                SCREEN_WIDTH - 260,  # Right side
                start_y + i * 60,
                200,
                50,
                label,
                callback
            )
            self.buttons.append(btn)

    def go_to_deposit(self):
        print("[DEBUG] go_to_deposit called")
        self.game.gui_manager.set_screen(DepositScreen(self.game))

    def go_to_withdraw(self):
        print("[DEBUG] go_to_withdraw called")
        self.game.gui_manager.set_screen(WithdrawScreen(self.game))

    def go_to_deposit_savings(self):
        print("[DEBUG] go_to_deposit_savings called")
        self.game.gui_manager.set_screen(DepositToSavingsScreen(self.game))

    def go_to_view_balance(self):
        print("[DEBUG] go_to_view_balance called")
        self.game.gui_manager.set_screen(BankDetailsScreen(self.game))

    def go_to_view_savings(self):
        print("[DEBUG] go_to_view_savings called")
        self.game.gui_manager.set_screen(SavingsDetailsScreen(self.game))

    def go_to_open_account(self):
        print("[DEBUG] go_to_open_account called")
        self.game.gui_manager.set_screen(BankAccountScreen(self.game))

    def go_back(self):
        print("[DEBUG] go_back called")
        from moneySmarts.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def handle_events(self, events):
        super().handle_events(events)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(f"[DEBUG] Mouse button down at {mouse_pos}")
                mouse_click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("[DEBUG] ESC pressed, going back.")
                self.go_back()
        # Only trigger click for the frame the button is pressed
        if mouse_click:
            for button in self.buttons:
                print(f"[DEBUG] Checking button '{button.text}' at {button.rect}")
                action = button.update(mouse_pos, mouse_click)
                if callable(action):
                    print(f"[DEBUG] Button '{button.text}' clicked, calling action.")
                    action()  # Call the button's callback
        else:
            for button in self.buttons:
                button.update(mouse_pos, False)
    def draw(self, surface):
        # Draw the background image
        bg_image = pygame.image.load(os.path.join(ASSETS_DIR, 'images', 'Bank_Screen.png'))
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(bg_image, (0, 0))
        # Title - top left
        title_surface = self.title_font.render("Bank", True, WHITE)
        title_rect = title_surface.get_rect(topleft=(40, 40))
        surface.blit(title_surface, title_rect)
        player = self.game.player
        # Balances - top left, below title
        info_lines = [
            f"Cash: ${player.cash:.2f}",
            f"Checking: ${player.bank_account.balance:.2f}" if hasattr(player, 'bank_account') and player.bank_account else "Checking: $0.00",
            f"Savings: ${player.savings_account.balance:.2f}" if hasattr(player, 'savings_account') and player.savings_account else "Savings: $0.00"
        ]
        for i, line in enumerate(info_lines):
            text_surface = self.balance_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(topleft=(40, 120 + i * 40))
            surface.blit(text_surface, text_rect)
        for button in self.buttons:
            button.draw(surface)
        # Status message - large and white, below balances
        if self.status_message:
            status_surface = self.title_font.render(self.status_message, True, WHITE)
            status_rect = status_surface.get_rect(topleft=(40, 250))
            surface.blit(status_surface, status_rect)

class DepositToSavingsScreen(Screen):
    """
    Screen for depositing money into savings account and showing interest.
    """
    def __init__(self, game):
        super().__init__(game)
        font_path = os.path.join(ASSETS_DIR, 'fonts', 'pixelated_font.ttf') if os.path.exists(os.path.join(ASSETS_DIR, 'fonts', 'pixelated_font.ttf')) else None
        self.title_font = pygame.font.Font(font_path, 48) if font_path else pygame.font.SysFont('Arial', 48, bold=True)
        self.text_font = pygame.font.Font(font_path, 32) if font_path else pygame.font.SysFont('Arial', 32)
        self.input_active = False
        self.input_text = ""
        self.status_message = None
        self.status_color = WHITE
        self.interest_rate = 0.02  # 2% interest for demonstration

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.gui_manager.set_screen(BankScreen(self.game))
                elif event.key == pygame.K_RETURN:
                    self.deposit_to_savings()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.unicode.isdigit() or (event.unicode == '.' and '.' not in self.input_text):
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input_active = True

    def deposit_to_savings(self):
        player = self.game.player
        try:
            amount = float(self.input_text)
            if amount > 0 and amount <= player.cash:
                player.cash -= amount
                if not hasattr(player, 'savings_account') or player.savings_account is None:
                    player.savings_account = type('SavingsAccount', (), {'balance': 0.0})()
                player.savings_account.balance += amount
                # Apply interest
                interest = amount * self.interest_rate
                player.savings_account.balance += interest
                self.status_message = f"Deposited ${amount:.2f} (+${interest:.2f} interest)"
            else:
                self.status_message = "Invalid amount."
        except Exception:
            self.status_message = "Invalid input."
        self.input_text = ""

    def draw(self, surface):
        bg_image = pygame.image.load(os.path.join(ASSETS_DIR, 'images', 'Bank_Screen.png'))
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(bg_image, (0, 0))
        title_surface = self.title_font.render("Deposit to Savings", True, WHITE)
        surface.blit(title_surface, (40, 40))
        prompt_surface = self.text_font.render("Enter amount to deposit:", True, WHITE)
        surface.blit(prompt_surface, (40, 120))
        input_box = pygame.Rect(40, 170, 200, 50)
        pygame.draw.rect(surface, (0, 0, 0), input_box)
        input_surface = self.text_font.render(self.input_text, True, WHITE)
        surface.blit(input_surface, (input_box.x + 10, input_box.y + 10))
        if self.status_message:
            status_surface = self.text_font.render(self.status_message, True, WHITE)
            surface.blit(status_surface, (40, 240))
        # Show current savings balance
        player = self.game.player
        savings_balance = getattr(getattr(player, 'savings_account', None), 'balance', 0.0)
        balance_surface = self.text_font.render(f"Savings Balance: ${savings_balance:.2f}", True, WHITE)
        surface.blit(balance_surface, (40, 320))
