"""Test script to demonstrate the add_balance() feature."""

from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount
from logger import get_logger

logger = get_logger()

def test_add_balance():
    logger.info("=== Testing Add Balance Feature ===")
    print("--- Testing Add Balance Feature ---\n")
    
    try:
        # Create savings account
        savings = SavingsAccount("John Doe", 1000)
        print(f"Initial Savings Balance: ${savings.get_balance():.2f}")
        
        # Add balance directly (e.g., interest credited)
        logger.info("Adding interest to savings account")
        savings.add_balance(50)
        print(f"After interest: ${savings.get_balance():.2f}\n")
        
        # Create current account
        current = CurrentAccount("Jane Smith", 2000)
        print(f"Initial Current Balance: ${current.get_balance():.2f}")
        
        # Add balance directly (e.g., bonus/promotion)
        logger.info("Adding promotional credit to current account")
        current.add_balance(100)
        print(f"After promotional credit: ${current.get_balance():.2f}\n")
        
        # Test error case - negative amount
        print("Testing invalid amount (negative):")
        logger.info("Attempting to add negative balance")
        result = savings.add_balance(-50)
        print(f"Result: {result}\n")
        
        # Test valid large amount
        print("Adding large amount:")
        logger.info("Adding large balance adjustment")
        savings.add_balance(500)
        print(f"Final Savings Balance: ${savings.get_balance():.2f}\n")
        
        # Save account data
        logger.info("Saving account data to file")
        savings.save_to_file()
        current.save_to_file()
        
    except Exception as e:
        logger.error(f"Error in test_add_balance: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_add_balance()
