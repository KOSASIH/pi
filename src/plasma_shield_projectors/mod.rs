pub mod plasma_shield_projectors;

use super::ai_filter::AiFilter;
use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct PlasmaShieldProjectors {
    ai_filter: Arc<Mutex<AiFilter>>,
    pi_coin: Arc<Mutex<PiCoin>>,
    shields: Vec<PlasmaShield>,
}

impl PlasmaShieldProjectors {
    pub fn new(ai_filter: Arc<Mutex<AiFilter>>, pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { ai_filter, pi_coin, shields: Vec::new() }
    }

    pub async fn project_shield(&mut self, user: &str, strength: f64) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= strength * 2.0 { // Shield cost
            let shield = PlasmaShield { strength, active: true };
            self.shields.push(shield);
            println!("Plasma shield projected with strength {} for {}", strength, user);
        } else {
            return Err("Insufficient Pi Coin for plasma shield".into());
        }
        Ok(())
    }

    pub async fn modulate_shield(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        for shield in &mut self.shields {
            if shield.active {
                // AI modulation for threats
                if self.ai_filter.lock().await.filter_input("threat").await? {
                    shield.strength += 10.0;
                    println!("Shield modulated to strength {}", shield.strength);
                }
            }
        }
        Ok(())
    }

    pub fn get_shields(&self) -> Vec<PlasmaShield> {
        self.shields.clone()
    }
}

#[derive(Clone)]
pub struct PlasmaShield {
    strength: f64,
    active: bool,
}
