# automated_market_maker.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomatedMarketMaker:
    def __init__(self):
        self.pool = {}  # Dictionary to hold asset pools

    def add_liquidity(self, asset, amount):
        """Add liquidity to the market maker."""
        if asset in self.pool:
            self.pool[asset] += amount
        else:
            self.pool[asset] = amount
        logging.info(f"Added {amount} of {asset} to the liquidity pool. Current pool: {self.pool}")

    def remove_liquidity(self, asset, amount):
        """Remove liquidity from the market maker."""
        if asset in self.pool and self.pool[asset] >= amount:
            self.pool[asset] -= amount
            logging.info(f"Removed {amount} of {asset} from the liquidity pool. Current pool: {self.pool}")
        else:
            logging.error("Insufficient liquidity to remove.")

    def get_price(self, asset1, asset2):
        """Calculate price based on the constant product formula."""
        if asset1 in self.pool and asset2 in self.pool:
            price = self.pool[asset1] / self.pool[asset2]
            return price
        else:
            logging.error("One of the assets is not in the pool.")
            return None

    def trade(self, asset_in, amount_in, asset_out):
        """Execute a trade from asset_in to asset_out."""
        if asset_in not in self.pool or asset_out not in self.pool:
            logging.error("One of the assets is not in the pool.")
            return None

        # Calculate the amount of asset_out to give based on the constant product formula
        amount_out = (self.pool[asset_out] * amount_in) / (self.pool[asset_in] + amount_in)

        # Update the pool
        self.pool[asset_in] += amount_in
        self.pool[asset_out] -= amount_out

        logging.info(f"Traded {amount_in} of {asset_in} for {amount_out:.4f} of {asset_out}. Current pool: {self.pool}")
        return amount_out

if __name__ == "__main__":
    # Example usage
    ammk = AutomatedMarketMaker()

    # Add initial liquidity
    ammk.add_liquidity('PiCoin', 1000)
    ammk.add_liquidity('USD', 500)

    # Get price of PiCoin in USD
    price = ammk.get_price('PiCoin', 'USD')
    print(f"Price of PiCoin in USD: {price:.2f}")

    # Execute a trade
    amount_out = ammk.trade('USD', 100, 'PiCoin')
    print(f"Amount of PiCoin received: {amount_out:.4f}")

    # Remove liquidity
    ammk.remove_liquidity('PiCoin', 200)
