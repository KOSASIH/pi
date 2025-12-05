pub mod logging;

use super::data_storage::DataStorage;
use std::sync::Arc;
use tokio::sync::Mutex;
use chrono::Utc;

pub struct Logging {
    storage: Arc<Mutex<DataStorage>>,
    logs: Vec<String>,
}

impl Logging {
    pub fn new(storage: Arc<Mutex<DataStorage>>) -> Self {
        Self { storage, logs: Vec::new() }
    }

    pub async fn log_event(&mut self, event: &str) -> Result<(), Box<dyn std::error::Error>> {
        let timestamped = format!("[{}] {}", Utc::now(), event);
        self.logs.push(timestamped.clone());
        self.storage.lock().await.store_data("logs.enc", timestamped.as_bytes()).await?;
        println!("Logged: {}", event);
        Ok(())
    }

    pub async fn rotate_logs(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Backup and clear logs
        self.storage.lock().await.backup("logs.enc").await?;
        self.logs.clear();
        println!("Logs rotated");
        Ok(())
    }

    pub fn get_recent_logs(&self) -> Vec<String> {
        self.logs.iter().rev().take(10).cloned().collect()
    }
}
