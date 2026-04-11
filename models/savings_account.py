from models.base_account import BankAccount
from logger import get_logger
from validators import AccountValidator, ValidationError
from verifiers import TransactionVerifier

class SavingsAccount(BankAccount):
    MIN_BALANCE = 500.00

    def __init__(self, name, balance, acc_number=None):
        # Pass name and balance up to the BankAccount parent
        super().__init__(name, balance, acc_number)

    def account_type(self):
        return "Savings Account"

    def withdraw(self, amount):
        if 0 < amount <= self._balance - 500:
            self._balance -= amount
            self._log_transaction("Withdrawal", -amount)
            return True
        return False
