import sqlite3
import hashlib

class DatabaseManager:
    class DatabaseManager:
        def __init__(self, db_name="bank_system.db"):
            # This allows multiple 'threads' (web requests) to use one connection
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.create_tables()

    def create_tables(self):
        """Creates the necessary tables for accounts and transactions."""
        cursor = self.conn.cursor()
        # The 'password' column stores the SHA-256 hash, not the plain text.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY,
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
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES accounts (username)
            )
        ''')
        self.conn.commit()

    def _hash_password(self, password):
        """
        Converts a plain-text password into a secure 64-character hash.
        The underscore indicates this is an internal 'helper' method.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self, name, password, acc_type, balance):
        """Hashes the password and inserts a new user record."""
        cursor = self.conn.cursor()
        hashed_pw = self._hash_password(password)
        try:
            cursor.execute('''
                INSERT INTO accounts (username, password, acc_type, balance)
                VALUES (?, ?, ?, ?)
            ''', (name, hashed_pw, acc_type, balance))
            self.conn.commit()
            print(f"\n[✔] Account for {name} created successfully!")
        except sqlite3.IntegrityError:
            print(f"\n[!] Error: Username '{name}' already exists.")

    def verify_login(self, name, password):
        """
        Hashes the provided password and checks it against the database.
        Returns account data if successful, None otherwise.
        """
        cursor = self.conn.cursor()
        hashed_pw = self._hash_password(password)
        cursor.execute('''
            SELECT acc_type, balance FROM accounts 
            WHERE username = ? AND password = ?
        ''', (name, hashed_pw))
        return cursor.fetchone()

    def update_balance(self, name, balance):
        """Updates the balance column for a specific user."""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE accounts SET balance = ? WHERE username = ?', (balance, name))
        self.conn.commit()

    def add_transaction(self, name, action, amount):
        """Records a new entry in the transaction history table."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (username, description, amount)
            VALUES (?, ?, ?)
        ''', (name, action, amount))
        self.conn.commit()

    def fetch_history(self, name):
        """Retrieves all transaction records for a specific user."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT timestamp, description, amount FROM transactions 
            WHERE username = ? ORDER BY timestamp DESC
        ''', (name,))
        return cursor.fetchall()

    def fetch_user(self, name):
        """Basic lookup to see if a user exists (without password check)."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT acc_type, balance FROM accounts WHERE username = ?", (name,))
        return cursor.fetchone()

# Initialize the global instance to be used by base_account.py
db = DatabaseManager()