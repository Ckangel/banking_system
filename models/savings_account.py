from models.base_account import BankAccount

class SavingsAccount(BankAccount):
    MIN_BALANCE = 500.00

    def account_type(self):
        return "Savings Account"

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: Withdrawal must be positive.")
            return False
            
        # Rule: Balance cannot go below MIN_BALANCE
        if self._balance - amount >= self.MIN_BALANCE:
            self._balance -= amount
            print(f"Savings Withdrawal Successful: ${amount:.2f}")
            return True
        else:
            print(f"Denied! Savings accounts must maintain a ${self.MIN_BALANCE} minimum.")
            return False