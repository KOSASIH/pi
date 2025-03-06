# liquidity_mining.py

import uuid
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LiquidityMining:
    def __init__(self):
        self.liquidity_pool = {}  # Dictionary to hold user liquidity
        self.reward_rate = 0.1  # Reward rate (10% of liquidity per year)

    def add_liquidity(self, user_id, amount):
        """Add liquidity to the pool for a user."""
        if user_id not in self.liquidity_pool:
            self.liquidity_pool[user_id] = {
                'amount': 0,
                'start_time': datetime.now()
            }
        self.liquidity_pool[user_id]['amount'] += amount
        logging.info(f"User  {user_id} added {amount} to liquidity pool. Total: {self.liquidity_pool[user_id]['amount']}")

    def remove_liquidity(self, user_id, amount):
        """Remove liquidity from the pool for a user."""
        if user_id in self.liquidity_pool and self.liquidity_pool[user_id]['amount'] >= amount:
            self.liquidity_pool[user_id]['amount'] -= amount
            logging.info(f"User  {user_id} removed {amount} from liquidity pool. Remaining: {self.liquidity_pool[user_id]['amount']}")
        else:
            logging.error("Insufficient liquidity to remove.")

    def calculate_rewards(self, user_id):
        """Calculate rewards for a user based on their liquidity."""
        if user_id not in self.liquidity_pool:
            logging.error("User  not found in liquidity pool.")
            return 0

        liquidity_info = self.liquidity_pool[user_id]
        amount = liquidity_info['amount']
        duration = (datetime.now() - liquidity_info['start_time']).days / 365  # Duration in years
        rewards = amount * self.reward_rate * duration
        logging.info(f"User  {user_id} has earned {rewards:.2f} in rewards.")
        return rewards

    def distribute_rewards(self, user_id):
        """Distribute rewards to a user."""
        rewards = self.calculate_rewards(user_id)
        if rewards > 0:
            logging.info(f"Distributing {rewards:.2f} rewards to user {user_id}.")
            # Here you would implement the logic to actually distribute the rewards (e.g., transfer tokens)
            # For this example, we will just log it.
        else:
            logging.info(f"No rewards to distribute for user {user_id}.")

if __name__ == "__main__":
    # Example usage
    liquidity_mining = LiquidityMining()

    # Simulate users adding liquidity
    user_id_1 = str(uuid.uuid4())
    user_id_2 = str(uuid.uuid4())

    liquidity_mining.add_liquidity(user_id_1, 1000)
    liquidity_mining.add_liquidity(user_id_2, 2000)

    # Simulate time passing (for demonstration purposes, we will not actually wait)
    # In a real application, you would wait for some time before calculating rewards.

    # Distribute rewards
    liquidity_mining.distribute_rewards(user_id_1)
    liquidity_mining.distribute_rewards(user_id_2)

    # Simulate users removing liquidity
    liquidity_mining.remove_liquidity(user_id_1, 500)
    liquidity_mining.remove_liquidity(user_id_2, 1000)
