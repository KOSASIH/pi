import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommunityEngagement:
    def __init__(self):
        self.feedbacks = []  # List to hold feedback entries
        self.events = {}     # Dictionary to hold events

    def collect_feedback(self, user_id, feedback_text):
        """Collect feedback from users."""
        feedback_id = str(uuid.uuid4())  # Generate a unique feedback ID
        feedback_entry = {
            'feedback_id': feedback_id,
            'user_id': user_id,
            'feedback_text': feedback_text
        }
        self.feedbacks.append(feedback_entry)
        logging.info(f"Feedback collected from user {user_id}: {feedback_text}")
        return feedback_id

    def create_event(self, event_name, event_date, event_description):
        """Create a new community event."""
        event_id = str(uuid.uuid4())  # Generate a unique event ID
        event_details = {
            'event_id': event_id,
            'event_name': event_name,
            'event_date': event_date,
            'event_description': event_description
        }
        self.events[event_id] = event_details
        logging.info(f"Event created: {event_name} on {event_date}")
        return event_id

    def get_feedbacks(self):
        """Retrieve all feedback entries."""
        logging.info(f"Retrieving all feedbacks: {self.feedbacks}")
        return self.feedbacks

    def get_events(self):
        """Retrieve all community events."""
        logging.info(f"Retrieving all events: {self.events}")
        return self.events

if __name__ == "__main__":
    # Example usage
    community_engagement = CommunityEngagement()

    # Collect feedback
    feedback_id = community_engagement.collect_feedback("user123", "Great project! Looking forward to the future.")
    
    # Create an event
    event_id = community_engagement.create_event("Pi Coin Community Meetup", "2023-12-01", "Join us for a community meetup to discuss the future of Pi Coin.")

    # Retrieve feedbacks
    feedbacks = community_engagement.get_feedbacks()

    # Retrieve events
    events = community_engagement.get_events()

    # Print results
    print(f"Feedback ID: {feedback_id}")
    print(f"Events: {events}")
    print(f"Feedbacks: {feedbacks}")
