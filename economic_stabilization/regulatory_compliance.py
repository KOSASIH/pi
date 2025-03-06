import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RegulatoryCompliance:
    def __init__(self, config_file='config.json'):
        self.load_config(config_file)

    def load_config(self, config_file):
        """Load configuration from a JSON file."""
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
                self.kyc_api_url = config.get('kyc_api_url')
                self.aml_api_url = config.get('aml_api_url')
                logging.info("Configuration loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            raise

    def check_kyc(self, user_id):
        """Check if the user has completed KYC."""
        try:
            response = requests.get(f"{self.kyc_api_url}/check/{user_id}")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return data.get('kyc_completed', False)
        except requests.RequestException as e:
            logging.error(f"Error checking KYC for user {user_id}: {e}")
            return False

    def check_aml(self, user_id):
        """Check if the user is on any AML watchlists."""
        try:
            response = requests.get(f"{self.aml_api_url}/check/{user_id}")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return data.get('is_flagged', False)
        except requests.RequestException as e:
            logging.error(f"Error checking AML for user {user_id}: {e}")
            return False

    def validate_transaction(self, user_id, transaction_amount):
        """Validate a transaction based on KYC and AML checks."""
        if not self.check_kyc(user_id):
            logging.warning(f"Transaction denied: User {user_id} has not completed KYC.")
            return False

        if self.check_aml(user_id):
            logging.warning(f"Transaction denied: User {user_id} is flagged in AML checks.")
            return False

        # Additional checks can be added here (e.g., transaction limits)
        logging.info(f"Transaction approved for user {user_id} of amount {transaction_amount}.")
        return True

if __name__ == "__main__":
    # Example usage
    compliance_checker = RegulatoryCompliance(config_file='config.json')

    user_id = "user123"  # Example user ID
    transaction_amount = 1000  # Example transaction amount

    if compliance_checker.validate_transaction(user_id, transaction_amount):
        print("Transaction can proceed.")
    else:
        print("Transaction cannot proceed due to compliance issues.")
