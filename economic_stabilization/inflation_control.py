import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InflationControl:
    def __init__(self, economic_model):
        self.economic_model = economic_model  # Reference to the economic model
        self.inflation_rate = 0.0              # Current inflation rate

    def monitor_inflation(self):
        """Monitor inflation rates and adjust supply accordingly."""
        self.inflation_rate = self.calculate_inflation_rate()
        logging.info(f"Current inflation rate: {self.inflation_rate:.2f}%")

        if self.inflation_rate > 2.0:  # Example threshold for inflation
            self.adjust_supply(-0.05)  # Decrease supply by 5%
            logging.info("Inflation detected. Adjusting supply downwards.")
        elif self.inflation_rate < 1.0:  # Example threshold for deflation
            self.adjust_supply(0.05)  # Increase supply by 5%
            logging.info("Deflation detected. Adjusting supply upwards.")

    def calculate_inflation_rate(self):
        """Calculate the current inflation rate based on simulated economic indicators."""
        # Simulate economic indicators affecting inflation
        base_inflation = random.uniform(1.0, 3.0)  # Simulated base inflation rate
        economic_growth = random.uniform(-1.0, 2.0)  # Simulated economic growth rate
        inflation_rate = base_inflation + economic_growth
        return max(0.0, inflation_rate)  # Ensure inflation rate is non-negative

    def adjust_supply(self, adjustment):
        """Adjust the supply of Pi Coin based on the inflation control mechanism."""
        if adjustment < 0:
            logging.info(f"Decreasing supply by {abs(adjustment) * 100:.2f}%")
            self.economic_model.adjust_supply(adjustment)  # Call to economic model to adjust supply
        elif adjustment > 0:
            logging.info(f"Increasing supply by {adjustment * 100:.2f}%")
            self.economic_model.adjust_supply(adjustment)  # Call to economic model to adjust supply

if __name__ == "__main__":
    class EconomicModel:
        """A simple economic model for demonstration purposes."""
        def __init__(self):
            self.total_supply = 1000000000  # Initial total supply of Pi Coin

        def adjust_supply(self, adjustment):
            """Adjust the total supply of Pi Coin."""
            self.total_supply += self.total_supply * adjustment
            logging.info(f"New total supply: {self.total_supply:.2f} Pi Coin")

    # Example usage
    economic_model = EconomicModel()
    inflation_control = InflationControl(economic_model)

    # Simulate monitoring inflation over time
    for _ in range(10):  # Simulate 10 time periods
        inflation_control.monitor_inflation()
