pub mod telepathy_network;

use super::ai_filter::AiFilter;
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;

pub struct TelepathyNetwork {
    ai_filter: Arc<Mutex<AiFilter>>,
    telepathic_links: HashMap<String, Vec<String>>, // User -> Linked minds
}

impl TelepathyNetwork {
    pub fn new(ai_filter: Arc<Mutex<AiFilter>>) -> Self {
        Self { ai_filter, telepathic_links: HashMap::new() }
    }

    pub async fn establish_telepathic_link(&mut self, user1: &str, user2: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Filter for safety
        if self.ai_filter.lock().await.filter_input("telepathy_request").await? {
            self.telepathic_links.entry(user1.to_string()).or_insert(Vec::new()).push(user2.to_string());
            self.telepathic_links.entry(user2.to_string()).or_insert(Vec::new()).push(user1.to_string());
            println!("Telepathic link established between {} and {}", user1, user2);
        }
        Ok(())
    }

    pub async fn send_telepathic_message(&mut self, from: &str, to: &str, message: &str) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(links) = self.telepathic_links.get(from) {
            if links.contains(&to.to_string()) {
                println!("Telepathic message from {} to {}: {}", from, to, message);
            }
        }
        Ok(())
    }

    pub fn get_links(&self, user: &str) -> Vec<String> {
        self.telepathic_links.get(user).cloned().unwrap_or_default()
    }
}
