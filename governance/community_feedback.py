# community_feedback.py

import sqlite3
import logging
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommunityFeedback:
    def __init__(self):
        self.conn = sqlite3.connect('community_feedback.db')
        self.create_tables()

    def create_tables(self):
        """Create tables for storing feedback."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    proposal_id TEXT,
                    feedback_text TEXT,
                    sentiment REAL
                )
            ''')
        logging.info("Feedback table created.")

    def submit_feedback(self, user_id, proposal_id, feedback_text):
        """Submit feedback for a governance proposal."""
        sentiment = self.analyze_sentiment(feedback_text)
        with self.conn:
            self.conn.execute('INSERT INTO feedback (user_id, proposal_id, feedback_text, sentiment) VALUES (?, ?, ?, ?)',
                              (user_id, proposal_id, feedback_text, sentiment))
        logging.info(f"Feedback submitted by user {user_id} for proposal {proposal_id}: {feedback_text}")

    def analyze_sentiment(self, feedback_text):
        """Analyze the sentiment of the feedback text."""
        analysis = TextBlob(feedback_text)
        return analysis.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)

    def get_feedback_statistics(self, proposal_id):
        """Get feedback statistics for a specific proposal."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*), AVG(sentiment) FROM feedback WHERE proposal_id = ?', (proposal_id,))
        count, avg_sentiment = cursor.fetchone()
        logging.info(f"Feedback statistics for proposal {proposal_id}: Count = {count}, Average Sentiment = {avg_sentiment:.2f}")
        return count, avg_sentiment

if __name__ == "__main__":
    # Example usage
    feedback_system = CommunityFeedback()

    # Simulate submitting feedback
    feedback_system.submit_feedback("user123", "proposal_001", "I think this proposal is great!")
    feedback_system.submit_feedback("user456", "proposal_001", "This proposal is not good at all.")
    feedback_system.submit_feedback("user789", "proposal_002", "I have mixed feelings about this proposal.")

    # Get feedback statistics for a proposal
    count, avg_sentiment = feedback_system.get_feedback_statistics("proposal_001")
    print(f"Proposal ID: proposal_001, Feedback Count: {count}, Average Sentiment: {avg_sentiment:.2f}")
