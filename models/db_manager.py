import sqlite3
import hashlib
import random

class DatabaseManager:
    def __init__(self, db_name="bank_system.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                acc_number TEXT PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                acc_type TEXT,
                balance REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                description TEXT,
                amount REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self, name, password, acc_type, balance):
        cursor = self.conn.cursor()
        hashed_pw = self._hash_password(password)
        acc_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        try:
            cursor.execute('''
                INSERT INTO accounts (acc_number, username, password, acc_type, balance)
                VALUES (?, ?, ?, ?, ?)
            ''', (acc_number, name, hashed_pw, acc_type, balance))
            
            cursor.execute('''
                INSERT INTO transactions (username, description, amount)
                VALUES (?, ?, ?)
            ''', (name, "Initial Deposit", balance))
            
            self.conn.commit()
            return acc_number
        except sqlite3.IntegrityError:
            return None

    def verify_login(self, name, password):
        cursor = self.conn.cursor()
        hashed_pw = self._hash_password(password)
        cursor.execute('SELECT acc_type, balance, acc_number FROM accounts WHERE username = ? AND password = ?', (name, hashed_pw))
        return cursor.fetchone()

    def fetch_all_accounts(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT acc_number, username, acc_type, balance FROM accounts ORDER BY username ASC')
        return cursor.fetchall()

    def fetch_history(self, name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT timestamp, description, amount FROM transactions WHERE username = ? ORDER BY timestamp DESC', (name,))
        return cursor.fetchall()

    def transfer_funds(self, sender_name, receiver_acc_num, amount):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT username FROM accounts WHERE acc_number = ?", (receiver_acc_num,))
            receiver_data = cursor.fetchone()
            if not receiver_data: return False, "Receiver not found."
            
            receiver_name = receiver_data[0]
            if receiver_name == sender_name: return False, "Cannot transfer to self."
            
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (sender_name,))
            if cursor.fetchone()[0] < amount: return False, "Insufficient funds."

            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE username = ?", (amount, sender_name))
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_number = ?", (amount, receiver_acc_num))
            
            cursor.execute("INSERT INTO transactions (username, description, amount) VALUES (?, ?, ?)", (sender_name, f"To {receiver_name} ({receiver_acc_num})", -amount))
            cursor.execute("INSERT INTO transactions (username, description, amount) VALUES (?, ?, ?)", (receiver_name, f"From {sender_name}", amount))
            
            self.conn.commit()
            return True, "Transfer Successful!"
        except Exception as e:
            self.conn.rollback()
            return False, f"Error: {e}"

    def update_balance(self, name, balance):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE accounts SET balance = ? WHERE username = ?', (balance, name))
        self.conn.commit()

    def add_transaction(self, name, action, amount):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO transactions (username, description, amount) VALUES (?, ?, ?)', (name, action, amount))
        self.conn.commit()

db = DatabaseManager()