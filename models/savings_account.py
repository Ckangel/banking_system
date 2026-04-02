from models.base_account import BankAccount
from logger import get_logger
from validators import AccountValidator, ValidationError
from verifiers import TransactionVerifier

class SavingsAccount(BankAccount):
    MIN_BALANCE = 500.00

    def account_type(self):
        return "Savings Account"

    def withdraw(self, amount):
        self.logger = get_logger()
        
        try:
            # Validate amount
            AccountValidator.validate_amount(amount, operation="withdrawal")
            
            # Validate withdrawal for savings account
            is_valid, error_msg = AccountValidator.validate_savings_withdrawal(
                self._balance, amount, self.MIN_BALANCE
            )
            
            if not is_valid:
                self.logger.transaction(self.name, "Withdrawal", amount, self._balance, "FAILED")
                print(f"Denied! {error_msg}")
                return False
            
            # Verify minimum balance will be maintained
            if not TransactionVerifier.verify_minimum_balance_maintained(
                self._balance - amount, self.MIN_BALANCE
            ):
                self.logger.transaction(self.name, "Withdrawal", amount, self._balance, "FAILED")
                print(f"Error: Withdrawal would violate minimum balance requirement.")
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
            print(f"Savings Withdrawal Successful: ${amount:.2f}")
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