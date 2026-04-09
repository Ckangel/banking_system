# 🏦 Secure Python Banking System (GUI)

A robust, Object-Oriented banking application featuring a Streamlit web interface, SQLite persistence, and SHA-256 password security. This project demonstrates advanced Python concepts including Abstraction, Inheritance, and Multi-threaded Database management.

## 🚀 Key Features

- **Modern GUI:** Interactive web interface powered by Streamlit.
- **Secure Authentication:** User login system with SHA-256 password hashing.
- **Persistent Storage:** Full transaction history and account balances stored in SQLite.
- **OOP Architecture:** Uses abstract base classes to handle unique logic for Savings and Current accounts.
- **Real-time Analytics:** Visual financial overview with dynamic bar charts.

---

## 📂 Project Structure

```text
banking_system/
├── app.py                # Main Streamlit GUI Entry Point
├── main.py               # Terminal/CLI Version Entry Point
├── bank_system.db        # SQLite Database (Auto-generated)
├── models/               # Business Logic Layer
│   ├── __init__.py
│   ├── base_account.py   # Abstract Base Class (Encapsulation/Logic)
│   ├── savings_account.py# Savings Logic (Min Balance rules)
│   ├── current_account.py# Current Logic (Overdraft rules)
│   └── db_manager.py     # SQL Persistence Layer
└── requirements.txt      # Project Dependencies
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Frontend:** Streamlit
- **Database:** SQLite3
- **Security:** Hashlib (SHA-256)

---

## ⚙️ Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/ckangel/banking-system.git](https://github.com//banking-system.git)
   cd banking-system
   ```

2. **Install Dependencies:**

   ```bash
   pip install streamlit
   ```

3. **Run the Application:**
   To launch the Web GUI:

   ```bash
   python -m streamlit run app.py
   ```

   *To run the legacy Terminal version:* `python main.py`

---

## 🛡️ Security Implementation

This system does not store plain-text passwords. Every password is "salted" and hashed using the SHA-256 algorithm. When a user logs in, their input is hashed and compared against the stored hash in the database, ensuring that even if the database is compromised, user credentials remain secure.

---

## 📊 Account Logic

- **Savings Account:** Enforces a minimum balance of $500. Withdrawals that drop below this limit are automatically denied.
- **Current Account:** Features a $1,000 overdraft protection, allowing users to spend slightly beyond their current balance.
