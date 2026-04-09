import os
from abc import ABC, abstractmethod
from models.db_manager import db  # Ensure db_manager.py exists in your models folder

class BankAccount(ABC):
    def __init__(self, name, balance):
        """
        Constructor: Initializes the account.
        """
        self.name = name
        self._balance = balance
        # CHANGE THIS LINE: Use update_balance instead of save_or_update_account
        db.update_balance(self.name, self._balance)

    def _log_transaction(self, action, amount):
        """
        Internal helper to log to the SQL transactions table 
        and update the current balance in the accounts table.
        """
        db.add_transaction(self.name, action, amount)
        # CHANGE THIS LINE: Use update_balance instead of save_or_update_account
        db.update_balance(self.name, self._balance)
    @abstractmethod
    def account_type(self):
        """Abstract method: Must be implemented by child classes."""
        pass

    @abstractmethod
    def withdraw(self, amount):
        """Abstract method: Specific rules implemented in Savings/Current."""
        pass

    def deposit(self, amount):
        """
        Updates the account balance and syncs it with the database.
        """
        if amount > 0:
            self._balance += amount
            self._log_transaction("Deposit", amount)
            print(f"Successfully deposited ${amount:,.2f}")
        else:
            print("Error: Deposit amount must be positive.")

    def get_balance(self):
        """Standard getter to return the current protected balance."""
        return self._balance

    def show_history(self):
        """Fetches and displays the transaction log from the database."""
        history = db.fetch_history(self.name)
        print(f"\n--- Transaction History for {self.name} ---")
        if not history:
            print("No transactions found.")
        else:
            for row in history:
                # SQLite returns rows as tuples: (timestamp, description, amount)
                print(f"{row[0]} | {row[1]}: ${row[2]:,.2f}")

    @staticmethod
    def login(name, password):
        """
        Static Method: Acts as a factory.
        Now takes BOTH name and password to verify against the DB hash.
        """
        # Import db here to ensure it's available
        from models.db_manager import db
        
        # This calls the method in db_manager that hashes the input 
        # and compares it to the stored password
        user_data = db.verify_login(name, password)
        
        if not user_data:
            return None
        
        acc_type, balance = user_data
        
        # Delayed imports to avoid circular dependency
        from models.savings_account import SavingsAccount
        from models.current_account import CurrentAccount
        
        if acc_type == "Savings Account":
            return SavingsAccount(name, balance)
        return CurrentAccount(name, balance)
        
        # Imports are inside the method to prevent 'Circular Import' errors
        from models.savings_account import SavingsAccount
        from models.current_account import CurrentAccount
        
        if acc_type == "Savings Account":
            return SavingsAccount(name, balance)
        return CurrentAccount(name, balance)