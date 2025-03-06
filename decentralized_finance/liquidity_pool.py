# liquidity_pool.py

class LiquidityPool:
    def __init__(self):
        self.liquidity_providers = {}
        self.total_liquidity = 0
        self.total_fees = 0
        self.fee_rate = 0.003  # 0.3% fee on trades

    def add_liquidity(self, provider, amount):
        if provider not in self.liquidity_providers:
            self.liquidity_providers[provider] = 0
        self.liquidity_providers[provider] += amount
        self.total_liquidity += amount
        print(f"{provider} added {amount} liquidity. Total liquidity: {self.total_liquidity}")

    def remove_liquidity(self, provider, amount):
        if provider not in self.liquidity_providers or self.liquidity_providers[provider] < amount:
            print("Insufficient liquidity to remove.")
            return

        self.liquidity_providers[provider] -= amount
        self.total_liquidity -= amount
        print(f"{provider} removed {amount} liquidity. Total liquidity: {self.total_liquidity}")

    def trade(self, amount):
        if self.total_liquidity <= 0:
            print("No liquidity available for trading.")
            return

        # Calculate fees
        fees = amount * self.fee_rate
        self.total_fees += fees
        print(f"Trade executed for {amount}. Fees collected: {fees}. Total fees: {self.total_fees}")

    def distribute_fees(self):
        if self.total_fees == 0:
            print("No fees to distribute.")
            return

        for provider, liquidity in self.liquidity_providers.items():
            if liquidity > 0:
                provider_fee = (liquidity / self.total_liquidity) * self.total_fees
                print(f"Distributing {provider_fee} to {provider}.")
                self.liquidity_providers[provider] += provider_fee  # Add fees to provider's liquidity

        self.total_fees = 0  # Reset total fees after distribution

if __name__ == "__main__":
    pool = LiquidityPool()
    
    # Example usage
    pool.add_liquidity("Alice", 1000)
    pool.add_liquidity("Bob", 2000)
    pool.trade(5000)
    pool.distribute_fees()
    pool.remove_liquidity("Alice", 500)
    pool.remove_liquidity("Bob", 1000)
