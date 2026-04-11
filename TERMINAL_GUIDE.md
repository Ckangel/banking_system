# Interactive Banking System - Terminal Guide

## How to Use the Terminal Interface

### Start the Interactive CLI

```bash
python interactive_banking.py
```

This launches an interactive menu-driven interface where you can input commands and make changes in real-time.

---

## Menu Options

### 1. **Create New Account**

- Input account holder name
- Choose account type (1=Savings, 2=Current)
- Set initial balance
- **Example:**

```bash
Enter account holder name: John Smith
Account type (1=Savings, 2=Current): 1
Enter initial balance: 5000
```

### 2. **Deposit Money**

- Select account
- Enter deposit amount
- **Example:**

```bash
Select account (number): 1
Enter deposit amount: $500
```

### 3. **Withdraw Money**

- Select account
- Enter withdrawal amount
- **Example:**

```bash
Select account (number): 1
Enter withdrawal amount: $200
```

### 4. **Add Balance** (Interest/Bonus)

- Select account
- Enter amount to add
- **Example:**

```bash
Select account (number): 1
Enter amount to add: $50
```

### 5. **Check Balance**

- Select account
- View current balance and details
- **Example:**

```bash
Select account (number): 1

Account: john_smith_savings
Holder: John Smith
Type: Savings Account
Balance: $5350.00
```

### 6. **View Transaction History**

- Select account
- See all transaction record
- **Example:**

```bash
Select account (number): 1

Transaction History for john_smith_savings:
1. 2026-04-02 09:44:42 | Account Created: $5,000.00 | Balance: $5,000.00
2. 2026-04-02 09:44:42 | Deposit: $500.00 | Balance: $5,500.00
3. 2026-04-02 09:44:42 | Balance Addition: $50.00 | Balance: $5,550.00
```

### 7. **Save Account Data**

- Save single account or all accounts
- Creates `{AccountName}_data.txt` files
- **Example:**

```bash
Save all accounts? (y/n): y
✓ All 2 account(s) saved successfully!
```

### 8. **List All Accounts**

- View all created accounts at a glance
- Shows account IDs, holders, types, and balances
- **Example:**

```bash
Total Accounts: 2

Account ID: john_smith_savings
  Holder: John Smith
  Type: Savings Account
  Balance: $5350.00
  Min Balance: $500.00

Account ID: jane_doe_current
  Holder: Jane Doe
  Type: Current Account
  Balance: $2500.00
  Overdraft Limit: $1000.00
```

### 9. **Exit**

- Close the program

---

## Quick Start Example

```bash
# Step 1: Open terminal and navigate to banking system
cd C:\Users\HP\Documents\BankingSystem\banking_system

# Step 2: Run the interactive program
python interactive_banking.py

# Step 3: Follow the menu prompts
# Menu will appear asking you to choose an option (1-9)
```

---

## Features

- ✅ **Real-time Input**: Type commands and values in the terminal
- ✅ **Validation**: All inputs are validated before processing
- ✅ **Logging**: All transactions are logged automatically
- ✅ **Verification**: Data integrity checked for every operation
- ✅ **Account Management**: Create and manage multiple accounts
- ✅ **Transaction History**: Full audit trail of all operations
- ✅ **Data Persistence**: Save account data to files

---

## Terminal Command Examples

### Create an account and do transactions

```text
Choice: 1 → Create account (John, Savings, $1000)
Choice: 2 → Deposit $500
Choice: 5 → Check balance
Choice: 7 → Save data
Choice: 9 → Exit
```

---

## Log Files

All terminal interactions are logged to:

```text
logs/banking_YYYYMMDD_HHMMSS.log
```

Each file contains detailed information about:

- Account creation
- All deposits/withdrawals
- Balance additions
- Validation checks
- Errors and warnings

---

## More Options

| Script | Purpose |
| --- | --- |
| `python interactive_banking.py` | Interactive terminal menu |
| `python main.py` | Run automated tests |
| `python demo.py` | See demo examples |
| `python test_add_balance.py` | Test balance addition feature |
