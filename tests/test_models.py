import pytest
from moneySmarts.models import Player, BankAccount, Loan, Asset

def test_player_creation():
    player = Player("TestUser")
    assert player.name == "TestUser"
    assert player.age == 16
    assert player.cash >= 0
    assert player.bank_account is None

def test_bank_account_deposit_withdraw():
    acc = BankAccount()
    assert acc.deposit(100)
    assert acc.balance == 100
    assert acc.withdraw(50)
    assert acc.balance == 50
    with pytest.raises(Exception):
        acc.withdraw(1000)  # Should fail

def test_loan_payment():
    loan = Loan("TestLoan", 1200, 0.12, 1)
    old_balance = loan.current_balance
    assert loan.make_payment(loan.monthly_payment)
    assert loan.current_balance < old_balance

def test_asset_depreciation():
    car = Asset("Car", "TestCar", 10000)
    car.age_asset()
    assert car.current_value < 10000

