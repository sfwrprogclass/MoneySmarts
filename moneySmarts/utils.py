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