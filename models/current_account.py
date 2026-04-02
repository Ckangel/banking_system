from models.base_account import BankAccount
from logger import get_logger
from validators import AccountValidator, ValidationError
from verifiers import TransactionVerifier

class CurrentAccount(BankAccount):
    """Current account that supports an overdraft up to a fixed limit."""

    OVERDRAFT_LIMIT = 1000.00

    def account_type(self) -> str:
        return "Current Account"

    def withdraw(self, amount: float) -> bool:
        """Withdraw money while enforcing overdraft limit and logging."""
        
        self.logger = get_logger()
        
        try:
            # Validate amount
            AccountValidator.validate_amount(amount, operation="withdrawal")
            
            # Validate overdraft withdrawal
            is_valid, error_msg = AccountValidator.validate_overdraft_withdrawal(
                self._balance, amount, self.OVERDRAFT_LIMIT
            )
            
            if not is_valid:
                self.logger.transaction(self.name, "Withdrawal", amount, self._balance, "FAILED")
                print(f"Denied! {error_msg}")
                return False
            
            # Verify overdraft won't be exceeded
            if not TransactionVerifier.verify_overdraft_not_exceeded(
                self._balance - amount, self.OVERDRAFT_LIMIT
            ):
                self.logger.transaction(self.name, "Withdrawal", amount, self._balance, "FAILED")
                print(f"Error: Withdrawal would exceed overdraft limit of ${self.OVERDRAFT_LIMIT:.2f}.")
                return False
            
            # Perform withdrawal
            previous_balance = self._balance
            self._balance -= amount
            
            # Verify transaction
            is_valid, checks = TransactionVerifier.verify_withdrawal_operation(
                previous_balance, amount, self._balance
            )
            
            if not is_valid:
                self.logger.error(f"Withdrawal verification failed: {checks}")
                self._balance = previous_balance  # Rollback
                return False
            
            self._log_transaction("Withdrawal", amount)
            self.logger.transaction(self.name, "Withdrawal", amount, self._balance, "SUCCESS")
            print(f"Current withdrawal successful: ${amount:.2f}")
            
            if self._balance < 0:
                self.logger.warning(f"Overdraft being used - Balance: ${self._balance:.2f}")
                print(
                    f"Warning: You are now using your overdraft! "
                    f"(Balance: ${self._balance:.2f})"
                )
            
            return True
            
        except ValidationError as e:
            self.logger.warning(f"Withdrawal validation failed for {self.name}: {e}")
            print(f"Error: {e}")
            self.logger.transaction(self.name, "Withdrawal", amount, self._balance, "FAILED")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during withdrawal for {self.name}: {e}")
            print(f"Unexpected error: {e}")
            return False