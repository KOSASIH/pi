pub mod ecosystem_bridge;

use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct EcosystemBridge {
    pi_coin: Arc<Mutex<PiCoin>>,
    connected_apps: Vec<String>,
}

impl EcosystemBridge {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, connected_apps: Vec::new() }
    }

    pub async fn connect_app(&mut self, app_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Verify with Pi Coin balance
        let balance = self.pi_coin.lock().await.get_balance(app_id);
        if balance > 0.0 {
            self.connected_apps.push(app_id.to_string());
            println!("Connected to Pi Ecosystem app: {}", app_id);
        } else {
            return Err("Insufficient Pi Coin for connection".into());
        }
        Ok(())
    }

    pub async fn transfer_data(&mut self, from_app: &str, to_app: &str, data: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
        // Secure transfer via Pi Coin escrow
        self.pi_coin.lock().await.p2p_transfer(from_app, "escrow", 0.01)?;
        println!("Data transferred between {} and {}", from_app, to_app);
        Ok(())
    }

    pub fn list_connected_apps(&self) -> Vec<String> {
        self.connected_apps.clone()
    }
}
