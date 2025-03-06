# voting_system.py

class VotingSystem:
    def __init__(self):
        self.proposals = {}
        self.total_proposals = 0

    def create_proposal(self, description):
        self.total_proposals += 1
        self.proposals[self.total_proposals] = {
            'description': description,
            'votes': {},
            'total_votes': 0
        }
        print(f"Proposal {self.total_proposals} created: {description}")

    def vote(self, proposal_id, voter, amount):
        if proposal_id not in self.proposals:
            print("Proposal does not exist.")
            return

        if voter in self.proposals[proposal_id]['votes']:
            print(f"{voter} has already voted on this proposal.")
            return

        self.proposals[proposal_id]['votes'][voter] = amount
        self.proposals[proposal_id]['total_votes'] += amount
        print(f"{voter} voted {amount} on Proposal {proposal_id}.")

    def get_results(self, proposal_id):
        if proposal_id not in self.proposals:
            print("Proposal does not exist.")
            return

        proposal = self.proposals[proposal_id]
        print(f"Results for Proposal {proposal_id}:")
        print(f"Description: {proposal['description']}")
        print(f"Total Votes: {proposal['total_votes']}")
        for voter, amount in proposal['votes'].items():
            print(f"  {voter}: {amount}")

if __name__ == "__main__":
    voting_system = VotingSystem()
    
    # Example usage
    voting_system.create_proposal("Increase the reward rate for staking.")
    voting_system.create_proposal("Implement a new governance model.")
    
    voting_system.vote(1, "Alice", 100)
    voting_system.vote(1, "Bob", 200)
    voting_system.vote(2, "Alice", 150)
    
    voting_system.get_results(1)
    voting_system.get_results(2)
