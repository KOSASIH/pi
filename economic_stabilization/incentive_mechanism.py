class IncentiveMechanism:
    def __init__(self):
        self.user_rewards = {}

    def transact(self, user, amount):
        # Simulate a transaction and reward the user
        if user not in self.user_rewards:
            self.user_rewards[user] = 0
        reward = self.calculate_reward(amount)
        self.user_rewards[user] += reward
        print(f"User  {user} transacted {amount} PI. Reward: {reward}. Total Rewards: {self.user_rewards[user]}")

    def calculate_reward(self, amount):
        # Reward 2% of the transaction amount
        return amount * 0.02

if __name__ == "__main__":
    incentive_system = IncentiveMechanism()
    incentive_system.transact("Alice", 1000)
    incentive_system.transact("Bob", 500)
    incentive_system.transact("Alice", 2000)
