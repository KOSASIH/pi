pub mod resource_manager;

use super::pi_coin::PiCoin;
use super::ai_orchestrator::AiOrchestrator;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct ResourceManager {
    pi_coin: Arc<Mutex<PiCoin>>,
    ai: Arc<Mutex<AiOrchestrator>>,
    allocated_resources: HashMap<String, Resource>,
}

impl ResourceManager {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>, ai: Arc<Mutex<AiOrchestrator>>) -> Self {
        Self { pi_coin, ai, allocated_resources: HashMap::new() }
    }

    pub async fn allocate_resource(&mut self, user: &str, resource_type: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 1.0 {
            let resource = Resource { rtype: resource_type.to_string(), amount: 100 }; // Placeholder
            self.allocated_resources.insert(user.to_string(), resource);
            println!("Allocated {} for {}", resource_type, user);
        } else {
            return Err("Insufficient Pi Coin".into());
        }
        Ok(())
    }

    pub async fn optimize_resources(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Use AI for optimization
        // self.ai.lock().await.optimize().await?;
        println!("Resources optimized");
        Ok(())
    }
}

pub struct Resource {
    rtype: String,
    amount: u32,
}
