"""Simulate the exact interactive banking flow to test list_accounts."""

import sys

# Import the interactive banking module
import interactive_banking

print("="*70)
print("  SIMULATING INTERACTIVE BANKING - List Accounts Test")
print("="*70)

# Step 1: Simulate creating an account
print("\n[Step 1] Creating an account...")
print("-" * 70)

# Manually add an account like create_account() would do
from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount

savings = SavingsAccount("John Doe", 5000)
interactive_banking.accounts["john_savings"] = savings

current = CurrentAccount("Jane Smith", 3000)
interactive_banking.accounts["jane_current"] = current

print(f"✓ Added {len(interactive_banking.accounts)} accounts to the global accounts dictionary")
print(f"  Accounts: {list(interactive_banking.accounts.keys())}")

# Step 2: Call list_accounts function
print("\n[Step 2] Calling list_accounts() function...")
print("-" * 70)

# Call the list_accounts function from the module
interactive_banking.list_accounts()

print("\n" + "="*70)
print("✓ TEST COMPLETED")
print("="*70)
