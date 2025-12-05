pub mod bio_organic_fusion;

use super::pi_coin::PiCoin;
use super::monitoring::Monitoring;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct BioOrganicFusion {
    pi_coin: Arc<Mutex<PiCoin>>,
    monitoring: Arc<Mutex<Monitoring>>,
    fusions: Vec<Fusion>,
}

impl BioOrganicFusion {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>, monitoring: Arc<Mutex<Monitoring>>) -> Self {
        Self { pi_coin, monitoring, fusions: Vec::new() }
    }

    pub async fn initiate_fusion(&mut self, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 100.0 { // Fusion cost
            let fusion = Fusion { user: user.to_string(), enhancement_level: 1.0 };
            self.fusions.push(fusion);
            println!("Bio-organic fusion initiated for {}", user);
        } else {
            return Err("Insufficient Pi Coin for fusion".into());
        }
        Ok(())
    }

    pub async fn monitor_fusion_health(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        for fusion in &self.fusions {
            // Use monitoring for health check
            self.monitoring.lock().await.monitor_system().await?;
            println!("Fusion health monitored for {}", fusion.user);
        }
        Ok(())
    }

    pub fn get_fusions(&self) -> Vec<Fusion> {
        self.fusions.clone()
    }
}

#[derive(Clone)]
pub struct Fusion {
    user: String,
    enhancement_level: f64,
}
