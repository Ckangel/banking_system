import sqlite3
import hashlib

class DatabaseManager:
    def __init__(self, db_name="bank_system.db"):
        # We define self.conn first to prevent AttributeErrors
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
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
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self, name, password, acc_type, balance):
        cursor = self.conn.cursor()
        hashed_pw = self._hash_password(password)
        try:
            cursor.execute('''
                INSERT INTO accounts (username, password, acc_type, balance)
                VALUES (?, ?, ?, ?)
            ''', (name, hashed_pw, acc_type, balance))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass # User already exists

    def verify_login(self, name, password):
        cursor = self.conn.cursor()
        hashed_pw = self._hash_password(password)
        cursor.execute('''
            SELECT acc_type, balance FROM accounts 
            WHERE username = ? AND password = ?
        ''', (name, hashed_pw))
        return cursor.fetchone()

    def update_balance(self, name, balance):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE accounts SET balance = ? WHERE username = ?', (balance, name))
        self.conn.commit()

    def add_transaction(self, name, action, amount):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (username, description, amount)
            VALUES (?, ?, ?)
        ''', (name, action, amount))
        self.conn.commit()

    def fetch_history(self, name):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT timestamp, description, amount FROM transactions 
            WHERE username = ? ORDER BY timestamp DESC
        ''', (name,))
        return cursor.fetchall()

# Initialize the global instance
db = DatabaseManager()