# web_app.py

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5000"  # URL of the API server

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_proposal', methods=['POST'])
def create_proposal():
    description = request.form['description']
    response = requests.post(f"{API_URL}/proposals", json={"description": description})
    return redirect(url_for('index'))

@app.route('/vote', methods=['POST'])
def vote():
    proposal_id = request.form['proposal_id']
    voter = request.form['voter']
    amount = request.form['amount']
    response = requests.post(f"{API_URL}/proposals/{proposal_id}/vote", json={"voter": voter, "amount": amount})
    return redirect(url_for('index'))

@app.route('/results/<int:proposal_id>')
def results(proposal_id):
    response = requests.get(f"{API_URL}/proposals/{proposal_id}/results")
    results = response.json()
    return render_template('results.html', results=results)

@app.route('/complete/<int:proposal_id>', methods=['POST'])
def complete(proposal_id):
    response = requests.post(f"{API_URL}/proposals/{proposal_id}/complete")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)
