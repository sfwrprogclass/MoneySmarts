import pygame
import os
from moneySmarts.constants import *
from moneySmarts.ui import Screen, Button

HOME_OPTIONS = [
    {"name": "Starter Home", "price": 3000, "desc": "A cozy starter home. Affordable and simple."},
    {"name": "Family House", "price": 7000, "desc": "A spacious house for a growing family."},
    {"name": "Luxury Villa", "price": 20000, "desc": "A luxurious villa with all amenities."},
]

class HomePurchaseScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.selected_home = None
        self.message = ""
        self.show_popup = False
        self.popup_text = ""
        self.create_buttons()
        # Load home images
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
        self.home_images = [
            pygame.image.load(os.path.join(assets_dir, 'home_starter.png')).convert_alpha(),
            pygame.image.load(os.path.join(assets_dir, 'home_family.png')).convert_alpha(),
            pygame.image.load(os.path.join(assets_dir, 'home_luxury.png')).convert_alpha()
        ]

    def create_buttons(self):
        self.buttons = []
        y = 150
        for idx, home in enumerate(HOME_OPTIONS):
            btn = Button(80, y, 400, 60, f"{home['name']} - ${home['price']}", action=lambda i=idx: self.select_home(i))
            self.buttons.append(btn)
            y += 90
        self.buy_btn = Button(600, 200, 180, 50, "Buy Home", action=self.buy_home)
        self.back_btn = Button(600, 350, 120, 40, "Back", action=self.go_back)

    def select_home(self, idx):
        self.selected_home = HOME_OPTIONS[idx]
        self.message = f"Selected: {self.selected_home['name']}"

    def buy_home(self):
        if not self.selected_home:
            self.message = "Select a home first."
            return
        price = self.selected_home['price']
        cash_before = self.game.player.cash
        if cash_before >= price:
            self.game.player.cash -= price
            cash_after = self.game.player.cash
            self.game.player.home = self.selected_home['name']
            self.show_popup = True
            self.popup_text = (
                f"Purchase Confirmation:\n"
                f"Before: ${cash_before:.2f}\n"
                f"Purchase: -${price:.2f}\n"
                f"After: ${cash_after:.2f}\n"
                f"Congratulations! You bought the {self.selected_home['name']}!"
            )
            self.selected_home = None
        else:
            self.message = "Not enough cash."

    def go_back(self):
        from moneySmarts.screens.shop_screen import ShopScreen
        self.selected_home = None
        self.message = ""
        self.game.gui_manager.set_screen(ShopScreen(self.game))

    def draw(self, surface):
        surface.fill((220, 240, 255))  # Light blue background for home screen
        font = pygame.font.SysFont('Arial', FONT_LARGE)
        title = font.render("Choose Your Home", True, BLUE)
        surface.blit(title, (80, 60))
        font_small = pygame.font.SysFont('Arial', FONT_MEDIUM)
        y = 150
        for idx, home in enumerate(HOME_OPTIONS):
            # Draw home image
            surface.blit(self.home_images[idx], (30, y))
            desc = font_small.render(home['desc'], True, BLACK)
            surface.blit(desc, (500, y+20))
            y += 90
        for btn in self.buttons:
            btn.draw(surface)
        self.buy_btn.draw(surface)
        self.back_btn.draw(surface)
        msg_font = pygame.font.SysFont('Arial', FONT_MEDIUM)
        # Show message as popup if not enough cash
        if self.message == "Not enough cash.":
            popup_rect = pygame.Rect(250, 250, 520, 160)
            pygame.draw.rect(surface, (255, 220, 220), popup_rect)
            pygame.draw.rect(surface, RED, popup_rect, 3)
            msg = msg_font.render(self.message, True, RED)
            surface.blit(msg, (popup_rect.x + 40, popup_rect.y + 40))
            # Draw OK button centered at bottom of popup
            ok_btn_width, ok_btn_height = 140, 40
            ok_btn_x = popup_rect.x + (popup_rect.width - ok_btn_width) // 2
            ok_btn_y = popup_rect.y + popup_rect.height - ok_btn_height - 20
            ok_btn_rect = pygame.Rect(ok_btn_x, ok_btn_y, ok_btn_width, ok_btn_height)
            pygame.draw.rect(surface, GREEN, ok_btn_rect)
            ok_text = msg_font.render("OK", True, WHITE)
            surface.blit(ok_text, (ok_btn_rect.x + 45, ok_btn_rect.y + 5))
            self.ok_btn_rect = ok_btn_rect
            return  # Prevent drawing other popups/buttons
        else:
            msg = msg_font.render(self.message, True, RED if "Not" in self.message else GREEN)
            surface.blit(msg, (80, 420))
        # Draw popup if needed
        if self.show_popup:
            popup_rect = pygame.Rect(200, 180, 500, 280)
            pygame.draw.rect(surface, (255, 255, 220), popup_rect)
            pygame.draw.rect(surface, BLUE, popup_rect, 3)
            lines = self.popup_text.split('\n')
            for i, line in enumerate(lines):
                line_surf = msg_font.render(line, True, BLACK)
                surface.blit(line_surf, (popup_rect.x + 30, popup_rect.y + 30 + i * 35))
            # Draw OK button centered at bottom of popup
            ok_btn_width, ok_btn_height = 140, 40
            ok_btn_x = popup_rect.x + (popup_rect.width - ok_btn_width) // 2
            ok_btn_y = popup_rect.y + popup_rect.height - ok_btn_height - 20
            ok_btn_rect = pygame.Rect(ok_btn_x, ok_btn_y, ok_btn_width, ok_btn_height)
            pygame.draw.rect(surface, GREEN, ok_btn_rect)
            ok_text = msg_font.render("OK", True, WHITE)
            surface.blit(ok_text, (ok_btn_rect.x + 45, ok_btn_rect.y + 5))
            self.ok_btn_rect = ok_btn_rect
        else:
            self.ok_btn_rect = None

    def handle_event(self, event):
        # Handle OK button for both popups
        if (self.show_popup or self.message == "Not enough cash.") and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.ok_btn_rect and self.ok_btn_rect.collidepoint(mouse_pos):
                self.show_popup = False
                self.popup_text = ""
                self.message = ""
                return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                if btn.rect.collidepoint(mouse_pos):
                    if btn.action:
                        btn.action()
                        return
            if self.buy_btn.rect.collidepoint(mouse_pos):
                if self.buy_btn.action:
                    self.buy_btn.action()
                    return
            if self.back_btn.rect.collidepoint(mouse_pos):
                if self.back_btn.action:
                    self.back_btn.action()
                    return
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                self.go_back()
