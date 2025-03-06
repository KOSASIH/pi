import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EconomicModel:
    def __init__(self, initial_supply=100000000000, peg_value=314159):
        self.total_supply = initial_supply  # Total supply of Pi Coin
        self.peg_value = peg_value            # Pegged value in USD
        self.current_price = peg_value         # Current market price
        self.demand = 0                        # Current demand for Pi Coin
        self.incentives = []                   # List to hold incentive structures

    def update_demand(self, new_demand):
        """Update the current demand for Pi Coin."""
        self.demand = new_demand
        logging.info(f"Demand updated to: {self.demand}")

    def adjust_supply(self):
        """Adjust the supply of Pi Coin based on demand and current price."""
        if self.demand > self.total_supply:
            # Increase supply if demand exceeds total supply
            adjustment = self.demand * 0.1  # Increase supply by 10% of demand
            self.total_supply += adjustment
            logging.info(f"Increasing supply by {adjustment:.2f}. New total supply: {self.total_supply:.2f}")
        elif self.demand < self.total_supply * 0.5:
            # Decrease supply if demand is less than 50% of total supply
            adjustment = self.total_supply * 0.1  # Decrease supply by 10%
            self.total_supply -= adjustment
            logging.info(f"Decreasing supply by {adjustment:.2f}. New total supply: {self.total_supply:.2f}")

    def stabilize_price(self):
        """Stabilize the price of Pi Coin based on market conditions."""
        if self.current_price < self.peg_value * 0.95:
            # If price drops below 95% of peg, increase supply
            self.adjust_supply()
            logging.info("Price is below peg value. Adjusting supply to stabilize price.")
        elif self.current_price > self.peg_value * 1.05:
            # If price rises above 105% of peg, consider decreasing supply
            self.adjust_supply()
            logging.info("Price is above peg value. Adjusting supply to stabilize price.")

    def add_incentive(self, incentive):
        """Add an incentive structure for users or merchants."""
        self.incentives.append(incentive)
        logging.info(f"Incentive added: {incentive}")

    def apply_incentives(self):
        """Apply incentives to encourage usage of Pi Coin."""
        for incentive in self.incentives:
            logging.info(f"Applying incentive: {incentive}")

    def get_economic_summary(self):
        """Get a summary of the current economic model state."""
        return {
            "Total Supply": self.total_supply,
            "Current Price": self.current_price,
            "Demand": self.demand,
            "Peg Value": self.peg_value,
            "Incentives": self.incentives
        }

if __name__ == "__main__":
    # Example usage
    economic_model = EconomicModel()

    # Simulate demand updates
    economic_model.update_demand(120000000000)  # Example demand
    economic_model.stabilize_price()             # Adjust supply based on price
    economic_model.add_incentive("5% discount for early adopters")
    economic_model.apply_incentives()

    # Print economic summary
    summary = economic_model.get_economic_summary()
    print("Economic Model Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")
