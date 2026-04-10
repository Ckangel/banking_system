from models.base_account import BankAccount

class CurrentAccount(BankAccount):
    OVERDRAFT_LIMIT = 1000.00

    def __init__(self, name, balance, acc_number=None):
        # Pass name and balance up to the BankAccount parent
        super().__init__(name, balance, acc_number)

    def account_type(self):
        return "Current Account"

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: Withdrawal must be positive.")
            return False

        if (self._balance + self.OVERDRAFT_LIMIT) >= amount:
            self._balance -= amount
            self._log_transaction("Withdrawal", amount)
            return True
        else:
            print("Denied! Exceeds overdraft limit.")
            return False