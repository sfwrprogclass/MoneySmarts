"""
Money Smartz: Financial Life Simulator

A 2D graphical financial education game inspired by the classic Oregon Trail.
This game simulates the financial journey of life, from your first bank account
as a teenager to retirement.
"""

# Export main modules
from moneySmarts.constants import *
from moneySmarts.models import Player, BankAccount, Card, Loan, Asset
from moneySmarts.game import Game
from moneySmarts.ui import Button, TextInput, Screen, GUIManager
from moneySmarts.image_manager import ImageManager, image_manager

# Version information
__version__ = "1.0.0"
