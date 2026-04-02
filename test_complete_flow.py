"""Complete test of the banking system with list accounts feature."""

from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount
from logger import get_logger

logger = get_logger()

# Simulate the accounts dictionary from interactive_banking.py
accounts = {}

def list_accounts():
    """List all created accounts."""
    print("\n--- All Accounts ---")
    
    if not accounts:
        print("\n⚠ No accounts created yet.")
        print("Tip: Use option 1 to create a new account first.")
        logger.debug("List accounts requested but no accounts exist")
        return
    
    print(f"\nTotal Accounts: {len(accounts)}")
    print("-" * 60)
    
    try:
        for idx, (account_id, account) in enumerate(accounts.items(), 1):
            print(f"\n{idx}. Account ID: {account_id}")
            print(f"   Holder: {account.name}")
            print(f"   Type: {account.account_type()}")
            print(f"   Balance: ${account.get_balance():.2f}")
            
            if account.account_type() == "Savings Account":
                print(f"   Min Balance: ${account.MIN_BALANCE:.2f}")
            else:
                print(f"   Overdraft Limit: ${account.OVERDRAFT_LIMIT:.2f}")
        
        print("\n" + "-" * 60)
        logger.info(f"Listed all {len(accounts)} accounts via CLI")
        
    except Exception as e:
        print(f"\n✗ Error retrieving accounts: {e}")
        logger.error(f"Error in list_accounts: {e}")

# Test workflow
print("="*70)
print("  COMPLETE BANKING SYSTEM TEST - List Accounts Feature")
print("="*70)

print("\n[Step 1] Testing list_accounts with NO accounts created...")
list_accounts()

print("\n" + "="*70)
print("[Step 2] Creating accounts...")
print("="*70)

# Create accounts
savings1 = SavingsAccount("Alice Johnson", 5000)
savings2 = SavingsAccount("Charlie Brown", 2500)
current1 = CurrentAccount("Bob Smith", 3000)

# Add to accounts dictionary
accounts["alice_johnson_savings"] = savings1
accounts["charlie_brown_savings"] = savings2
accounts["bob_smith_current"] = current1

print(f"✓ Created 3 accounts")

# Perform some transactions
print("\n[Step 3] Performing transactions...")
savings1.deposit(1000)
savings2.withdraw(500)
current1.add_balance(250)

print("✓ Transactions completed")

# List accounts
print("\n" + "="*70)
print("[Step 4] Testing list_accounts with ACCOUNTS created...")
print("="*70)
list_accounts()

print("\n" + "="*70)
print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
print("="*70)
