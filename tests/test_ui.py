import os
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pygame = pytest.importorskip("pygame")

from moneySmarts.ui import Button
from moneySmarts.constants import PRIMARY

def test_button_creation_and_update():
    pygame.init()
    screen = pygame.display.set_mode((200, 100))
    clicked = []
    def cb():
        clicked.append(True)
    btn = Button(10, 10, 100, 40, "Test", color=PRIMARY, action=cb)
    # Simulate hover and click
    btn.update((15, 20), False)
    assert not clicked
    action = btn.update((15, 20), True)
    if action:
        action()
    assert clicked, "Button action should have been invoked on click"
    # Draw (smoke test)
    btn.draw(screen)
    pygame.quit()

