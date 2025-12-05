pub mod telekinetic_manipulation;

use super::ai_orchestrator::AiOrchestrator;
use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct TelekineticManipulation {
    ai: Arc<Mutex<AiOrchestrator>>,
    pi_coin: Arc<Mutex<PiCoin>>,
    manipulated_objects: Vec<TelekineticObject>,
}

impl TelekineticManipulation {
    pub fn new(ai: Arc<Mutex<AiOrchestrator>>, pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { ai, pi_coin, manipulated_objects: Vec::new() }
    }

    pub async fn manipulate_object(&mut self, object_id: &str, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 15.0 { // Manipulation energy cost
            let object = TelekineticObject { id: object_id.to_string(), position: [0.0, 0.0, 0.0] };
            self.manipulated_objects.push(object);
            // AI-guided movement
            self.ai.lock().await.optimize_vms(&Arc::new(Mutex::new(super::hypervisor::Hypervisor::new()?))).await?;
            println!("Telekinetic manipulation initiated on {} by {}", object_id, user);
        } else {
            return Err("Insufficient Pi Coin for telekinesis".into());
        }
        Ok(())
    }

    pub async fn move_object(&mut self, object_id: &str, new_pos: [f64; 3]) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(obj) = self.manipulated_objects.iter_mut().find(|o| o.id == object_id) {
            obj.position = new_pos;
            println!("Object {} moved to position {:?}", object_id, new_pos);
        }
        Ok(())
    }

    pub fn get_manipulated_objects(&self) -> Vec<TelekineticObject> {
        self.manipulated_objects.clone()
    }
}

#[derive(Clone)]
pub struct TelekineticObject {
    id: String,
    position: [f64; 3],
}
