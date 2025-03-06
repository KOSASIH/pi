import uuid
import logging
import sqlite3
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StakingProtocol:
    def __init__(self):
        self.conn = sqlite3.connect('staking_protocol.db')
        self.create_tables()

    def create_tables(self):
        """Create tables for users and staking."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE,
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

    def register_user(self, username, initial_balance):
        """Register a new user with an initial balance."""
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        try:
            with self.conn:
                self.conn.execute('INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)',
                                  (user_id, username, initial_balance))
            logging.info(f"User  registered: {username} with ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError:
            logging.error("Username already exists.")
            return None

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
        logging.info(f"Stake created: ID {stake_id}, Amount {amount:.2f} Pi Coin for user {user_id}.")
        return stake_id

    def calculate_rewards(self, stake_id):
        """Calculate rewards for a given stake."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT amount, start_date, end_date FROM stakes WHERE stake_id = ?', (stake_id,))
        stake = cursor.fetchone()

        if stake:
            amount, start_date, end_date = stake
            duration = (datetime.now() - datetime.fromisoformat(start_date)).days
            # Example reward calculation: 5% per day
            reward_rate = 0.05
            rewards = amount * reward_rate * duration
            logging.info(f"Rewards calculated for stake ID {stake_id}: {rewards:.2f} Pi Coin.")
            return rewards
        else:
            logging.error("Stake ID not found.")
            return 0.0

    def unstake_coins(self, stake_id):
        """Unstake coins and return the amount plus rewards."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id, amount, end_date FROM stakes WHERE stake_id = ?', (stake_id,))
        stake = cursor.fetchone()

        if stake:
            user_id, amount, end_date = stake
            if datetime.now() < datetime.fromisoformat(end_date):
                logging.error("Cannot unstake before the end date.")
                return None

            rewards = self.calculate_rewards(stake_id)
            total_amount = amount + rewards

            with self.conn:
                self.conn.execute('DELETE FROM stakes WHERE stake_id = ?', (stake_id,))
                self.conn.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (total_amount, user_id))
            logging.info(f"Unstaked: ID {stake_id}, Total Amount Returned {total_amount:.2f} Pi Coin to user {user_id}.")
            return total_amount
        else:
            logging.error("Stake ID not found.")
            return None

if __name__ == "__main__":
    staking_protocol = StakingProtocol()

    # Example usage
    user_id = staking_protocol.register_user("Alice", 1000.0)  # Register user with initial balance

    # Stake coins
    stake_id = staking_protocol.stake_coins(user_id, 200.0, 30)  # Stake 200 Pi Coin for 30 days

    # Unstake coins after the staking period
    total_returned = staking_protocol.unstake_coins(stake_id)  # Unstake coins
    print(f"Total amount returned after unstaking: {total_returned:.2f} Pi Coin")
