# api_server.py

from flask import Flask, request, jsonify
from proposal_management import ProposalManagement

app = Flask(__name__)
proposal_management = ProposalManagement()

@app.route('/proposals', methods=['POST'])
def create_proposal():
    data = request.json
    description = data.get('description')
    proposal_management.create_proposal(description)
    return jsonify({"message": "Proposal created successfully."}), 201

@app.route('/proposals/<int:proposal_id>/vote', methods=['POST'])
def vote_on_proposal(proposal_id):
    data = request.json
    voter = data.get('voter')
    amount = data.get('amount')
    proposal_management.vote(proposal_id, voter, amount)
    return jsonify({"message": "Vote recorded successfully."}), 200

@app.route('/proposals/<int:proposal_id>/results', methods=['GET'])
def get_proposal_results(proposal_id):
    results = proposal_management.get_proposal_results(proposal_id)
    return jsonify(results), 200

@app.route('/proposals/<int:proposal_id>/complete', methods=['POST'])
def complete_proposal(proposal_id):
    proposal_management.complete_proposal(proposal_id)
    return jsonify({"message": "Proposal completed successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
