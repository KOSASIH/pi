# proposal_management.py

class Proposal:
    def __init__(self, proposal_id, description):
        self.proposal_id = proposal_id
        self.description = description
        self.votes = {}
        self.total_votes = 0
        self.status = "Pending"  # Status can be Pending, Active, or Completed

    def vote(self, voter, amount):
        if voter in self.votes:
            print(f"{voter} has already voted on this proposal.")
            return

        self.votes[voter] = amount
        self.total_votes += amount
        print(f"{voter} voted {amount} on Proposal {self.proposal_id}.")

    def get_results(self):
        return {
            "description": self.description,
            "total_votes": self.total_votes,
            "votes": self.votes,
            "status": self.status
        }

    def complete_proposal(self):
        self.status = "Completed"
        print(f"Proposal {self.proposal_id} has been completed.")

class ProposalManagement:
    def __init__(self):
        self.proposals = {}
        self.total_proposals = 0

    def create_proposal(self, description):
        self.total_proposals += 1
        proposal = Proposal(self.total_proposals, description)
        self.proposals[self.total_proposals] = proposal
        print(f"Proposal {self.total_proposals} created: {description}")

    def vote(self, proposal_id, voter, amount):
        if proposal_id not in self.proposals:
            print("Proposal does not exist.")
            return

        self.proposals[proposal_id].vote(voter, amount)

    def get_proposal_results(self, proposal_id):
        if proposal_id not in self.proposals:
            print("Proposal does not exist.")
            return

        results = self.proposals[proposal_id].get_results()
        print(f"Results for Proposal {proposal_id}:")
        print(f"Description: {results['description']}")
        print(f"Total Votes: {results['total_votes']}")
        for voter, amount in results['votes'].items():
            print(f"  {voter}: {amount}")
        print(f"Status: {results['status']}")

    def complete_proposal(self, proposal_id):
        if proposal_id not in self.proposals:
            print("Proposal does not exist.")
            return

        self.proposals[proposal_id].complete_proposal()

if __name__ == "__main__":
    proposal_management = ProposalManagement()
    
    # Example usage
    proposal_management.create_proposal("Increase the reward rate for staking.")
    proposal_management.create_proposal("Implement a new governance model.")
    
    proposal_management.vote(1, "Alice", 100)
    proposal_management.vote(1, "Bob", 200)
    proposal_management.vote(2, "Alice", 150);
    
    proposal_management.get_proposal_results(1)
    proposal_management.get_proposal_results(2)
    
    proposal_management.complete_proposal(1)
    proposal_management.get_proposal_results(1)
