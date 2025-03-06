import uuid
import logging
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MobileApp:
    def __init__(self):
        self.conn = sqlite3.connect('mobile_app.db')
        self.create_tables()

    def create_tables(self):
        """Create tables for users and transactions."""
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
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    sender_id TEXT,
                    receiver_id TEXT,
                    amount REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users (user_id),
                    FOREIGN KEY (receiver_id) REFERENCES users (user_id)
                )
            ''')

    def register_user(self, username, password):
        """Register a new user."""
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        try:
            with self.conn:
                self.conn.execute('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)',
                                  (user_id, username, password))
            logging.info(f"User  registered: {username} with ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError:
            logging.error("Username already exists.")
            return None

    def login(self, username, password):
        """Login a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            logging.info(f"User  {username} logged in successfully.")
            return user[0]  # Return user_id
        else:
            logging.error("Invalid username or password.")
            return None

    def deposit(self, user_id, amount):
        """Deposit Pi Coin into user account."""
        if amount <= 0:
            logging.error("Deposit amount must be greater than zero.")
            return False

        with self.conn:
            self.conn.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        logging.info(f"Deposited {amount:.2f} Pi Coin to user {user_id}.")
        return True

    def send_pi_coin(self, sender_id, receiver_id, amount):
        """Send Pi Coin from one user to another."""
        if amount <= 0:
            logging.error("Transfer amount must be greater than zero.")
            return False

        cursor = self.conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (sender_id,))
        sender_balance = cursor.fetchone()[0]

        if sender_balance < amount:
            logging.error("Insufficient balance.")
            return False

        # Process the transaction
        transaction_id = str(uuid.uuid4())
        with self.conn:
            self.conn.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, sender_id))
            self.conn.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, receiver_id))
            self.conn.execute('INSERT INTO transactions (transaction_id, sender_id, receiver_id, amount) VALUES (?, ?, ?, ?)',
                              (transaction_id, sender_id, receiver_id, amount))
        logging.info(f"Transaction {transaction_id}: {amount:.2f} Pi Coin sent from {sender_id} to {receiver_id}.")
        return transaction_id

    def get_balance(self, user_id):
        """Get the balance of a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        balance = cursor.fetchone()[0]
        logging.info(f"User  ID {user_id} has a balance of {balance:.2f} Pi Coin.")
        return balance

    def get_transaction_history(self, user_id):
        """Get transaction history for a user."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?', (user_id, user_id))
        transactions = cursor.fetchall()
        logging.info(f"Transaction history for user ID {user_id}: {transactions}")
        return transactions

if __name__ == "__main__":
    mobile_app = MobileApp()

    while True:
        print("\nWelcome to the Pi Coin Mobile App")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            mobile_app.register_user(username, password)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = mobile_app.login(username, password)

            if user_id:
                while True:
                    print("\nUser  Menu")
                    print("1. Deposit")
                    print("2. Send Pi Coin")
                    print("3. Check Balance")
                    print("4. Transaction History")
                    print("5. Logout")
                    user_choice = input("Choose an option: ")

                    if user_choice == '1':
                        amount amount = float(input("Enter amount to deposit: "))
                        mobile_app.deposit(user_id, amount)

                    elif user_choice == '2':
                        receiver_id = input("Enter receiver user ID: ")
                        amount = float(input("Enter amount to send: "))
                        transaction_id = mobile_app.send_pi_coin(user_id, receiver_id, amount)
                        if transaction_id:
                            print(f"Transaction successful! ID: {transaction_id}")

                    elif user_choice == '3':
                        balance = mobile_app.get_balance(user_id)
                        print(f"Your balance: {balance:.2f} Pi Coin")

                    elif user_choice == '4':
                        history = mobile_app.get_transaction_history(user_id)
                        print("Transaction History:")
                        for transaction in history:
                            print(transaction)

                    elif user_choice == '5':
                        print("Logging out...")
                        break

                    else:
                        print("Invalid option. Please try again.")

        elif choice == '3':
            print("Exiting the application.")
            break

        else:
            print("Invalid option. Please try again.")
