"""Demo of the interactive banking system."""

from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount

print('='*60)
print('  INTERACTIVE BANKING CLI - DEMO')
print('='*60 + '\n')

print('1. Creating accounts...')
savings = SavingsAccount('Alice', 2000)
current = CurrentAccount('Bob', 1500)
print('✓ Accounts created\n')

print('2. Performing deposit...')
savings.deposit(300)
print()

print('3. Performing withdrawal...')
savings.withdraw(150)
print()

print('4. Adding balance (interest)...')
savings.add_balance(25)
print()

print('5. Checking final balances...')
print(f'Alice Balance: ${savings.get_balance():.2f}')
print(f'Bob Balance: ${current.get_balance():.2f}')

print('\n' + '='*60)
print('  To use the INTERACTIVE terminal interface, run:')
print('  python interactive_banking.py')
print('='*60)
