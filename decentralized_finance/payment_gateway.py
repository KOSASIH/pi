import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PaymentGateway:
    def __init__(self):
        self.merchants = {}  # Dictionary to hold merchant data
        self.transactions = []  # List to hold transaction records

    def register_merchant(self, merchant_name):
        """Register a new merchant."""
        merchant_id = str(uuid.uuid4())  # Generate a unique merchant ID
        self.merchants[merchant_id] = {
            'name': merchant_name,
            'balance': 0.0  # Initial balance
        }
        logging.info(f"Merchant registered: {merchant_name} with ID: {merchant_id}")
        return merchant_id

    def process_payment(self, merchant_id, amount):
        """Process a payment for a merchant."""
        if merchant_id not in self.merchants:
            logging.error(f"Merchant ID {merchant_id} not found.")
            return False

        if amount <= 0:
            logging.error("Payment amount must be greater than zero.")
            return False

        # Simulate payment processing
        transaction_id = str(uuid.uuid4())
        self.transactions.append({
            'transaction_id': transaction_id,
            'merchant_id': merchant_id,
            'amount': amount
        })

        # Update merchant balance
        self.merchants[merchant_id]['balance'] += amount
        logging.info(f"Payment processed: Transaction ID {transaction_id}, Amount {amount:.2f} for Merchant ID {merchant_id}")
        return transaction_id

    def get_merchant_balance(self, merchant_id):
        """Get the balance of a merchant."""
        if merchant_id not in self.merchants:
            logging.error(f"Merchant ID {merchant_id} not found.")
            return None

        balance = self.merchants[merchant_id]['balance']
        logging.info(f"Merchant ID {merchant_id} has a balance of {balance:.2f}")
        return balance

    def get_transaction_history(self, merchant_id):
        """Get the transaction history for a merchant."""
        if merchant_id not in self.merchants:
            logging.error(f"Merchant ID {merchant_id} not found.")
            return None

        merchant_transactions = [t for t in self.transactions if t['merchant_id'] == merchant_id]
        logging.info(f"Transaction history for Merchant ID {merchant_id}: {merchant_transactions}")
        return merchant_transactions

if __name__ == "__main__":
    # Example usage
    payment_gateway = PaymentGateway()

    # Register a merchant
    merchant_id = payment_gateway.register_merchant("Example Merchant")

    # Process a payment
    transaction_id = payment_gateway.process_payment(merchant_id, 100.0)

    # Get merchant balance
    balance = payment_gateway.get_merchant_balance(merchant_id)

    # Get transaction history
    transactions = payment_gateway.get_transaction_history(merchant_id)

    # Print results
    print(f"Merchant Balance: {balance:.2f}")
    print(f"Transaction ID: {transaction_id}")
    print(f"Transaction History: {transactions}")
