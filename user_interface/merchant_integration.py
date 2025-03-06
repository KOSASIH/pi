import uuid
import logging
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MerchantIntegration:
    def __init__(self):
        self.conn = sqlite3.connect('merchant_integration.db')
        self.create_tables()

    def create_tables(self):
        """Create tables for merchants and transactions."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS merchants (
                    merchant_id TEXT PRIMARY KEY,
                    name TEXT UNIQUE,
                    password TEXT,
                    balance REAL DEFAULT 0.0
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS merchant_transactions (
                    transaction_id TEXT PRIMARY KEY,
                    merchant_id TEXT,
                    amount REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (merchant_id) REFERENCES merchants (merchant_id)
                )
            ''')

    def register_merchant(self, name, password):
        """Register a new merchant."""
        merchant_id = str(uuid.uuid4())  # Generate a unique merchant ID
        try:
            with self.conn:
                self.conn.execute('INSERT INTO merchants (merchant_id, name, password) VALUES (?, ?, ?)',
                                  (merchant_id, name, password))
            logging.info(f"Merchant registered: {name} with ID: {merchant_id}")
            return merchant_id
        except sqlite3.IntegrityError:
            logging.error("Merchant name already exists.")
            return None

    def login(self, name, password):
        """Login a merchant."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT merchant_id FROM merchants WHERE name = ? AND password = ?', (name, password))
        merchant = cursor.fetchone()
        if merchant:
            logging.info(f"Merchant {name} logged in successfully.")
            return merchant[0]  # Return merchant_id
        else:
            logging.error("Invalid merchant name or password.")
            return None

    def process_payment(self, merchant_id, amount):
        """Process a payment for a merchant."""
        if amount <= 0:
            logging.error("Payment amount must be greater than zero.")
            return False

        transaction_id = str(uuid.uuid4())
        with self.conn:
            self.conn.execute('UPDATE merchants SET balance = balance + ? WHERE merchant_id = ?', (amount, merchant_id))
            self.conn.execute('INSERT INTO merchant_transactions (transaction_id, merchant_id, amount) VALUES (?, ?, ?)',
                              (transaction_id, merchant_id, amount))
        logging.info(f"Payment processed: Transaction ID {transaction_id}, Amount {amount:.2f} for Merchant ID {merchant_id}")
        return transaction_id

    def get_merchant_balance(self, merchant_id):
        """Get the balance of a merchant."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT balance FROM merchants WHERE merchant_id = ?', (merchant_id,))
        balance = cursor.fetchone()[0]
        logging.info(f"Merchant ID {merchant_id} has a balance of {balance:.2f} Pi Coin.")
        return balance

    def get_merchant_transaction_history(self, merchant_id):
        """Get transaction history for a merchant."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM merchant_transactions WHERE merchant_id = ?', (merchant_id,))
        transactions = cursor.fetchall()
        logging.info(f"Transaction history for merchant ID {merchant_id}: {transactions}")
        return transactions

if __name__ == "__main__":
    merchant_integration = MerchantIntegration()

    while True:
        print("\nWelcome to the Pi Coin Merchant Integration")
        print("1. Register Merchant")
        print("2. Login Merchant")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter merchant name: ")
            password = input("Enter password: ")
            merchant_integration.register_merchant(name, password)

        elif choice == '2':
            name = input("Enter merchant name: ")
            password = input("Enter password: ")
            merchant_id = merchant_integration.login(name, password)

            if merchant_id:
                while True:
                    print("\nMerchant Menu")
                    print("1. Process Payment")
                    print("2. Check Balance")
                    print("3. Transaction History")
                    print("4. Logout")
                    merchant_choice = input("Choose an option: ")

                    if merchant_choice == '1':
                        amount = float(input("Enter amount to process: "))
                        transaction_id = merchant_integration.process_payment(merchant_id, amount)
                        if transaction_id:
                            print(f"Payment successful! Transaction ID: {transaction_id}")

                    elif merchant_choice == '2':
                        balance = merchant_integration.get_merchant_balance(merchant_id)
                        print(f"Your balance: {balance:.2f} Pi Coin")

                    elif merchant_choice == '3':
                        history = merchant_integration.get_merchant_transaction_history(merchant_id)
                        print("Transaction History:")
                        for transaction in history:
                            print(transaction)

                    elif merchant_choice == '4':
                        print("Logging out...")
                        break

                    else:
                        print("Invalid option. Please try again.")

        elif choice == '3':
            print("Exiting the application.")
            break

        else:
            print("Invalid option. Please try again.")
