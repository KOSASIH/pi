# yield_farming.py

class YieldFarming:
    def __init__(self):
        self.stakers = {}
        self.total_staked = 0
        self.reward_rate = 0.1  # 10% reward rate per cycle

    def stake(self, user, amount):
        if user not in self.stakers:
            self.stakers[user] = {'staked': 0, 'rewards': 0}
        
        self.stakers[user]['staked'] += amount
        self.total_staked += amount
        print(f"{user} has staked {amount}. Total staked: {self.total_staked}")

    def calculate_rewards(self, user):
        if user not in self.stakers:
            print("User  not found.")
            return 0
        
        staked_amount = self.stakers[user]['staked']
        rewards = staked_amount * self.reward_rate
        self.stakers[user]['rewards'] += rewards
        print(f"{user} earned {rewards} in rewards.")
        return rewards

    def withdraw(self, user):
        if user not in self.stakers or self.stakers[user]['staked'] <= 0:
            print("No staked amount to withdraw.")
            return
        
        staked_amount = self.stakers[user]['staked']
        rewards = self.stakers[user]['rewards']
        
        # Reset user's staked amount and rewards
        self.stakers[user]['staked'] = 0
        self.stakers[user]['rewards'] = 0
        self.total_staked -= staked_amount
        
        print(f"{user} withdrew {staked_amount} and earned {rewards} in rewards.")
        return staked_amount + rewards

if __name__ == "__main__":
    farm = YieldFarming()
    
    # Example usage
    farm.stake("Alice", 1000)
    farm.stake("Bob", 2000)
    
    # Simulate a reward cycle
    farm.calculate_rewards("Alice")
    farm.calculate_rewards("Bob")
    
    # Users withdraw their stakes and rewards
    farm.withdraw("Alice")
    farm.withdraw("Bob")
