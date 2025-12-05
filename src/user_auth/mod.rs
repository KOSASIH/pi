pub mod user_auth;

use super::pi_coin::PiCoin;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct UserAuth {
    pi_coin: Arc<Mutex<PiCoin>>,
    sessions: HashMap<String, String>, // Token -> User
}

impl UserAuth {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, sessions: HashMap::new() }
    }

    pub async fn login(&mut self, user: &str, password: &str) -> Result<String, String> {
        // Simplified: Check Pi Coin balance as auth (min 1 PI)
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 1.0 && password == "pi_secure" { // Mock password
            let token = format!("token_{}", user);
            self.sessions.insert(token.clone(), user.to_string());
            Ok(token)
        } else {
            Err("Invalid credentials or insufficient Pi Coin".to_string())
        }
    }

    pub fn verify_token(&self, token: &str) -> Option<String> {
        self.sessions.get(token).cloned()
    }

    pub async fn logout(&mut self, token: &str) {
        self.sessions.remove(token);
    }
}
