"""Interactive Banking System CLI - Terminal-based Interface (Version 2)."""

from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount
from logger import get_logger

logger = get_logger()

# Global account storage
accounts = {}


def display_menu():
    """Display main menu."""
    print("\n" + "="*60)
    print("    BANKING SYSTEM - INTERACTIVE TERMINAL")
    print("="*60)
    print("\n1. Create New Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Add Balance (Interest/Bonus)")
    print("5. Check Balance")
    print("6. View Transaction History")
    print("7. Save Account Data")
    print("8. List All Accounts")
    print("9. Exit")
    print("-"*60)


def create_account():
    """Create a new bank account."""
    print("\n--- Create New Account ---")
    
    name = input("Enter account holder name: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        logger.warning("Account creation failed: Empty name")
        return
    
    account_type = input("Account type (1=Savings, 2=Current): ").strip()
    
    try:
        initial_balance = float(input("Enter initial balance: $"))
        
        if account_type == "1":
            account = SavingsAccount(name, initial_balance)
            account_id = f"{name.replace(' ', '_')}_savings"
        elif account_type == "2":
            account = CurrentAccount(name, initial_balance)
            account_id = f"{name.replace(' ', '_')}_current"
        else:
            print("Error: Invalid account type!")
            logger.warning(f"Account creation failed: Invalid type {account_type}")
            return
        
        accounts[account_id] = account
        print(f"\n✓ Account created successfully!")
        print(f"  Account ID: {account_id}")
        print(f"  Name: {name}")
        print(f"  Type: {account.account_type()}")
        print(f"  Balance: ${account.get_balance():.2f}")
        logger.info(f"New account created via CLI: {account_id}")
        
    except ValueError:
        print("Error: Invalid balance amount!")
        logger.warning("Account creation failed: Invalid balance input")


def deposit_money():
    """Deposit money into an account."""
    print("\n--- Deposit Money ---")
    
    account_id = select_account()
    if not account_id:
        return
    
    try:
        amount = float(input(f"Enter deposit amount: $"))
        
        if amount <= 0:
            print("Error: Amount must be positive!")
            logger.warning(f"Deposit failed for {account_id}: Invalid amount")
            return
        
        account = accounts[account_id]
        result = account.deposit(amount)
        
        if result:
            print(f"\n✓ Deposit successful!")
            print(f"  Amount: ${amount:.2f}")
            print(f"  New Balance: ${account.get_balance():.2f}")
            logger.info(f"Deposit via CLI - Account: {account_id}, Amount: ${amount:.2f}")
        else:
            print("\n✗ Deposit failed!")
            logger.warning(f"Deposit failed for {account_id}")
            
    except ValueError:
        print("Error: Invalid amount!")
        logger.warning(f"Deposit failed for {account_id}: Invalid input")


def withdraw_money():
    """Withdraw money from an account."""
    print("\n--- Withdraw Money ---")
    
    account_id = select_account()
    if not account_id:
        return
    
    try:
        amount = float(input(f"Enter withdrawal amount: $"))
        
        if amount <= 0:
            print("Error: Amount must be positive!")
            logger.warning(f"Withdrawal failed for {account_id}: Invalid amount")
            return
        
        account = accounts[account_id]
        result = account.withdraw(amount)
        
        if result:
            print(f"\n✓ Withdrawal successful!")
            print(f"  Amount: ${amount:.2f}")
            print(f"  New Balance: ${account.get_balance():.2f}")
            logger.info(f"Withdrawal via CLI - Account: {account_id}, Amount: ${amount:.2f}")
        else:
            print("\n✗ Withdrawal failed!")
            logger.warning(f"Withdrawal failed for {account_id}")
            
    except ValueError:
        print("Error: Invalid amount!")
        logger.warning(f"Withdrawal failed for {account_id}: Invalid input")


def add_balance():
    """Add balance to an account (interest/bonus)."""
    print("\n--- Add Balance ---")
    
    account_id = select_account()
    if not account_id:
        return
    
    try:
        amount = float(input(f"Enter amount to add: $"))
        
        if amount <= 0:
            print("Error: Amount must be positive!")
            logger.warning(f"Balance addition failed for {account_id}: Invalid amount")
            return
        
        account = accounts[account_id]
        result = account.add_balance(amount)
        
        if result:
            print(f"\n✓ Balance added successfully!")
            print(f"  Amount Added: ${amount:.2f}")
            print(f"  New Balance: ${account.get_balance():.2f}")
            logger.info(f"Balance addition via CLI - Account: {account_id}, Amount: ${amount:.2f}")
        else:
            print("\n✗ Balance addition failed!")
            logger.warning(f"Balance addition failed for {account_id}")
            
    except ValueError:
        print("Error: Invalid amount!")
        logger.warning(f"Balance addition failed for {account_id}: Invalid input")


def check_balance():
    """Check account balance."""
    print("\n--- Check Balance ---")
    
    account_id = select_account()
    if not account_id:
        return
    
    account = accounts[account_id]
    print(f"\nAccount: {account_id}")
    print(f"Holder: {account.name}")
    print(f"Type: {account.account_type()}")
    print(f"Balance: ${account.get_balance():.2f}")
    
    if account.get_balance() < 0:
        print(f"⚠ Warning: Negative balance (Overdraft in use)")
    
    logger.debug(f"Balance check via CLI - Account: {account_id}")


def view_history():
    """View transaction history."""
    print("\n--- Transaction History ---")
    
    account_id = select_account()
    if not account_id:
        return
    
    account = accounts[account_id]
    print(f"\nTransaction History for {account_id}:")
    print("-" * 60)
    
    if account._history:
        for i, transaction in enumerate(account._history, 1):
            print(f"{i}. {transaction}")
    else:
        print("No transactions found.")
    
    logger.debug(f"History view via CLI - Account: {account_id}")


def save_data():
    """Save account data to file."""
    print("\n--- Save Account Data ---")
    
    if not accounts:
        print("No accounts to save!")
        return
    
    save_all = input("Save all accounts? (y/n): ").strip().lower()
    
    if save_all == "y":
        for account_id, account in accounts.items():
            account.save_to_file()
        print(f"\n✓ All {len(accounts)} account(s) saved successfully!")
        logger.info(f"All {len(accounts)} accounts saved via CLI")
    else:
        account_id = select_account()
        if not account_id:
            return
        
        account = accounts[account_id]
        if account.save_to_file():
            print(f"\n✓ {account_id} saved successfully!")
            logger.info(f"Account {account_id} saved via CLI")
        else:
            print("\n✗ Failed to save account!")
            logger.warning(f"Failed to save {account_id}")


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


def select_account():
    """Select an account from the list."""
    if not accounts:
        print("No accounts available!")
        return None
    
    print("\nAvailable Accounts:")
    account_list = list(accounts.keys())
    
    for i, account_id in enumerate(account_list, 1):
        account = accounts[account_id]
        print(f"{i}. {account_id} (${account.get_balance():.2f})")
    
    try:
        choice = int(input("Select account (number): ")) - 1
        
        if 0 <= choice < len(account_list):
            return account_list[choice]
        else:
            print("Invalid selection!")
            logger.warning("Invalid account selection")
            return None
            
    except ValueError:
        print("Invalid input!")
        logger.warning("Invalid account selection input")
        return None


def main():
    """Main interactive loop."""
    logger.info("=== Interactive Banking CLI Started ===")
    print("\n" + "="*60)
    print("  WELCOME TO INTERACTIVE BANKING SYSTEM")
    print("="*60)
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == "1":
            create_account()
        elif choice == "2":
            deposit_money()
        elif choice == "3":
            withdraw_money()
        elif choice == "4":
            add_balance()
        elif choice == "5":
            check_balance()
        elif choice == "6":
            view_history()
        elif choice == "7":
            save_data()
        elif choice == "8":
            list_accounts()
        elif choice == "9":
            print("\nThank you for using Banking System!")
            logger.info("=== Interactive Banking CLI Closed ===")
            break
        else:
            print("Invalid choice! Please try again.")
            logger.warning(f"Invalid menu choice: {choice}")


if __name__ == "__main__":
    main()
