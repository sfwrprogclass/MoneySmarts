import os
import pygame
from moneySmarts.constants import *
from moneySmarts.ui import Screen, Button

VEHICLE_OPTIONS = [
    {"name": "Used Car", "price": 1200, "desc": "Reliable but basic transportation."},
    {"name": "Sedan", "price": 6000, "desc": "A comfortable family sedan."},
    {"name": "SUV", "price": 15000, "desc": "Spacious and powerful SUV."},
]

class VehiclePurchaseScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.selected_vehicle = None
        self.message = ""
        self.show_popup = False
        self.popup_text = ""
        self.create_buttons()
        # Load vehicle images
        self.vehicle_images = [
            pygame.image.load(os.path.join(ASSETS_DIR, 'vehicle_used_car.png')).convert_alpha(),
            pygame.image.load(os.path.join(ASSETS_DIR, 'vehicle_sedan.png')).convert_alpha(),
            pygame.image.load(os.path.join(ASSETS_DIR, 'vehicle_suv.png')).convert_alpha()
        ]

    def create_buttons(self):
        self.buttons = []
        y = 150
        for idx, vehicle in enumerate(VEHICLE_OPTIONS):
            btn = Button(80, y, 400, 60, f"{vehicle['name']} - ${vehicle['price']}", action=lambda i=idx: self.select_vehicle(i))
            self.buttons.append(btn)
            y += 90
        self.buy_cash_btn = Button(600, 150, 180, 40, "Buy Cash", action=self.buy_cash)
        self.buy_bank_btn = Button(600, 210, 180, 40, "Buy Bank", action=self.buy_bank)
        self.buy_credit_btn = Button(600, 270, 180, 40, "Buy Credit", action=self.buy_credit)
        self.finance_btn = Button(600, 330, 180, 40, "Finance", action=self.finance_vehicle)
        self.back_btn = Button(600, 400, 120, 40, "Back", action=self.go_back)

    def select_vehicle(self, idx):
        self.selected_vehicle = VEHICLE_OPTIONS[idx]
        self.message = f"Selected: {self.selected_vehicle['name']}"

    def buy_cash(self):
        if not self.selected_vehicle:
            self.message = "Select a vehicle first."
            return
        price = self.selected_vehicle['price']
        cash_before = self.game.player.cash
        if cash_before >= price:
            self.game.player.cash -= price
            cash_after = self.game.player.cash
            self.game.player.vehicle = self.selected_vehicle['name']
            from moneySmarts.models import Asset
            self.game.player.assets.append(Asset("Car", self.selected_vehicle['name'], price))
            self.show_popup = True
            self.popup_text = (
                f"Purchase Confirmation:\n"
                f"Before: ${cash_before:.2f}\n"
                f"Purchase: -${price:.2f}\n"
                f"After: ${cash_after:.2f}\n"
                f"You bought the {self.selected_vehicle['name']} with cash!"
            )
            self.selected_vehicle = None
        else:
            self.message = "Not enough cash."

    def buy_bank(self):
        if not self.selected_vehicle:
            self.message = "Select a vehicle first."
            return
        acct = self.game.player.bank_account
        price = self.selected_vehicle['price']
        bank_before = acct.balance if acct else 0
        if acct and acct.balance >= price:
            acct.withdraw(price)
            bank_after = acct.balance
            self.game.player.vehicle = self.selected_vehicle['name']
            from moneySmarts.models import Asset
            self.game.player.assets.append(Asset("Car", self.selected_vehicle['name'], price))
            self.show_popup = True
            self.popup_text = (
                f"Purchase Confirmation:\n"
                f"Bank Before: ${bank_before:.2f}\n"
                f"Purchase: -${price:.2f}\n"
                f"Bank After: ${bank_after:.2f}\n"
                f"You bought the {self.selected_vehicle['name']} from bank!"
            )
            self.selected_vehicle = None
        else:
            self.message = "Not enough in bank account."

    def buy_credit(self):
        if not self.selected_vehicle:
            self.message = "Select a vehicle first."
            return
        card = self.game.player.credit_card
        price = self.selected_vehicle['price']
        credit_before = card.balance if card else 0
        if card and card.charge(price):
            credit_after = card.balance
            self.game.player.vehicle = self.selected_vehicle['name']
            from moneySmarts.models import Asset
            self.game.player.assets.append(Asset("Car", self.selected_vehicle['name'], price))
            self.show_popup = True
            self.popup_text = (
                f"Purchase Confirmation:\n"
                f"Credit Before: ${credit_before:.2f}\n"
                f"Purchase: -${price:.2f}\n"
                f"Credit After: ${credit_after:.2f}\n"
                f"You bought the {self.selected_vehicle['name']} on credit!"
            )
            self.selected_vehicle = None
        else:
            self.message = "Not enough credit or no card."

    def finance_vehicle(self):
        if not self.selected_vehicle:
            self.message = "Select a vehicle first."
            return
        price = self.selected_vehicle['price']
        if hasattr(self.game.player, 'credit_score') and self.game.player.credit_score >= 650:
            self.game.player.loans.append({
                'type': 'vehicle',
                'amount': price,
                'name': self.selected_vehicle['name']
            })
            self.game.player.vehicle = self.selected_vehicle['name']
            from moneySmarts.models import Asset
            self.game.player.assets.append(Asset("Car", self.selected_vehicle['name'], price))
            self.show_popup = True
            self.popup_text = (
                f"Purchase Confirmation:\n"
                f"Financed Amount: ${price:.2f}\n"
                f"Financed {self.selected_vehicle['name']}! Loan added."
            )
            self.selected_vehicle = None
        else:
            self.message = "Credit score too low for financing."

    def go_back(self):
        from moneySmarts.screens.shop_screen import ShopScreen
        self.selected_vehicle = None
        self.message = ""
        self.game.gui_manager.set_screen(ShopScreen(self.game))

    def draw(self, surface):
        surface.fill((240, 240, 220))  # Light tan background for vehicle screen
        font = pygame.font.SysFont('Arial', FONT_LARGE)
        title = font.render("Choose Your Vehicle", True, BLUE)
        surface.blit(title, (80, 60))
        font_small = pygame.font.SysFont('Arial', FONT_MEDIUM)
        y = 150
        for idx, vehicle in enumerate(VEHICLE_OPTIONS):
            # Draw vehicle image
            surface.blit(self.vehicle_images[idx], (30, y))
            desc = font_small.render(vehicle['desc'], True, BLACK)
            surface.blit(desc, (500, y+20))
            y += 90
        for btn in self.buttons:
            btn.draw(surface)
        self.buy_cash_btn.draw(surface)
        self.buy_bank_btn.draw(surface)
        self.buy_credit_btn.draw(surface)
        self.finance_btn.draw(surface)
        self.back_btn.draw(surface)
        msg_font = pygame.font.SysFont('Arial', FONT_MEDIUM)
        msg = msg_font.render(self.message, True, RED if "Not" in self.message or "low" in self.message else GREEN)
        surface.blit(msg, (80, 480))
        # Draw popup if needed
        if self.show_popup:
            popup_rect = pygame.Rect(200, 180, 500, 220)
            pygame.draw.rect(surface, (255, 255, 220), popup_rect)
            pygame.draw.rect(surface, BLUE, popup_rect, 3)
            lines = self.popup_text.split('\n')
            for i, line in enumerate(lines):
                line_surf = msg_font.render(line, True, BLACK)
                surface.blit(line_surf, (popup_rect.x + 30, popup_rect.y + 30 + i * 35))
            # Draw OK button
            ok_btn_rect = pygame.Rect(popup_rect.x + 180, popup_rect.y + 160, 140, 40)
            pygame.draw.rect(surface, GREEN, ok_btn_rect)
            ok_text = msg_font.render("OK", True, WHITE)
            surface.blit(ok_text, (ok_btn_rect.x + 45, ok_btn_rect.y + 5))
            self.ok_btn_rect = ok_btn_rect
        else:
            self.ok_btn_rect = None

    def handle_event(self, event):
        if self.show_popup and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.ok_btn_rect and self.ok_btn_rect.collidepoint(mouse_pos):
                self.show_popup = False
                self.popup_text = ""
                return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                if btn.rect.collidepoint(mouse_pos):
                    if btn.action:
                        btn.action()
                        return
            for btn in [self.buy_cash_btn, self.buy_bank_btn, self.buy_credit_btn, self.finance_btn, self.back_btn]:
                if btn.rect.collidepoint(mouse_pos):
                    if btn.action:
                        btn.action()
                        return
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                self.go_back()
