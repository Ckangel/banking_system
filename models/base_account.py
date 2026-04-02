from abc import ABC, abstractmethod
from datetime import datetime
from logger import get_logger
from validators import AccountValidator, ValidationError
from verifiers import AccountVerifier, TransactionVerifier

class BankAccount(ABC):
    def __init__(self, name, balance):
        self.logger = get_logger()
        
        # Validate inputs
        try:
            AccountValidator.validate_name(name)
            AccountValidator.validate_balance(balance)
        except ValidationError as e:
            self.logger.error(f"Failed to create account: {e}")
            raise
        
        # Verify account can be created
        is_valid, conditions = AccountVerifier.verify_account_creation(name, balance)
        if not is_valid:
            self.logger.error(f"Account creation verification failed: {conditions}")
            raise ValueError(f"Invalid account creation parameters: {conditions}")
        
        self.name = name
        self._balance = balance 
        self._history = []  # Internal list for transaction logs
        
        self.logger.info(f"Account created successfully - Name: {name}, Initial Balance: ${balance:.2f}")
        self._log_transaction("Account Created", balance)

    def _log_transaction(self, action, amount):
        """Helper to create a timestamped record."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} | {action}: ${amount:,.2f} | Balance: ${self._balance:,.2f}"
        self._history.append(entry)

    def deposit(self, amount):
        try:
            # Validate amount
            AccountValidator.validate_amount(amount, operation="deposit")
            
            previous_balance = self._balance
            self._balance += amount
            
            # Verify transaction integrity
            is_valid, checks = TransactionVerifier.verify_deposit_operation(
                previous_balance, amount, self._balance
            )
            
            if not is_valid:
                self.logger.error(f"Deposit verification failed: {checks}")
                self._balance = previous_balance  # Rollback
                return False
            
            self._log_transaction("Deposit", amount)
            self.logger.transaction(self.name, "Deposit", amount, self._balance, "SUCCESS")
            print(f"Deposited: ${amount:.2f}")
            return True
            
        except ValidationError as e:
            self.logger.warning(f"Deposit validation failed for {self.name}: {e}")
            print(f"Error: {e}")
            self.logger.transaction(self.name, "Deposit", amount, self._balance, "FAILED")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during deposit for {self.name}: {e}")
            print(f"Unexpected error: {e}")
            return False

    def save_to_file(self):
        """Writes the entire account state and history to a text file."""
        filename = f"{self.name}_data.txt"
        try:
            # Verify account state before saving
            is_valid, checks = AccountVerifier.verify_account_state(
                self.name, self._balance, self.account_type()
            )
            
            if not is_valid:
                self.logger.error(f"Account state verification failed before save: {checks}")
                print(f"Error: Cannot save account with invalid state.")
                return False
            
            with open(filename, "w") as f:
                f.write(f"USER: {self.name}\n")
                f.write(f"TYPE: {self.account_type()}\n")
                f.write(f"FINAL_BALANCE: {self._balance}\n")
                f.write("-" * 50 + "\n")
                f.write("TRANSACTION HISTORY:\n")
                for record in self._history:
                    f.write(record + "\n")
            
            self.logger.info(f"Data saved successfully to {filename}")
            print(f"Success: Data saved to {filename}")
            return True
            
        except IOError as e:
            self.logger.error(f"File Error: Could not save data for {self.name}. {e}")
            print(f"File Error: Could not save data. {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while saving data for {self.name}: {e}")
            print(f"Unexpected error: {e}")
            return False

    @abstractmethod
    def account_type(self):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def add_balance(self, amount):
        """Add balance directly (e.g., for interest, admin adjustments)."""
        try:
            # Validate amount
            AccountValidator.validate_amount(amount, operation="balance addition")
            
            previous_balance = self._balance
            self._balance += amount
            
            # Verify transaction integrity
            is_valid, checks = TransactionVerifier.verify_deposit_operation(
                previous_balance, amount, self._balance
            )
            
            if not is_valid:
                self.logger.error(f"Balance addition verification failed: {checks}")
                self._balance = previous_balance  # Rollback
                print(f"Error: Balance addition verification failed.")
                return False
            
            self._log_transaction("Balance Addition", amount)
            self.logger.transaction(self.name, "Balance Addition", amount, self._balance, "SUCCESS")
            print(f"Balance added: ${amount:.2f} | New Balance: ${self._balance:.2f}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during balance addition for {self.name}: {e}")
            print(f"Error: {e}")
            return False

    def get_balance(self):
        return self._balance