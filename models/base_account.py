from abc import ABC, abstractmethod
from models.db_manager import db

class BankAccount(ABC):
    def __init__(self, name, balance, acc_number=None):
        self.name = name
        self._balance = balance
        self.acc_number = acc_number
        db.update_balance(self.name, self._balance)

    def get_balance(self):
        return self._balance

    @abstractmethod
    def account_type(self): pass

    @abstractmethod
    def withdraw(self, amount): pass

    def add_balance(self, amount):
        """Add balance directly (e.g., for interest, admin adjustments)."""
        try:
            # Validate amount
            AccountValidator.validate_amount(amount, operation="balance addition")
            
            previous_balance = self._balance
            self._balance += amount
            self._log_transaction("Deposit", amount)
            return True
        return False

    def _log_transaction(self, action, amount):
        db.add_transaction(self.name, action, amount)
        db.update_balance(self.name, self._balance)

    @staticmethod
    def login(name, password):
        user_data = db.verify_login(name, password)
        if user_data:
            acc_type, balance, acc_num = user_data
            if acc_type == "Savings Account":
                from models.savings_account import SavingsAccount
                return SavingsAccount(name, balance, acc_num)
            else:
                from models.current_account import CurrentAccount
                return CurrentAccount(name, balance, acc_num)
        return None