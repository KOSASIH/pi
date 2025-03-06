# dynamic_pricing_model.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DynamicPricingModel:
    def __init__(self, base_price):
        self.base_price = base_price  # Base price of Pi Coin
        self.current_price = base_price  # Initialize current price

    def calculate_price(self, demand, supply, volatility=1.0):
        """Calculate the dynamic price based on demand and supply."""
        if supply <= 0:
            logging.error("Supply must be greater than zero to calculate price.")
            return None

        # Example dynamic pricing formula
        price = self.base_price * (demand / supply) * volatility
        
        # Ensure price does not fall below a minimum threshold
        self.current_price = max(price, self.base_price * 0.5)  # Minimum price is 50% of base price
        logging.info(f"Calculated price: {self.current_price:.2f} Pi Coin (Demand: {demand}, Supply: {supply}, Volatility: {volatility})")
        return self.current_price

    def simulate_price_changes(self, demand_changes, supply_changes):
        """Simulate price changes over a series of demand and supply changes."""
        for demand, supply in zip(demand_changes, supply_changes):
            self.calculate_price(demand, supply)
            print(f"New Price: {self.current_price:.2f} Pi Coin")

if __name__ == "__main__":
    # Example usage
    pricing_model = DynamicPricingModel(base_price=1.0)

    # Simulate market conditions
    demand_changes = [1200, 800, 1000, 1500]  # Example demand values
    supply_changes = [1000, 1000, 800, 1200]  # Example supply values

    # Simulate price changes
    pricing_model.simulate_price_changes(demand_changes, supply_changes)
