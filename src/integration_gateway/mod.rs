pub mod integration_gateway;

use super::ai_filter::AiFilter;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct IntegrationGateway {
    ai_filter: Arc<Mutex<AiFilter>>,
    integrations: Vec<String>,
}

impl IntegrationGateway {
    pub fn new(ai_filter: Arc<Mutex<AiFilter>>) -> Self {
        Self { ai_filter, integrations: Vec::new() }
    }

    pub async fn add_integration(&mut self, app: &str) -> Result<(), Box<dyn std::error::Error>> {
        if self.ai_filter.lock().await.filter_input(app).await? {
            self.integrations.push(app.to_string());
            println!("Integrated app: {}", app);
        } else {
            return Err("Rejected volatile integration".into());
        }
        Ok(())
    }

    pub fn list_integrations(&self) -> Vec<String> {
        self.integrations.clone()
    }
}
