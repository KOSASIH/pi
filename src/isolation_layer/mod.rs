pub mod isolation_layer;

use super::ai_filter::AiFilter;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct IsolationLayer {
    ai_filter: Arc<Mutex<AiFilter>>,
}

impl IsolationLayer {
    pub fn new(ai_filter: Arc<Mutex<AiFilter>>) -> Self {
        Self { ai_filter }
    }

    pub async fn isolate_request(&mut self, request: &str) -> Result<(), Box<dyn std::error::Error>> {
        if !self.ai_filter.lock().await.filter_input(request).await? {
            println!("Isolated volatile request: {}", request);
            // Block or quarantine
        }
        Ok(())
    }

    pub async fn enforce_isolation(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Continuous scan for volatile tech (e.g., block external APIs)
        println!("Enforcing isolation: Rejecting all volatile finance/crypto inputs");
        Ok(())
    }
}
