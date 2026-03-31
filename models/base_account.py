from abc import ABC, abstractmethod
from datetime import datetime

class BankAccount(ABC):
    def __init__(self, name, balance):
        self.name = name
        self._balance = balance 
        self._history = []  # Internal list for transaction logs
        self._log_transaction("Account Created", balance)

    def _log_transaction(self, action, amount):
        """Helper to create a timestamped record."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} | {action}: ${amount:,.2f} | Balance: ${self._balance:,.2f}"
        self._history.append(entry)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._log_transaction("Deposit", amount)
            print(f"Deposited: ${amount:.2f}")
        else:
            print("Error: Deposit must be positive.")

    def save_to_file(self):
        """Writes the entire account state and history to a text file."""
        filename = f"{self.name}_data.txt"
        try:
            with open(filename, "w") as f:
                f.write(f"USER: {self.name}\n")
                f.write(f"TYPE: {self.account_type()}\n")
                f.write(f"FINAL_BALANCE: {self._balance}\n")
                f.write("-" * 50 + "\n")
                f.write("TRANSACTION HISTORY:\n")
                for record in self._history:
                    f.write(record + "\n")
            print(f"Success: Data saved to {filename}")
        except IOError as e:
            print(f"File Error: Could not save data. {e}")

    @abstractmethod
    def account_type(self):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def get_balance(self):
        return self._balance