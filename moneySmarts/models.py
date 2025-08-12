import random
import logging
from moneySmarts.config_manager import Config
from moneySmarts.exceptions import BankAccountError, LoanError, AssetError

class Player:
    """
    Represents the player character in the game.
    Tracks personal and financial information, including age, education, job, salary, cash, accounts, credit, loans, assets, family, and bills.

    Attributes:
        name (str): Player's name.
        age (int): Player's age.
        education (str): Player's education status.
        job (str): Player's current job title.
        salary (float): Player's annual salary.
        cash (float): Player's available cash.
        bank_account (BankAccount): Player's bank account.
        debit_card (Card): Player's debit card.
        credit_card (Card): Player's credit card.
        credit_score (int): Player's credit score.
        loans (list): List of Loan objects.
        assets (list): List of Asset objects.
        family (list): List of family members (dicts).
        inventory (list): List of purchased items.
        recurring_bills (list): List of recurring bills (dicts).
        utility_bills (list): List of utility bills (dicts).
    """
    def __init__(self, name):
        self.name = name
        self.age = 16
        self.education = "High School"
        self.job = None
        self.salary = 0
        self.cash = Config.get("starting_cash", 100)  # Configurable
        self.bank_account = None
        self.savings_account = None  # Add this line for savings account support
        self.debit_card = None
        self.credit_card = None
        self.credit_score = Config.get("starting_credit_score", 650)  # Configurable
        self.loans = []
        self.assets = []
        self.family = []  # List of family members (spouse, children)
        self.inventory = []  # List of purchased items
        self.recurring_bills = []  # List of dicts: {name, amount, source}
        self.utility_bills = Config.get("utility_bills", [
            {"name": "Electricity", "amount": 60},
            {"name": "Water", "amount": 30},
            {"name": "Internet", "amount": 50}
        ]
        self.insurance_policies = []  # List of Insurance objects
        self.investments = []  # List of Investment objects

    def purchase_insurance(self, insurance_type, premium, coverage_amount, deductible):
        """Add a new insurance policy to the player."""
        from moneySmarts.models import Insurance
        policy = Insurance(insurance_type, premium, coverage_amount, deductible)
        self.insurance_policies.append(policy)
        self.recurring_bills.append({
            "name": f"{insurance_type} Insurance Premium",
            "amount": premium,
            "source": "bank_or_credit"
        })

    def invest(self, investment_type, amount, expected_annual_return):
        """Add a new investment for the player."""
        from moneySmarts.models import Investment
        if amount > 0 and self.cash >= amount:
            self.cash -= amount
            investment = Investment(investment_type, amount, expected_annual_return)
            self.investments.append(investment)
            return True
        return False

    def file_insurance_claim(self, insurance_type, loss_amount):
        """File a claim for a specific insurance type if policy exists."""
        for policy in self.insurance_policies:
            if policy.insurance_type == insurance_type and policy.active:
                payout = policy.file_claim(loss_amount)
                self.cash += payout
                return payout
        return 0

    def purchase_investment(self):
        """Menu-driven investment purchase for realism."""
        print("\n--- INVESTMENT OPTIONS ---")
        print("1. Stock Market (Avg. 7% annual return, high risk)")
        print("2. Bonds (Avg. 3% annual return, low risk)")
        print("3. Retirement Account (Avg. 5% annual return, medium risk)")
        choice = input("Choose investment type (1-3): ")
        if choice == "1":
            inv_type, ret = "Stock", 0.07
        elif choice == "2":
            inv_type, ret = "Bond", 0.03
        elif choice == "3":
            inv_type, ret = "Retirement", 0.05
        else:
            print("Invalid choice.")
            return False
        amt = 0
        while amt <= 0 or amt > self.cash:
            try:
                amt = float(input(f"How much to invest? Available cash: ${self.cash:.2f}: "))
                if amt <= 0:
                    print("Amount must be positive.")
                elif amt > self.cash:
                    print("Not enough cash.")
            except Exception:
                print("Invalid input.")
        return self.invest(inv_type, amt, ret)

    def purchase_insurance_menu(self):
        """Menu-driven insurance purchase for realism."""
        print("\n--- INSURANCE OPTIONS ---")
        print("1. Car Insurance ($50/mo, $10,000 coverage, $500 deductible)")
        print("2. Home Insurance ($60/mo, $200,000 coverage, $1,000 deductible)")
        print("3. Health Insurance ($80/mo, $50,000 coverage, $1,000 deductible)")
        choice = input("Choose insurance type (1-3): ")
        if choice == "1":
            self.purchase_insurance("Car", 50, 10000, 500)
        elif choice == "2":
            self.purchase_insurance("Home", 60, 200000, 1000)
        elif choice == "3":
            self.purchase_insurance("Health", 80, 50000, 1000)
        else:
            print("Invalid choice.")
            return False
        print("Insurance purchased.")
        return True

class BankAccount:
    """
    Represents a bank account that can hold money and earn interest.

    Attributes:
        account_type (str): Type of account ('Checking' or 'Savings').
        balance (float): Current account balance.
        interest_rate (float): Annual interest rate (for savings).
        transaction_history (list): List of transaction records (dicts).
    """
    def __init__(self, account_type="Checking"):
        self.account_type = account_type
        self.balance = 0
        self.interest_rate = 0.01 if account_type == "Savings" else 0.0
        self.transaction_history = []

    def deposit(self, amount):
        """Deposit money into the account. Returns True if successful, raises BankAccountError on failure."""
        try:
            if amount > 0:
                self.balance += amount
                self.transaction_history.append({"type": "deposit", "amount": amount})
                return True
            else:
                raise BankAccountError("Deposit amount must be positive.")
        except Exception as e:
            logging.error(f"BankAccount deposit error: {e}")
            raise BankAccountError(f"Deposit failed: {e}")

    def withdraw(self, amount):
        """Withdraw money from the account if sufficient funds are available. Returns True if successful, raises BankAccountError on failure."""
        try:
            if 0 < amount <= self.balance:
                self.balance -= amount
                self.transaction_history.append({"type": "withdrawal", "amount": amount})
                return True
            else:
                raise BankAccountError("Insufficient funds or invalid withdrawal amount.")
        except Exception as e:
            logging.error(f"BankAccount withdraw error: {e}")
            raise BankAccountError(f"Withdrawal failed: {e}")

    def apply_interest(self):
        """Apply interest to the account balance (for savings accounts). Returns the interest amount, logs errors."""
        try:
            if self.account_type == "Savings" and self.balance > 0:
                interest = self.balance * self.interest_rate
                self.balance += interest
                self.transaction_history.append({"type": "interest", "amount": interest})
                return interest
            return 0
        except Exception as e:
            logging.error(f"BankAccount interest error: {e}")
            return 0

class Card:
    """
    Represents a payment card (debit or credit).

    Attributes:
        card_type (str): 'Debit' or 'Credit'.
        limit (float): Credit limit (for credit cards).
        balance (float): Current balance (for credit cards).
        transaction_history (list): List of transaction records (dicts).
    """
    def __init__(self, card_type, limit=0):
        self.card_type = card_type
        self.limit = limit
        self.balance = 0
        self.transaction_history = []

    def charge(self, amount):
        """
        Charge an amount to the card.
        For debit cards, this is a placeholder as they use the bank account directly.
        For credit cards, this adds to the balance if within the limit.
        Returns True if successful.
        """
        if amount <= 0:
            return False
            
        if self.card_type == "Credit":
            if self.balance + amount <= self.limit:
                self.balance += amount
                self.transaction_history.append({"type": "charge", "amount": amount})
                return True
            return False
        return True  # Debit cards don't track balance here

    def pay(self, amount):
        """Pay off some of the credit card balance. Returns True if successful."""
        if self.card_type == "Credit" and 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append({"type": "payment", "amount": amount})
            return True
        return False

class Loan:
    """
    Represents a loan with principal, interest rate, and term.

    Attributes:
        loan_type (str): Type of loan (e.g., 'Student', 'Auto', 'Mortgage').
        original_amount (float): Original loan amount.
        current_balance (float): Current balance remaining.
        interest_rate (float): Annual interest rate.
        term_years (int): Loan term in years.
        monthly_payment (float): Calculated monthly payment.
        payment_history (list): List of payment records (dicts).
    """
    def __init__(self, loan_type, amount, interest_rate, term_years):
        self.loan_type = loan_type
        self.original_amount = amount
        self.current_balance = amount
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.monthly_payment = self.calculate_payment()
        self.payment_history = []

    def calculate_payment(self):
        """Calculate the monthly payment for the loan. Returns the payment amount."""
        r = self.interest_rate / 12  # Monthly interest rate
        n = self.term_years * 12     # Total number of payments
        if r == 0:  # Handle zero interest case
            return self.original_amount / n
        return (self.original_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)

    def make_payment(self, amount):
        """Make a payment on the loan. Returns True if successful, raises LoanError on failure."""
        try:
            if amount <= 0:
                raise LoanError("Payment amount must be positive.")

        # Apply payment to interest first, then principal
        interest_payment = self.current_balance * (self.interest_rate / 12)

        # Check if payment covers interest
        if amount <= interest_payment:
            # If payment doesn't cover interest, all goes to interest
            interest_payment = amount
            principal_payment = 0
        else:
            # Payment covers interest and some principal
            principal_payment = min(amount - interest_payment, self.current_balance)

        self.current_balance -= principal_payment

        if self.current_balance < 0.01:  # Handle small floating-point errors
            self.current_balance = 0

        self.payment_history.append({
            "amount": amount,
            "interest": interest_payment,
            "principal": principal_payment

            })
            return True
        except Exception as e:
            logging.error(f"Loan payment error: {e}")
            raise LoanError(f"Loan payment failed: {e}")

class Asset:
    """
    Represents an asset owned by the player (car, house, etc.).

    Attributes:
        asset_type (str): Type of asset ('Car', 'House', etc.).
        name (str): Name or description of the asset.
        purchase_value (float): Original purchase value.
        current_value (float): Current estimated value.
        condition (str): Condition of the asset ('Good', 'Fair', 'Poor').
        age (int): Years since purchase.
    """
    def __init__(self, asset_type, name, value, condition="Good"):
        self.asset_type = asset_type
        self.name = name
        self.purchase_value = value
        self.current_value = value
        self.condition = condition
        self.age = 0  # Years since purchase

    def age_asset(self):
        """Age the asset by one year, affecting its value and condition."""
        self.age += 1
        
        # Update condition based on age
        if self.age > 10 and self.condition == "Good":
            self.condition = "Fair"
        elif self.age > 15 and self.condition == "Fair":
            self.condition = "Poor"
            
        # Update value based on asset type
        if self.asset_type == "Car":
            self.current_value *= 0.85  # 15% depreciation per year
        elif self.asset_type == "House":
            # Houses might appreciate
            appreciation = random.uniform(-0.05, 0.1)  # -5% to +10%
            self.current_value *= (1 + appreciation)

    def repair(self, cost):
        """Repair the asset to improve its condition. Returns the repair cost, logs errors."""
        try:
            self.condition = "Good"
            return cost
        except Exception as e:
            logging.error(f"Asset repair error: {e}")
            raise AssetError(f"Asset repair failed: {e}")

class Insurance:
    """
    Represents insurance for an asset or health.
    """
    def __init__(self, insurance_type, premium, coverage_amount, deductible):
        self.insurance_type = insurance_type  # e.g. 'Car', 'Home', 'Health'
        self.premium = premium  # Monthly cost
        self.coverage_amount = coverage_amount  # Max payout
        self.deductible = deductible  # Out-of-pocket cost before insurance pays
        self.active = True

    def file_claim(self, loss_amount):
        if not self.active:
            return 0
        payout = max(0, min(loss_amount - self.deductible, self.coverage_amount))
        return payout

class Investment:
    """
    Represents an investment (stocks, bonds, retirement).
    """
    def __init__(self, investment_type, amount, expected_annual_return):
        self.investment_type = investment_type  # e.g. 'Stock', 'Bond', 'Retirement'
        self.amount = amount
        self.expected_annual_return = expected_annual_return

    def apply_monthly_return(self):
        monthly_return = self.amount * (self.expected_annual_return / 12)
        self.amount += monthly_return
        return monthly_return
