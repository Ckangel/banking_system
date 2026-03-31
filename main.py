from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount

def test_setup():
    print("--- Sprint 1: Architecture Test ---")
    
    # Creating objects (Inheritance)
    savings = SavingsAccount("Deepak", 1000)
    current = CurrentAccount("Amit", 500)

    # Testing Polymorphism
    accounts = [savings, current]
    for acc in accounts:
        print(f"User: {acc.name} | Type: {acc.account_type()} | Balance: ${acc.get_balance()}")

if __name__ == "__main__":
    test_setup()

print ("--------------------------------------------------------------------------------------------")

from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount

def sprint_2_test():
    print("--- Sprint 2: Validation Test ---")
    
    # Test Savings Minimum Balance
    sav = SavingsAccount("Deepak", 600)
    print(f"Initial Savings: ${sav.get_balance()}")
    sav.withdraw(200) # Should fail (600 - 200 = 400, which is < 500)
    
    # Test Current Overdraft
    curr = CurrentAccount("Amit", 100)
    print(f"\nInitial Current: ${curr.get_balance()}")
    curr.withdraw(500) # Should pass (Uses $400 of overdraft)
    print(f"New Balance: ${curr.get_balance()}")

if __name__ == "__main__":
    sprint_2_test()

print ("--------------------------------------------------------------------------------------------")

from models.savings_account import SavingsAccount

def sprint_3_test():
    print("--- Sprint 3: Persistence Test ---")
    user_acc = SavingsAccount("Deepak", 1000)
    
    user_acc.deposit(500)
    user_acc.withdraw(200)
    
    # This should create 'Deepak_data.txt' in your folder
    user_acc.save_to_file()

if __name__ == "__main__":
    sprint_3_test()