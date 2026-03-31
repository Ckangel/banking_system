from models.base_account import BankAccount

class CurrentAccount(BankAccount):
    """Current account that supports an overdraft up to a fixed limit."""

    OVERDRAFT_LIMIT = 1000.00

    def account_type(self) -> str:
        return "Current Account"

    def withdraw(self, amount: float) -> bool:
        """Withdraw money while enforcing overdraft limit and logging."""

        # Validate amount
        if amount <= 0:
            print("Error: Withdrawal amount must be positive.")
            return False

        # Rule: Balance can go negative down to -OVERDRAFT_LIMIT
        if self._balance - amount < -self.OVERDRAFT_LIMIT:
            print(
                f"Denied! Withdrawal exceeds your "
                f"${self.OVERDRAFT_LIMIT:.2f} overdraft limit."
            )
            return False

        # Perform withdrawal
        self._balance -= amount
        self._log_transaction("Withdrawal", amount)
        print(f"Current withdrawal successful: ${amount:.2f}")

        if self._balance < 0:
            print(
                f"Warning: You are now using your overdraft! "
                f"(Balance: ${self._balance:.2f})"
            )

        return True