pub mod notification_system;

use std::sync::Arc;
use tokio::sync::Mutex;
use super::monitoring::Monitoring;

pub struct NotificationSystem {
    monitoring: Arc<Mutex<Monitoring>>,
    notifications: Vec<String>,
}

impl NotificationSystem {
    pub fn new(monitoring: Arc<Mutex<Monitoring>>) -> Self {
        Self { monitoring, notifications: Vec::new() }
    }

    pub async fn send_notification(&mut self, message: &str) -> Result<(), Box<dyn std::error::Error>> {
        self.notifications.push(message.to_string());
        println!("Notification sent: {}", message);
        // Simulate delivery (e.g., to web interface)
        Ok(())
    }

    pub async fn check_and_notify(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        let alerts = self.monitoring.lock().await.get_alerts();
        for alert in alerts {
            self.send_notification(&alert).await?;
        }
        Ok(())
    }

    pub fn get_notifications(&self) -> Vec<String> {
        self.notifications.clone()
    }
}
