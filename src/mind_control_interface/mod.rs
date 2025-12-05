pub mod mind_control_interface;

use super::ai_orchestrator::AiOrchestrator;
use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct MindControlInterface {
    ai: Arc<Mutex<AiOrchestrator>>,
    pi_coin: Arc<Mutex<PiCoin>>,
    controlled_entities: Vec<String>,
}

impl MindControlInterface {
    pub fn new(ai: Arc<Mutex<AiOrchestrator>>, pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { ai, pi_coin, controlled_entities: Vec::new() }
    }

    pub async fn initiate_mind_control(&mut self, entity: &str, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 50.0 { // High fee for mind control
            self.controlled_entities.push(entity.to_string());
            // AI-guided control
            self.ai.lock().await.optimize_vms(&Arc::new(Mutex::new(super::hypervisor::Hypervisor::new()?))).await?;
            println!("Mind control initiated on {} by {}", entity, user);
        } else {
            return Err("Insufficient Pi Coin for mind control".into());
        }
        Ok(())
    }

    pub async fn execute_mind_command(&mut self, entity: &str, command: &str) -> Result<(), Box<dyn std::error::Error>> {
        if self.controlled_entities.contains(&entity.to_string()) {
            println!("Mind command executed on {}: {}", entity, command);
        }
        Ok(())
    }

    pub fn get_controlled_entities(&self) -> Vec<String> {
        self.controlled_entities.clone()
    }
}
