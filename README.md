# Bank Account Management System (Python OOP)

A robust, terminal-based banking application demonstrating advanced Object-Oriented Programming (OOP) principles, data persistence, and business logic validation.

## Features

• Account Diversity: Supports both Savings and Current accounts with unique financial rules.
• Business Logic Validation: * Savings: Minimum balance enforcement of $500.
o Current: Overdraft protection up to $1,000.
• Automatic Persistence: Saves user data and transaction logs to unique .txt files.
• Secure Session Handling: A login system that restores account states and history upon return.
• Audit Trail: Timestamped logging of every deposit and withdrawal.
________________________________________

## Core OOP Concepts Applied

This project was built to showcase industry-standard coding patterns:
Concept Implementation in this Project
Abstraction Used abc.ABC for the BankAccount base class to ensure generic accounts cannot be instantiated.
Inheritance SavingsAccount and CurrentAccount inherit core logic from the base class to reduce code redundancy.
Encapsulation Protected members (_balance,_history) prevent direct external tampering with financial data.
Polymorphism The withdraw() method is overridden in child classes to apply specific banking rules.
________________________________________

## Project Structure

bank_system/
├── main.py                # App entry point & User Interface logic
├── models/
│   ├── __init__.py
│   ├── base_account.py    # Abstract Base Class & persistence logic
│   ├── savings_account.py # Savings logic & constants
│   └── current_account.py # Current logic & overdraft rules
└── [User]_data.txt        # Generated persistence files
________________________________________

## Installation & Usage

1. Clone the repository:
Bash
git clone <https://github.com/ckangel/bank-system-python.git>
cd bank-system-python
2. Run the application:
Bash
python main.py
3. Follow the prompts: Enter a username to login or create a new account. Your progress is saved automatically upon selecting Save & Exit.

________________________________________

## Future Enhancements (Roadmap)

[ ] Database Integration: Move from .txt files to SQLite for better data handling.
[ ] GUI: Implement a graphical interface using Tkinter or PyQt.
[ ] Transfer Logic: Allow users to transfer funds between different account holders.
[ ] Encryption: Hash passwords and encrypt sensitive file data.
