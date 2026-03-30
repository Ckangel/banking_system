from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, name, balance):
        self.name = name
        self._balance = balance 

    @abstractmethod
    def account_type(self):
        pass

    @abstractmethod
    def withdraw(self, amount):
        """Each account type will handle withdrawals differently."""
        pass

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited: ${amount:.2f}")
        else:
            print("Error: Deposit must be a positive number.")

    def get_balance(self):
        return self._balance