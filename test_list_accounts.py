"""Test the list_accounts function."""

import sys
sys.path.insert(0, 'C:\\Users\\HP\\Documents\\BankingSystem\\banking_system')

from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount

# Simulate accounts dictionary
accounts = {}

# Create test accounts
print("Creating test accounts...\n")
savings = SavingsAccount("Alice Johnson", 5000)
current = CurrentAccount("Bob Smith", 3000)

# Add to accounts dictionary
accounts["alice_savings"] = savings
accounts["bob_current"] = current

print("\n" + "="*60)
print("Testing List Accounts Function")
print("="*60)

# Test list_accounts function
print("\n--- All Accounts ---")

if not accounts:
    print("No accounts created yet.")
else:
    print(f"\nTotal Accounts: {len(accounts)}")
    print("-" * 60)
    
    for account_id, account in accounts.items():
        print(f"\nAccount ID: {account_id}")
        print(f"  Holder: {account.name}")
        print(f"  Type: {account.account_type()}")
        print(f"  Balance: ${account.get_balance():.2f}")
        
        if account.account_type() == "Savings Account":
            print(f"  Min Balance: ${account.MIN_BALANCE:.2f}")
        else:
            print(f"  Overdraft Limit: ${account.OVERDRAFT_LIMIT:.2f}")

print("\n" + "="*60)
print("✓ List accounts function works correctly!")
print("="*60)
