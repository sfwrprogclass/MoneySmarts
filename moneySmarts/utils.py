"""
Utility functions for MoneySmarts game.
"""
import logging

def safe_float_input(prompt, min_value=None, max_value=None):
    """
    Prompt the user for a float input, with optional min/max validation.
    Returns the float value or None if input is invalid.
    """
    try:
        value = float(input(prompt))
        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            return None
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            return None
        return value
    except ValueError:
        print("Please enter a valid number.")
        return None

def safe_int_input(prompt, min_value=None, max_value=None):
    """
    Prompt the user for an integer input, with optional min/max validation.
    Returns the int value or None if input is invalid.
    """
    try:
        value = int(input(prompt))
        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            return None
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            return None
        return value
    except ValueError:
        print("Please enter a valid integer.")
        return None

def log_and_raise(exception, message):
    """
    Log an error message and raise the given exception.
    """
    logging.error(message)
    raise exception(message)

def compute_net_worth(player):
    """Compute player's net worth.
    Components:
      + cash
      + checking (bank_account if type != Savings)
      + savings_account (if present)
      + investments (sum of investment.amount)
      + asset current values
      - credit card balance
      - loan current balances
    Returns float.
    Safe against missing attributes.
    """
    if not player:
        return 0.0
    cash = getattr(player, 'cash', 0.0) or 0.0
    checking = 0.0
    if getattr(player, 'bank_account', None) and player.bank_account.account_type != 'Savings':
        checking = player.bank_account.balance
    savings = getattr(getattr(player, 'savings_account', None), 'balance', 0.0) or 0.0
    investments_total = 0.0
    for inv in getattr(player, 'investments', []) or []:
        investments_total += getattr(inv, 'amount', 0.0) or 0.0
    asset_value = 0.0
    for asset in getattr(player, 'assets', []) or []:
        asset_value += getattr(asset, 'current_value', 0.0) or 0.0
    credit_debt = 0.0
    if getattr(player, 'credit_card', None):
        credit_debt = player.credit_card.balance
    loan_debt = 0.0
    for loan in getattr(player, 'loans', []) or []:
        loan_debt += getattr(loan, 'current_balance', 0.0) or 0.0
    return cash + checking + savings + investments_total + asset_value - credit_debt - loan_debt
def compute_net_worth(player):
    """Compute player's net worth.
    Components:
      + cash
      + checking (bank_account if type != Savings)
      + savings_account (if present)
      + investments (sum of investment.amount)
      + asset current values
      - credit card balance
      - loan current balances
    Returns float.
    Safe against missing attributes.
    """
    if not player:
        return 0.0
    cash = getattr(player, 'cash', 0.0) or 0.0
    checking = 0.0
    if getattr(player, 'bank_account', None) and player.bank_account.account_type != 'Savings':
        checking = player.bank_account.balance
    savings = getattr(getattr(player, 'savings_account', None), 'balance', 0.0) or 0.0
    investments_total = 0.0
    for inv in getattr(player, 'investments', []) or []:
        investments_total += getattr(inv, 'amount', 0.0) or 0.0
    asset_value = 0.0
    for asset in getattr(player, 'assets', []) or []:
        asset_value += getattr(asset, 'current_value', 0.0) or 0.0
    credit_debt = 0.0
    if getattr(player, 'credit_card', None):
        credit_debt = player.credit_card.balance
    loan_debt = 0.0
    for loan in getattr(player, 'loans', []) or []:
        loan_debt += getattr(loan, 'current_balance', 0.0) or 0.0
    return cash + checking + savings + investments_total + asset_value - credit_debt - loan_debt
