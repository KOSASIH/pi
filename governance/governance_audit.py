import uuid
import logging
import sqlite3
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GovernanceAudit:
    def __init__(self):
        self.conn = sqlite3.connect('governance_audit.db')
        self.create_tables()

    def create_tables(self):
        """Create tables for governance actions and audit logs."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS governance_actions (
                    action_id TEXT PRIMARY KEY,
                    action_type TEXT,
                    description TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    log_id TEXT PRIMARY KEY,
                    action_id TEXT,
                    user_id TEXT,
                    result TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (action_id) REFERENCES governance_actions (action_id)
                )
            ''')

    def record_governance_action(self, action_type, description):
        """Record a governance action."""
        action_id = str(uuid.uuid4())
        with self.conn:
            self.conn.execute('INSERT INTO governance_actions (action_id, action_type, description) VALUES (?, ?, ?)',
                              (action_id, action_type, description))
        logging.info(f"Governance action recorded: {action_type} - {description} (ID: {action_id})")
        return action_id

    def record_audit_log(self, action_id, user_id, result):
        """Record an audit log for a governance action."""
        log_id = str(uuid.uuid4())
        with self.conn:
            self.conn.execute('INSERT INTO audit_logs (log_id, action_id, user_id, result) VALUES (?, ?, ?, ?)',
                              (log_id, action_id, user_id, result))
        logging.info(f"Audit log recorded: Action ID {action_id}, User ID {user_id}, Result: {result}")

    def generate_audit_report(self):
        """Generate a report of all governance actions and their audit logs."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ga.action_id, ga.action_type, ga.description, ga.timestamp, al.user_id, al.result, al.timestamp
            FROM governance_actions ga
            LEFT JOIN audit_logs al ON ga.action_id = al.action_id
        ''')
        report = cursor.fetchall()

        logging.info("Generating audit report...")
        for row in report:
            action_id, action_type, description, action_timestamp, user_id, result, log_timestamp = row
            print(f"Action ID: {action_id}, Type: {action_type}, Description: {description}, "
                  f"Action Timestamp: {action_timestamp}, User ID: {user_id}, Result: {result}, "
                  f"Log Timestamp: {log_timestamp}")

if __name__ == "__main__":
    # Example usage
    audit_system = GovernanceAudit()

    # Record a governance action
    action_id = audit_system.record_governance_action("Proposal", "Proposal to increase the block size.")

    # Record an audit log for the action
    audit_system.record_audit_log(action_id, "user123", "Approved")

    # Generate an audit report
    audit_system.generate_audit_report()
