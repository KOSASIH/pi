pub mod wormhole_communication;

use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;

pub struct WormholeCommunication {
    pi_coin: Arc<Mutex<PiCoin>>,
    wormholes: HashMap<String, Wormhole>,
}

impl WormholeCommunication {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, wormholes: HashMap::new() }
    }

    pub async fn create_wormhole(&mut self, id: &str, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 5.0 { // Wormhole creation fee
            let wormhole = Wormhole { id: id.to_string(), data_tunnel: vec![] };
            self.wormholes.insert(id.to_string(), wormhole);
            println!("Wormhole '{}' created for {}", id, user);
        } else {
            return Err("Insufficient Pi Coin for wormhole".into());
        }
        Ok(())
    }

    pub async fn send_through_wormhole(&mut self, id: &str, data: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(wormhole) = self.wormholes.get_mut(id) {
            wormhole.data_tunnel.extend_from_slice(data);
            println!("Data sent through wormhole {}: {} bytes", id, data.len());
        } else {
            return Err("Wormhole not found".into());
        }
        Ok(())
    }

    pub async fn receive_from_wormhole(&mut self, id: &str) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
        if let Some(wormhole) = self.wormholes.get_mut(id) {
            let data = wormhole.data_tunnel.clone();
            wormhole.data_tunnel.clear();
            println!("Data received from wormhole {}", id);
            Ok(data)
        } else {
            Err("Wormhole not found".into());
        }
    }
}

#[derive(Clone)]
pub struct Wormhole {
    id: String,
    data_tunnel: Vec<u8>,
}
