import random

class PiCoinMarket:
    def __init__(self, peg_value=314159):
        self.supply = 100000000000  # Fixed supply of 100 billion Pi Coins
        self.peg_value = peg_value
        self.current_price = peg_value
        self.price_history = []

    def simulate_market(self):
        # Simulate market fluctuations
        price_change = random.uniform(-1000, 1000)  # Simulate price changes
        self.current_price += price_change
        self.price_history.append(self.current_price)

        print(f"Current Price: {self.current_price:.2f} (Change: {price_change:.2f})")

        # Adjust supply based on price
        if self.current_price < self.peg_value * 0.95:  # If price drops below 95% of peg
            self.increase_supply()
        elif self.current_price > self.peg_value * 1.05:  # If price rises above 105% of peg
            self.decrease_supply()

    def increase_supply(self):
        adjustment = self.supply * 0.01 * (self.peg_value - self.current_price) / self.peg_value  # Adjust based on deviation
        self.supply += adjustment
        print(f"Increasing supply by {adjustment:.2f}. New supply: {self.supply:.2f}")

    def decrease_supply(self):
        adjustment = self.supply * 0.01 * (self.current_price - self.peg_value) / self.peg_value  # Adjust based on deviation
        self.supply -= adjustment
        print(f"Decreasing supply by {adjustment:.2f}. New supply: {self.supply:.2f}")

    def get_market_summary(self):
        print(f"Market Summary:")
        print(f"  Current Price: {self.current_price:.2f}")
        print(f"  Total Supply: {self.supply:.2f}")
        print(f"  Peg Value: {self.peg_value:.2f}")
        print(f"  Price History: {self.price_history}")

if __name__ == "__main__":
    peg_value = float(input("Enter peg value: "))
    
    market = PiCoinMarket(peg_value=peg_value)
    
    for _ in range(10):  # Simulate 10 market fluctuations
        market.simulate_market()
    
    market.get_market_summary()
