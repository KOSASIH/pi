import random

class PiCoinMarket:
    def __init__(self, initial_supply, peg_value):
        self.supply = initial_supply
        self.peg_value = peg_value
        self.current_price = peg_value

    def simulate_market(self):
        # Simulate market fluctuations
        self.current_price += random.uniform(-1000, 1000)  # Simulate price changes

        # Adjust supply based on price
        if self.current_price < self.peg_value * 0.95:  # If price drops below 95% of peg
            self.increase_supply()
        elif self.current_price > self.peg_value * 1.05:  # If price rises above 105% of peg
            self.decrease_supply()

    def increase_supply(self):
        adjustment = self.supply * 0.01  # Increase supply by 1%
        self.supply += adjustment
        print(f"Increasing supply by {adjustment}. New supply: {self.supply}")

    def decrease_supply(self):
        adjustment = self.supply * 0.01  # Decrease supply by 1%
        self.supply -= adjustment
        print(f"Decreasing supply by {adjustment}. New supply: {self.supply}")

if __name__ == "__main__":
    market = PiCoinMarket(initial_supply=1000000, peg_value=314159)
    for _ in range(10):  # Simulate 10 market fluctuations
        market.simulate_market()
