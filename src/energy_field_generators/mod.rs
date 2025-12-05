pub mod energy_field_generators;

use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct EnergyFieldGenerators {
    pi_coin: Arc<Mutex<PiCoin>>,
    fields: Vec<EnergyField>,
}

impl EnergyFieldGenerators {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, fields: Vec::new() }
    }

    pub async fn generate_field(&mut self, strength: f64, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= strength { // Energy cost
            let field = EnergyField { strength, active: true };
            self.fields.push(field);
            println!("Energy field generated with strength {} for {}", strength, user);
        } else {
            return Err("Insufficient Pi Coin for energy".into());
        }
        Ok(())
    }

    pub async fn maintain_fields(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        for field in &mut self.fields {
            if field.active {
                // Simulate maintenance
                println!("Maintaining energy field with strength {}", field.strength);
            }
        }
        Ok(())
    }

    pub fn get_fields(&self) -> Vec<EnergyField> {
        self.fields.clone()
    }
}

#[derive(Clone)]
pub struct EnergyField {
    strength: f64,
    active: bool,
}
