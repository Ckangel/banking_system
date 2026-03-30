from models.base_account import BankAccount

class CurrentAccount(BankAccount):
    OVERDRAFT_LIMIT = 1000.00

    def account_type(self):
        return "Current Account"

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: Withdrawal must be positive.")
            return False

        # Rule: Balance can go negative down to -OVERDRAFT_LIMIT
        if (self._balance + self.OVERDRAFT_LIMIT) >= amount:
            self._balance -= amount
            print(f"Current Withdrawal Successful: ${amount:.2f}")
            if self._balance < 0:
                print(f"Warning: You are now using your overdraft! (Balance: ${self._balance:.2f})")
            return True
        else:
            print(f"Denied! Withdrawal exceeds your ${self.OVERDRAFT_LIMIT} overdraft limit.")
            return False