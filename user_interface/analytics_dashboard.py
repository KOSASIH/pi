# analytics_dashboard.py

import sqlite3
import logging
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnalyticsDashboard:
    def __init__(self):
        self.conn = sqlite3.connect('user_data.db')
        self.create_tables()

    def create_tables(self):
        """Create tables for storing user data."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS staking (
                    user_id TEXT,
                    amount REAL,
                    start_date TEXT,
                    end_date TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    user_id TEXT,
                    transaction_id TEXT,
                    amount REAL,
                    transaction_type TEXT,
                    timestamp TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS governance (
                    user_id TEXT,
                    proposal_id TEXT,
                    voted INTEGER,
                    timestamp TEXT
                )
            ''')
        logging.info("User  data tables created.")

    def add_staking_data(self, user_id, amount, start_date, end_date):
        """Add staking data for a user."""
        with self.conn:
            self.conn.execute('INSERT INTO staking (user_id, amount, start_date, end_date) VALUES (?, ?, ?, ?)',
                              (user_id, amount, start_date, end_date))
        logging.info(f"Staking data added for user {user_id}: {amount} from {start_date} to {end_date}")

    def add_transaction_data(self, user_id, transaction_id, amount, transaction_type, timestamp):
        """Add transaction data for a user."""
        with self.conn:
            self.conn.execute('INSERT INTO transactions (user_id, transaction_id, amount, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?)',
                              (user_id, transaction_id, amount, transaction_type, timestamp))
        logging.info(f"Transaction data added for user {user_id}: {transaction_id}, Amount: {amount}, Type: {transaction_type}")

    def add_governance_data(self, user_id, proposal_id, voted, timestamp):
        """Add governance participation data for a user."""
        with self.conn:
            self.conn.execute('INSERT INTO governance (user_id, proposal_id, voted, timestamp) VALUES (?, ?, ?, ?)',
                              (user_id, proposal_id, voted, timestamp))
        logging.info(f"Governance data added for user {user_id}: Proposal {proposal_id}, Voted: {voted}")

    def get_staking_performance(self, user_id):
        """Get staking performance metrics for a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT SUM(amount), COUNT(*) FROM staking WHERE user_id = ?', (user_id,))
        total_staked, staking_count = cursor.fetchone()
        return total_staked or 0, staking_count or 0

    def get_transaction_history(self, user_id):
        """Get transaction history for a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT transaction_id, amount, transaction_type, timestamp FROM transactions WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

    def get_governance_participation(self, user_id):
        """Get governance participation metrics for a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM governance WHERE user_id = ? AND voted = 1', (user_id,))
        votes_cast = cursor.fetchone()[0]
        return votes_cast

    def visualize_staking_performance(self, user_id):
        """Visualize staking performance for a user."""
        total_staked, staking_count = self.get_staking_performance(user_id)
        plt.figure(figsize=(10, 5))
        plt.bar(['Total Staked', 'Staking Count'], [total_staked, staking_count], color=['blue', 'green'])
        plt.title(f'Staking Performance for User {user_id}')
        plt.ylabel('Amount / Count')
        plt.show()

    def visualize_transaction_history(self, user_id):
        """Visualize transaction history for a user."""
        transactions = self.get_transaction_history(user_id)
        if transactions:
            transaction_ids, amounts, transaction_types, timestamps = zip(*transactions)
            plt.figure(figsize=(10, 5))
            plt.bar(transaction_ids, amounts, color='orange')
            plt.title(f'Transaction History for User {user_id}')
            plt.xlabel('Transaction ID')
            plt.ylabel('Amount')
            plt.xticks(rotation=45)
            plt.show()
        else:
            logging.info(f"No transactions found for user {user_id}.")

    def visualize_governance_participation(self, user_id):
        """Visualize governance participation for a user."""
        votes_cast = self.get_governance_participation(user_id)
        plt.figure(figsize=(5, 5))
        plt.pie([votes_cast, 1 - votes_cast], labels=['Votes Cast', 'Votes Not Cast'], autopct='%1.1f%%', startangle=90)
        plt.title(f'Governance Participation for User {user_id}')
        plt.show()

if __name__ == "__main__":
    # Example usage
    dashboard = AnalyticsDashboard()

    # Simulate adding user data
    dashboard.add_staking_data("user123", 1000, "2023-01-01", "2023-12-31")
    dashboard.add_transaction_data("user123", "tx001", 150, "stake", "2023-01-05")
    dashboard.add_governance_data("user123", "proposal_001", 1, "2023-01-10")

    # Visualize user data
    dashboard.visualize_staking_performance("user123")
    dashboard.visualize_transaction_history("user123")
    dashboard.visualize_governance_participation("user123")
