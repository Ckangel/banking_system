from models.base_account import BankAccount

class SavingsAccount(BankAccount):
    MIN_BALANCE = 500.00

    def __init__(self, name, balance):
        # Pass name and balance up to the BankAccount parent
        super().__init__(name, balance)

    def account_type(self):
        return "Savings Account"

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: Withdrawal must be positive.")
            return False
            
        if (self._balance - amount) >= self.MIN_BALANCE:
            self._balance -= amount
            self._log_transaction("Withdrawal", amount)
            return True
        else:
            print(f"Denied! Minimum balance of ${self.MIN_BALANCE} required.")
            return False