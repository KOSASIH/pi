pub mod pi_coin;

use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;

pub const PI_VALUE_USD: f64 = 314159.0; // Fixed value in USD

#[derive(Clone)]
pub struct PiCoin {
    ledger: HashMap<String, f64>, // User -> PI balance
}

impl PiCoin {
    pub fn new() -> Self {
        Self { ledger: HashMap::new() }
    }

    pub fn mine(&mut self, user: &str, amount: f64) {
        *self.ledger.entry(user.to_string()).or_insert(0.0) += amount;
        println!("Mined {} PI for {}", amount, user);
    }

    pub fn reward_contribution(&mut self, user: &str, amount: f64) {
        *self.ledger.entry(user.to_string()).or_insert(0.0) += amount;
        println!("Rewarded {} PI for contribution to {}", amount, user);
    }

    pub fn p2p_transfer(&mut self, from: &str, to: &str, amount: f64) -> Result<(), String> {
        if let Some(balance) = self.ledger.get_mut(from) {
            if *balance >= amount {
                *balance -= amount;
                *self.ledger.entry(to.to_string()).or_insert(0.0) += amount;
                println!("Transferred {} PI from {} to {}", amount, from, to);
                Ok(())
            } else {
                Err("Insufficient balance".to_string())
            }
        } else {
            Err("User not found".to_string())
        }
    }

    pub fn get_balance(&self, user: &str) -> f64 {
        *self.ledger.get(user).unwrap_or(&0.0)
    }

    pub fn usd_value(&self, pi_amount: f64) -> f64 {
        pi_amount * PI_VALUE_USD
    }
}
