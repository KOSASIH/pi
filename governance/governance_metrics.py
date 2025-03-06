import uuid
import logging
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GovernanceMetrics:
    def __init__(self):
        self.proposals = []  # List to hold proposals
        self.voter_turnout = []  # List to hold voter turnout percentages

    def add_proposal(self, title, description):
        """Add a proposal to the governance metrics."""
        proposal_id = str(uuid.uuid4())
        self.proposals.append({
            'id': proposal_id,
            'title': title,
            'description': description,
            'status': 'pending',  # Initial status
            'votes_for': 0,
            'votes_against': 0,
            'total_votes': 0
        })
        logging.info(f"Proposal added: {title} (ID: {proposal_id})")

    def vote(self, proposal_id, vote):
        """Record a vote for a proposal."""
        for proposal in self.proposals:
            if proposal['id'] == proposal_id:
                if vote == 'for':
                    proposal['votes_for'] += 1
                elif vote == 'against':
                    proposal['votes_against'] += 1
                proposal['total_votes'] += 1
                logging.info(f"Vote recorded for proposal ID {proposal_id}: {vote}")
                return
        logging.error("Proposal ID not found.")

    def finalize_proposal(self, proposal_id):
        """Finalize a proposal and determine its status."""
        for proposal in self.proposals:
            if proposal['id'] == proposal_id:
                if proposal['votes_for'] > proposal['votes_against']:
                    proposal['status'] = 'approved'
                else:
                    proposal['status'] = 'rejected'
                logging.info(f"Proposal finalized: {proposal['title']} - Status: {proposal['status']}")
                return
        logging.error("Proposal ID not found.")

    def calculate_success_rate(self):
        """Calculate the success rate of proposals."""
        if not self.proposals:
            return 0.0
        successful_proposals = sum(1 for p in self.proposals if p['status'] == 'approved')
        success_rate = (successful_proposals / len(self.proposals)) * 100
        logging.info(f"Success rate of proposals: {success_rate:.2f}%")
        return success_rate

    def record_voter_turnout(self, turnout_percentage):
        """Record voter turnout percentage."""
        self.voter_turnout.append(turnout_percentage)
        logging.info(f"Voter turnout recorded: {turnout_percentage:.2f}%")

    def visualize_metrics(self):
        """Visualize governance metrics."""
        # Visualize success rate
        success_rate = self.calculate_success_rate()
        plt.figure(figsize=(10, 5))
        plt.bar(['Success Rate'], [success_rate], color='green')
        plt.ylim(0, 100)
        plt.title('Governance Proposal Success Rate')
        plt.ylabel('Percentage (%)')
        plt.grid()
        plt.show()

        # Visualize voter turnout
        plt.figure(figsize=(10, 5))
        plt.plot(self.voter_turnout, marker='o', linestyle='-', color='blue')
        plt.title('Voter Turnout Over Time')
        plt.xlabel('Voting Period')
        plt.ylabel('Turnout Percentage (%)')
        plt.grid()
        plt.show()

if __name__ == "__main__":
    # Example usage
    metrics = GovernanceMetrics()

    # Add proposals
    metrics.add_proposal("Increase Block Size", "Proposal to increase the block size to improve transaction throughput.")
    metrics.add_proposal("New Governance Model", "Proposal to implement a new governance model for better community engagement.")

    # Simulate voting
    metrics.vote(metrics.proposals[0]['id'], 'for')
    metrics.vote(metrics.proposals[0]['id'], 'against')
    metrics.vote(metrics.proposals[0]['id'], 'for')
    metrics.vote(metrics.proposals[1]['id'], 'for')

    # Finalize proposals
    metrics.finalize_proposal(metrics.proposals[0]['id'])
    metrics.finalize_proposal(metrics.proposals[1]['id'])

    # Record voter turnout
    metrics.record_voter_turnout(75.0)  # Example turnout percentage
    metrics.record_voter_turnout(80.0)  # Another example turnout percentage

    # Visualize metrics
    metrics.visualize_metrics()
