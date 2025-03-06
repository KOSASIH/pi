# lending_protocol.py

class LendingProtocol:
    def __init__(self):
        self.users = {}
        self.total_collateral = 0
        self.total_loans = 0
        self.interest_rate = 0.05  # 5% interest rate

    def deposit_collateral(self, user, amount):
        if user not in self.users:
            self.users[user] = {'collateral': 0, 'loan': 0}
        self.users[user]['collateral'] += amount
        self.total_collateral += amount
        print(f"{user} deposited {amount} as collateral. Total collateral: {self.total_collateral}")

    def borrow(self, user, amount):
        if user not in self.users:
            print("User  not registered. Please deposit collateral first.")
            return

        collateral = self.users[user]['collateral']
        if collateral <= 0:
            print("No collateral deposited.")
            return

        # Calculate maximum loan based on collateral (e.g., 50% of collateral)
        max_loan = collateral * 0.5
        if amount > max_loan:
            print(f"Cannot borrow more than {max_loan}.")
            return

        self.users[user]['loan'] += amount
        self.total_loans += amount
        print(f"{user} borrowed {amount}. Total loans: {self.total_loans}")

    def repay_loan(self, user, amount):
        if user not in self.users or self.users[user]['loan'] <= 0:
            print("No loan to repay.")
            return

        loan_amount = self.users[user]['loan']
        if amount < loan_amount:
            print(f"Repaying {amount}. Remaining loan: {loan_amount - amount}")
            self.users[user]['loan'] -= amount
        else:
            print(f"Loan fully repaid. Previous loan: {loan_amount}")
            self.users[user]['loan'] = 0

    def calculate_interest(self, user):
        if user not in self.users:
            print("User  not registered.")
            return

        loan_amount = self.users[user]['loan']
        interest = loan_amount * self.interest_rate
        print(f"Interest for {user}: {interest}")

if __name__ == "__main__":
    protocol = LendingProtocol()
    
    # Example usage
    protocol.deposit_collateral("Alice", 1000)
    protocol.borrow("Alice", 400)
    protocol.calculate_interest("Alice")
    protocol.repay_loan("Alice", 200)
    protocol.calculate_interest("Alice")
    protocol.repay_loan("Alice", 200)
