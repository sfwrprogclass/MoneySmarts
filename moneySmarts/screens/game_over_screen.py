import pygame
from moneySmarts.constants import *
from moneySmarts.ui import Screen, Button

class GameOverScreen(Screen):
    def __init__(self, game, reason=None):
        super().__init__(game)
        self.reason = reason or "Game Over! You can no longer continue."
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        restart_btn = Button(
            SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 40, 100, 50, "Restart", action=self.restart_game
        )
        quit_btn = Button(
            SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 40, 100, 50, "Quit", action=self.quit_game
        )
        self.buttons.extend([restart_btn, quit_btn])

    def restart_game(self):
        self.game.restart()

    @staticmethod
    def quit_game():
        pygame.quit()
        exit()

    def draw(self, surface):
        surface.fill((30, 30, 30))
        font = pygame.font.Font(None, 48)
        text = font.render(self.reason, True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        surface.blit(text, rect)
        for btn in self.buttons:
            btn.draw(surface)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

