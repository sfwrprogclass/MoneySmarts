"""
Money Smartz: Financial Life Simulator

A 2D graphical financial education game inspired by the classic Oregon Trail.
This game simulates the financial journey of life, from your first bank account
as a teenager to retirement.
"""

# Export core modules (pygame-free)
from moneySmarts.constants import *  # noqa
from moneySmarts.models import Player, BankAccount, Card, Loan, Asset  # noqa
from moneySmarts.game import Game  # noqa

# Optional / pygame-dependent exports (guarded so tests run headless)
try:  # pragma: no cover
    from moneySmarts.ui import Button, TextInput, Screen, GUIManager  # noqa
except Exception:  # pragma: no cover
    Button = TextInput = Screen = GUIManager = None  # type: ignore

try:  # image manager optional
    from moneySmarts.image_manager import ImageManager, image_manager  # noqa
except Exception:  # pragma: no cover
    ImageManager = image_manager = None  # type: ignore

__all__ = [
    'Player','BankAccount','Card','Loan','Asset','Game',
    'Button','TextInput','Screen','GUIManager','ImageManager','image_manager'
]

# Version information
__version__ = "1.0.0"
