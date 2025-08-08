"""
Custom exceptions for the MoneySmarts game.
"""

class GameError(Exception):
    """Base exception for game-related errors."""
    pass

class ConfigError(GameError):
    """Exception for configuration-related errors."""
    pass

class BankAccountError(GameError):
    """Exception for bank account-related errors."""
    pass

class LoanError(GameError):
    """Exception for loan-related errors."""
    pass

class AssetError(GameError):
    """Exception for asset-related errors."""
    pass

class GameSaveError(GameError):
    """Exception for game save/load-related errors."""
    pass