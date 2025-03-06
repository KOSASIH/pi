# notifications_system.py

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationSystem:
    def __init__(self):
        self.subscribers = []  # List to hold user email addresses

    def register_user(self, email):
        """Register a user for notifications."""
        if email not in self.subscribers:
            self.subscribers.append(email)
            logging.info(f"User  registered for notifications: {email}")
        else:
            logging.warning(f"User  {email} is already registered.")

    def trigger_notification(self, subject, message):
        """Trigger a notification to all registered users."""
        for email in self.subscribers:
            self.send_email(email, subject, message)

    def send_email(self, to_email, subject, message):
        """Send an email notification."""
        from_email = "your_email@example.com"  # Replace with your email
        password = "your_password"  # Replace with your email password

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            # Set up the server
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server
            server.starttls()
            server.login(from_email, password)

            # Send the email
            server.send_message(msg)
            logging.info(f"Notification sent to {to_email}")
        except Exception as e:
            logging.error(f"Failed to send email to {to_email}: {e}")
        finally:
            server.quit()

    def notify_proposal_update(self, proposal_title, proposal_status):
        """Notify users about a proposal update."""
        subject = f"Proposal Update: {proposal_title}"
        message = f"The status of the proposal '{proposal_title}' has been updated to: {proposal_status}."
        self.trigger_notification(subject, message)

    def notify_staking_reward(self, user_email, reward_amount):
        """Notify a user about their staking reward."""
        subject = "Staking Reward Notification"
        message = f"You have received a staking reward of {reward_amount:.2f} Pi Coin."
        self.send_email(user_email, subject, message)

    def notify_market_change(self, market_info):
        """Notify users about significant market changes."""
        subject = "Market Change Alert"
        message = f"Important market change detected: {market_info}."
        self.trigger_notification(subject, message)

if __name__ == "__main__":
    # Example usage
    notification_system = NotificationSystem()

    # Register users for notifications
    notification_system.register_user("user1@example.com")
    notification_system.register_user("user2@example.com")

    # Notify users about a proposal update
    notification_system.notify_proposal_update("Increase Block Size", "Approved")

    # Notify a specific user about their staking reward
    notification_system.notify_staking_reward("user1@example.com", 50.0)

    # Notify users about a market change
    notification_system.notify_market_change("Pi Coin price increased by 10%")
