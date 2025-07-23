import pygame
from moneySmartz.constants import *
from moneySmartz.ui import Screen, Button

SHOP_ITEMS = [
    {"name": "Groceries", "price": 50, "desc": "Weekly groceries for your family."},
    {"name": "Clothes", "price": 100, "desc": "A new set of clothes."},
    {"name": "Smartphone", "price": 600, "desc": "A modern smartphone.", "recurring": {"name": "Phone Plan", "amount": 30, "source": "bank_or_credit"}},
    {"name": "TV", "price": 400, "desc": "A 50-inch smart TV.", "recurring": {"name": "Streaming Service", "amount": 15, "source": "bank_or_credit"}},
    {"name": "Laptop", "price": 900, "desc": "A new laptop for work or school.", "recurring": {"name": "Software Subscription", "amount": 10, "source": "bank_or_credit"}},
    {"name": "Gift", "price": 30, "desc": "A gift for a friend or family member."},
    {"name": "Home", "price": 5000, "desc": "A place to call your own. Unlocks a new chapter!"},
    {"name": "Vehicle", "price": 1200, "desc": "Buy a new or used vehicle!"},
]

class ShopScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.selected_item = None
        self.message = ""
        self.show_payment_popup = False
        self.create_buttons()
        self.create_payment_buttons()

    def create_buttons(self):
        self.buttons = []
        y = 120
        for idx, item in enumerate(SHOP_ITEMS):
            btn = Button(60, y, 300, 50, f"{item['name']} - ${item['price']}", action=lambda i=idx: self.select_item(i))
            self.buttons.append(btn)
            y += 60
        # Add main Back button (not popup)
        self.main_back_btn = Button(700, 40, 120, 40, "Back", action=self.go_back)

    def create_payment_buttons(self):
        # Payment and back buttons for popup
        popup_x = 300
        popup_y = 250
        self.pay_cash_btn = Button(popup_x + 40, popup_y + 60, 180, 40, "Pay Cash", action=self.pay_cash)
        self.pay_bank_btn = Button(popup_x + 40, popup_y + 110, 180, 40, "Pay Bank", action=self.pay_bank)
        self.pay_credit_btn = Button(popup_x + 40, popup_y + 160, 180, 40, "Pay Credit", action=self.pay_credit)
        self.back_btn = Button(popup_x + 80, popup_y + 220, 120, 40, "Back", action=self.close_popup)

    def select_item(self, idx):
        self.selected_item = SHOP_ITEMS[idx]
        if self.selected_item['name'] == "Home":
            from moneySmartz.screens.home_purchase_screen import HomePurchaseScreen
            self.game.gui_manager.set_screen(HomePurchaseScreen(self.game))
            return
        if self.selected_item['name'] == "Vehicle":
            from moneySmartz.screens.vehicle_purchase_screen import VehiclePurchaseScreen
            self.game.gui_manager.set_screen(VehiclePurchaseScreen(self.game))
            return
        self.message = f"Selected: {self.selected_item['name']}"
        self.show_payment_popup = True

    def close_popup(self):
        self.show_payment_popup = False
        self.selected_item = None
        self.message = ""

    def pay_cash(self):
        if not self.selected_item:
            self.message = "Select an item first."
            return
        # Special logic for buying a home
        if self.selected_item['name'] == "Home":
            if self.game.player.cash >= self.selected_item['price']:
                self.game.player.cash -= self.selected_item['price']
                self.game.player.inventory.append(self.selected_item['name'])
                self.game.player.has_home = True
                self.message = "Congratulations! You bought a home and unlocked a new chapter!"
                # Optionally, trigger a new screen or event here
            else:
                self.message = "Not enough cash to buy a home."
            return
        if self.game.player.cash >= self.selected_item['price']:
            self.game.player.cash -= self.selected_item['price']
            self.game.player.inventory.append(self.selected_item['name'])
            # Add recurring bill if item has one
            if 'recurring' in self.selected_item:
                self.game.player.recurring_bills.append(self.selected_item['recurring'])
            self.message = f"Bought {self.selected_item['name']} with cash!"
        else:
            self.message = "Not enough cash."

    def pay_bank(self):
        if not self.selected_item:
            self.message = "Select an item first."
            return
        # Special logic for buying a home
        if self.selected_item['name'] == "Home":
            acct = self.game.player.bank_account
            if acct and acct.balance >= self.selected_item['price']:
                acct.withdraw(self.selected_item['price'])
                self.game.player.inventory.append(self.selected_item['name'])
                self.game.player.has_home = True
                self.message = "Congratulations! You bought a home and unlocked a new chapter!"
                # Optionally, trigger a new screen or event here
            else:
                self.message = "Not enough in bank account to buy a home."
            return
        acct = self.game.player.bank_account
        if acct and acct.balance >= self.selected_item['price']:
            acct.withdraw(self.selected_item['price'])
            self.game.player.inventory.append(self.selected_item['name'])
            if 'recurring' in self.selected_item:
                self.game.player.recurring_bills.append(self.selected_item['recurring'])
            self.message = f"Bought {self.selected_item['name']} from bank!"
        else:
            self.message = "Not enough in bank account."

    def pay_credit(self):
        if not self.selected_item:
            self.message = "Select an item first."
            return
        # Special logic for buying a home
        if self.selected_item['name'] == "Home":
            card = self.game.player.credit_card
            if card and card.charge(self.selected_item['price']):
                self.game.player.inventory.append(self.selected_item['name'])
                self.game.player.has_home = True
                self.message = "Congratulations! You bought a home and unlocked a new chapter!"
                # Optionally, trigger a new screen or event here
            else:
                self.message = "Not enough credit or no card to buy a home."
            return
        card = self.game.player.credit_card
        if card and card.charge(self.selected_item['price']):
            self.game.player.inventory.append(self.selected_item['name'])
            if 'recurring' in self.selected_item:
                self.game.player.recurring_bills.append(self.selected_item['recurring'])
            self.message = f"Bought {self.selected_item['name']} on credit!"
        else:
            self.message = "Not enough credit or no card."

    def go_back(self):
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True
        if self.show_payment_popup:
            # Only handle payment popup buttons
            for btn in [self.pay_cash_btn, self.pay_bank_btn, self.pay_credit_btn, self.back_btn]:
                action = btn.update(mouse_pos, mouse_click)
                if callable(action):
                    action()
                    return
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                    self.close_popup()
        else:
            # Handle item selection buttons
            for btn in self.buttons:
                action = btn.update(mouse_pos, mouse_click)
                if callable(action):
                    action()
                    return
            # Handle main Back button
            action = self.main_back_btn.update(mouse_pos, mouse_click)
            if callable(action):
                action()
                return
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                    self.go_back()

    def draw(self, surface):
        surface.fill(WHITE)
        font = pygame.font.SysFont('Arial', FONT_LARGE)
        title = font.render("Shop", True, BLUE)
        surface.blit(title, (60, 40))
        font_small = pygame.font.SysFont('Arial', FONT_MEDIUM)
        y = 120
        for idx, item in enumerate(SHOP_ITEMS):
            desc = font_small.render(item['desc'], True, BLACK)
            surface.blit(desc, (380, y+10))
            y += 60
        for btn in self.buttons:
            btn.draw(surface)
        # Draw main Back button (not popup)
        self.main_back_btn.draw(surface)
        msg_font = pygame.font.SysFont('Arial', FONT_MEDIUM)
        msg = msg_font.render(self.message, True, RED if "Not" in self.message else GREEN)
        surface.blit(msg, (60, 680))
        if self.selected_item:
            sel_font = pygame.font.SysFont('Arial', FONT_MEDIUM)
            sel_msg = sel_font.render(f"Selected: {self.selected_item['name']}", True, BLACK)
            surface.blit(sel_msg, (60, 620))
        # Draw payment popup if needed
        if self.show_payment_popup and self.selected_item:
            popup_x = 300
            popup_y = 250
            pygame.draw.rect(surface, LIGHT_GRAY, (popup_x, popup_y, 260, 300))
            pygame.draw.rect(surface, BLACK, (popup_x, popup_y, 260, 300), 3)
            popup_font = pygame.font.SysFont('Arial', FONT_LARGE)
            popup_title = popup_font.render("Choose Payment", True, BLUE)
            surface.blit(popup_title, (popup_x + 30, popup_y + 10))
            for btn in [self.pay_cash_btn, self.pay_bank_btn, self.pay_credit_btn, self.back_btn]:
                btn.draw(surface)
