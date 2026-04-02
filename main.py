from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount
from logger import get_logger

logger = get_logger()

def test_setup():
    logger.info("=== Sprint 1: Architecture Test ===")
    print("--- Sprint 1: Architecture Test ---")
    
    try:
        # Creating objects (Inheritance)
        savings = SavingsAccount("Deepak", 1000)
        current = CurrentAccount("Amit", 500)

        # Testing Polymorphism
        accounts = [savings, current]
        for acc in accounts:
            print(f"User: {acc.name} | Type: {acc.account_type()} | Balance: ${acc.get_balance()}")
            logger.debug(f"Account Info - {acc.name}: {acc.account_type()}, Balance: ${acc.get_balance()}")
    except Exception as e:
        logger.error(f"Error in sprint 1: {e}")
        print(f"Error in sprint 1: {e}")

if __name__ == "__main__":
    test_setup()

print ("--------------------------------------------------------------------------------------------")

from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount

def sprint_2_test():
    logger.info("=== Sprint 2: Validation Test ===")
    print("--- Sprint 2: Validation Test ---")
    
    try:
        # Test Savings Minimum Balance
        sav = SavingsAccount("Deepak", 600)
        print(f"Initial Savings: ${sav.get_balance()}")
        result = sav.withdraw(200)  # Should fail (600 - 200 = 400, which is < 500)
        logger.debug(f"Savings withdrawal attempt: amount=200, success={result}")
        
        # Test Current Overdraft
        curr = CurrentAccount("Amit", 100)
        print(f"\nInitial Current: ${curr.get_balance()}")
        result = curr.withdraw(500)  # Should pass (Uses $400 of overdraft)
        logger.debug(f"Current overdraft withdrawal: amount=500, success={result}")
        print(f"New Balance: ${curr.get_balance()}")
    except Exception as e:
        logger.error(f"Error in sprint 2: {e}")
        print(f"Error in sprint 2: {e}")

if __name__ == "__main__":
    sprint_2_test()

print ("--------------------------------------------------------------------------------------------")

from models.savings_account import SavingsAccount

def sprint_3_test():
    logger.info("=== Sprint 3: Persistence Test ===")
    print("--- Sprint 3: Persistence Test ---")
    
    try:
        user_acc = SavingsAccount("Deepak", 1000)
        
        logger.info("Performing deposit transaction")
        user_acc.deposit(500)
        
        logger.info("Performing withdrawal transaction")
        user_acc.withdraw(200)
        
        # This should create 'Deepak_data.txt' in your folder
        logger.info("Saving account data to file")
        user_acc.save_to_file()
    except Exception as e:
        logger.error(f"Error in sprint 3: {e}")
        print(f"Error in sprint 3: {e}")

if __name__ == "__main__":
    sprint_3_test()