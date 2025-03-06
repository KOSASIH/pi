import uuid
import logging
import sqlite3
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserDashboard:
    def __init__(self):
        self.conn = sqlite3.connect('user_dashboard.db')
        self.create_tables()

    def create_tables(self):
        """Create tables for users, stakes, and transactions."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    balance REAL DEFAULT 0.0
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS stakes (
                    stake_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    amount REAL,
                    start_date DATETIME,
                    end_date DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    amount REAL,
                    transaction_type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')

    def register_user(self, username, password, initial_balance):
        """Register a new user with an initial balance."""
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        try:
            with self.conn:
                self.conn.execute('INSERT INTO users (user_id, username, password, balance) VALUES (?, ?, ?, ?)',
                                  (user_id, username, password, initial_balance))
            logging.info(f"User  registered: {username} with ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError:
            logging.error("Username already exists.")
            return None

    def login_user(self, username, password):
        """Login a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id, balance FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            logging.info(f"User  {username} logged in successfully.")
            return user[0], user[1]  # Return user_id and balance
        else:
            logging.error("Invalid username or password.")
            return None, None

    def stake_coins(self, user_id, amount, duration_days):
        """Stake coins for a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        balance = cursor.fetchone()[0]

        if amount <= 0:
            logging.error("Stake amount must be greater than zero.")
            return None

        if balance < amount:
            logging.error("Insufficient balance to stake.")
            return None

        # Create a stake record
        stake_id = str(uuid.uuid4())
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)

        with self.conn:
            self.conn.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
            self.conn.execute('INSERT INTO stakes (stake_id, user_id, amount, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
                              (stake_id, user_id, amount, start_date, end_date))
            self.conn.execute('INSERT INTO transactions (transaction_id, user_id, amount, transaction_type) VALUES (?, ?, ?, ?)',
                              (str(uuid.uuid4()), user_id, -amount, 'stake'))
        logging.info(f"Stake created: ID {stake_id}, Amount {amount:.2f} Pi Coin for user {user_id}.")
        return stake_id

    def unstake_coins(self, user_id, stake_id):
        """Unstake coins and return the amount."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT amount, end_date FROM stakes WHERE stake_id = ?', (stake_id,))
        stake = cursor.fetchone()

        if stake:
            amount, end_date = stake
            if datetime.now() < datetime.fromisoformat(end_date):
                logging.error("Cannot unstake before the end date.")
                return None

            with self.conn:
                self.conn.execute('DELETE FROM stakes WHERE stake_id = ?', (stake_id,))
                self.conn.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
                self.conn.execute('INSERT INTO transactions (transaction_id, user_id, amount, transaction_type) VALUES (?, ?, ?, ?)',
                                  (str(uuid.uuid4()), user_id, amount, 'unstake'))
            logging.info(f"Unstaked: ID {stake_id}, Amount {amount:.2f} Pi Coin returned to user {user_id}.")
            return amount
        else:
            logging.error("Stake ID not found.")
            return None

    def view_transactions(self, user_id):
        """View transaction history for a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
        transactions = cursor.fetchall()
        return transactions

if __name__ == "__main__":
    dashboard = UserDashboard()

    # Example usage
    # Register a user
    user_id = dashboard.register_user("Alice", "password123", 1000.0)

    # Login the user
    logged_in_user_id, balance = dashboard.login_user("Alice", "password123")

    if logged_in_user_id:
        print(f"Logged in as: {logged_in_user_id}, Balance: {balance:.2f} Pi Coin")

        # Stake coins
        stake_id = dashboard.stake_coins(logged_in_user_id, 200.0, 30)  # Stake 200 Pi Coin for 30 days

        # Unstake coins after the staking period
        total_returned = dashboard.unstake_coins(logged_in_user_id, stake_id)  # Unstake coins
        print(f"Total amount returned after unstaking: {total_returned:.2f} Pi Coin")

        # View transaction history
        transactions = dashboard.view_transactions(logged_in_user_id)
        print("Transaction History:")
        for transaction in transactions:
            print(transaction)
