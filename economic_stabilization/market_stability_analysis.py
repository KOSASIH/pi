import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MarketStabilityAnalysis:
    def __init__(self):
        self.market_data = []  # List to hold market data over time
        self.stability_index = []  # List to hold calculated stability indices

    def add_market_data(self, supply, demand, price, trading_volume):
        """Add market data for analysis."""
        self.market_data.append({
            'supply': supply,
            'demand': demand,
            'price': price,
            'trading_volume': trading_volume
        })
        logging.info(f"Market data added: Supply={supply}, Demand={demand}, Price={price}, Trading Volume={trading_volume}")

    def calculate_stability_index(self):
        """Calculate the market stability index based on current market data."""
        if not self.market_data:
            logging.error("No market data available for stability analysis.")
            return None

        latest_data = self.market_data[-1]
        supply = latest_data['supply']
        demand = latest_data['demand']
        price = latest_data['price']
        trading_volume = latest_data['trading_volume']

        # Example stability index calculation
        stability_index = (demand / supply) * (1 / price) * (trading_volume / 1000)  # Adjusted for scale
        self.stability_index.append(stability_index)
        logging.info(f"Stability index calculated: {stability_index:.4f}")
        return stability_index

    def visualize_stability_index(self):
        """Visualize the stability index over time."""
        if not self.stability_index:
            logging.error("No stability index data available for visualization.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.stability_index, marker='o', linestyle='-', color='b')
        plt.title('Market Stability Index Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Stability Index')
        plt.grid()
        plt.axhline(y=1, color='r', linestyle='--', label='Stable Threshold')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # Example usage
    stability_analysis = MarketStabilityAnalysis()

    # Simulate adding market data over time
    stability_analysis.add_market_data(supply=1000000, demand=800000, price=1.0, trading_volume=50000)
    stability_analysis.calculate_stability_index()

    stability_analysis.add_market_data(supply=1000000, demand=900000, price=1.1, trading_volume=60000)
    stability_analysis.calculate_stability_index()

    stability_analysis.add_market_data(supply=1000000, demand=950000, price=1.2, trading_volume=70000)
    stability_analysis.calculate_stability_index()

    # Visualize the stability index
    stability_analysis.visualize_stability_index()
