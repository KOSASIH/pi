pub mod decentralized_identity;

use super::pi_coin::PiCoin;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct DecentralizedIdentity {
    pi_coin: Arc<Mutex<PiCoin>>,
    identities: HashMap<String, Identity>,
}

impl DecentralizedIdentity {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, identities: HashMap::new() }
    }

    pub async fn create_identity(&mut self, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 1.0 { // Require min Pi Coin
            let identity = Identity { user: user.to_string(), verified: true };
            self.identities.insert(user.to_string(), identity);
            println!("Created decentralized identity for: {}", user);
        } else {
            return Err("Insufficient Pi Coin for identity creation".into());
        }
        Ok(())
    }

    pub fn verify_identity(&self, user: &str) -> bool {
        self.identities.get(user).map(|id| id.verified).unwrap_or(false)
    }
}

pub struct Identity {
    user: String,
    verified: bool,
}
