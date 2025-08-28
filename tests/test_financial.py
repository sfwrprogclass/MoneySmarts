import random
import types
from moneySmarts.game import Game
from moneySmarts.models import Player, BankAccount, Investment, Loan, Asset
from moneySmarts.utils import compute_net_worth


def make_player(name="Tester"):
    p = Player(name)
    p.cash = 1000.0
    return p


def test_investment_monthly_return_compounds():
    p = make_player()
    # 12% annual -> 1% monthly on initial principal, compounds
    inv = Investment("Stock", 1000.0, 0.12)
    p.investments.append(inv)
    monthly_gain1 = inv.apply_monthly_return()
    assert 9.9 < monthly_gain1 < 10.1  # ~1% of 1000
    monthly_gain2 = inv.apply_monthly_return()
    # second month should be slightly higher due to compounding
    assert monthly_gain2 > monthly_gain1


def test_random_event_positive_applied_once():
    g = Game()
    g.player = make_player()
    start_cash = g.player.cash
    # Override events with deterministic positive event
    g.events = {"positive": [{"name": "Test Positive", "description": "", "cash_effect": lambda: 250}], "negative": []}
    random.seed(0)
    # Force positive by picking from only positive list
    g.trigger_random_event()
    assert g.player.cash == start_cash + 250


def test_random_event_negative_applied_once_with_cash():
    g = Game()
    g.player = make_player()
    start_cash = g.player.cash
    g.events = {"positive": [], "negative": [{"name": "Test Negative", "description": "", "cash_effect": lambda: -300}]}
    random.seed(1)
    g.trigger_random_event()
    assert g.player.cash == start_cash - 300


def test_compute_net_worth_includes_savings_and_investments():
    p = make_player()
    # Checking
    p.bank_account = BankAccount("Checking")
    p.bank_account.deposit(500)
    # Savings
    p.savings_account = BankAccount("Savings")
    p.savings_account.deposit(200)
    # Investment
    inv = Investment("Bond", 1000, 0.06)
    p.investments.append(inv)
    # Asset
    p.assets.append(Asset("Car", "Used Car", 5000))
    # Loan debt
    loan = Loan("Auto", 6000, 0.05, 5)
    p.loans.append(loan)
    # Simulate some principal paid
    loan.make_payment(loan.monthly_payment)
    nw = compute_net_worth(p)
    # Expected: cash(1000) + checking(500) + savings(200) + inv(1000) + asset(5000) - loan balance (~ < 6000) = > 1700
    assert nw > 1700

