import sys
from models.base_account import BankAccount

def main():
    print("=== SECURE PYTHON BANKING SYSTEM ===")
    name = input("Enter Username: ").strip().capitalize()
    password = input("Enter Password: ")
    
    # Attempt to load existing user
    account = BankAccount.login(name, password)
    
    if account:
        print(f"\n[✔] Access Granted. Welcome back, {name}!")
    else:
        print("\n[!] Login failed or User does not exist.")
        choice = input("Would you like to create a new account? (y/n): ")
        if choice.lower() == 'y':
            new_pw = input("Create a Secure Password: ")
            print("1. Savings Account | 2. Current Account")
            type_choice = input("Select Type: ")
            
            try:
                balance = float(input("Initial Deposit: $"))
                acc_type = "Savings Account" if type_choice == "1" else "Current Account"
                
                # Import db here to register the new user
                from models.db_manager import db
                db.create_account(name, new_pw, acc_type, balance)
                
                # Log them in automatically after creation
                account = BankAccount.login(name, new_pw)
            except ValueError:
                print("[!] Invalid amount entered. Restarting...")
                return
        else:
            print("Goodbye!")
            return

    # --- The Menu Loop ---
    while True:
        print(f"\n" + "="*40)
        print(f"ACCOUNT: {account.account_type()} | USER: {account.name}")
        print(f"BALANCE: ${account.get_balance():,.2f}")
        print("="*40)
        print("1. Deposit")
        print("2. Withdraw")
        print("3. View Statement (History)")
        print("4. Logout & Exit")
        
        option = input("\nChoose an option: ")

        try:
            if option == "1":
                amt = float(input("Enter deposit amount: "))
                account.deposit(amt)
            elif option == "2":
                amt = float(input("Enter withdrawal amount: "))
                account.withdraw(amt)
            elif option == "3":
                # Uses the DB-connected history method
                account.show_history()
            elif option == "4":
                print(f"\nSession closed for {account.name}. Goodbye!")
                sys.exit()
            else:
                print("[!] Invalid selection.")
        except ValueError:
            print("[!] Please enter a valid numerical amount.")

if __name__ == "__main__":
    main()