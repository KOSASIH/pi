pub mod dimensional_portals;

use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;

pub struct DimensionalPortals {
    pi_coin: Arc<Mutex<PiCoin>>,
    portals: HashMap<String, Dimension>,
}

impl DimensionalPortals {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, portals: HashMap::new() }
    }

    pub async fn open_portal(&mut self, dimension_name: &str, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 10.0 { // Portal fee
            let dimension = Dimension { name: dimension_name.to_string(), data: vec!["Portal data".to_string()] };
            self.portals.insert(dimension_name.to_string(), dimension);
            println!("Portal to dimension '{}' opened for {}", dimension_name, user);
        } else {
            return Err("Insufficient Pi Coin for portal".into());
        }
        Ok(())
    }

    pub async fn traverse_portal(&mut self, dimension_name: &str) -> Result<Vec<String>, Box<dyn std::error::Error>> {
        if let Some(dimension) = self.portals.get(dimension_name) {
            println!("Traversed to dimension: {}", dimension_name);
            Ok(dimension.data.clone())
        } else {
            Err("Portal not found".into())
        }
    }

    pub fn list_portals(&self) -> Vec<String> {
        self.portals.keys().cloned().collect()
    }
}

#[derive(Clone)]
pub struct Dimension {
    name: String,
    data: Vec<String>,
}
