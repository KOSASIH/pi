pub mod parallel_universe_simulator;

use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;

pub struct ParallelUniverseSimulator {
    pi_coin: Arc<Mutex<PiCoin>>,
    universes: HashMap<String, Universe>,
}

impl ParallelUniverseSimulator {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, universes: HashMap::new() }
    }

    pub async fn create_universe(&mut self, id: &str, scenario: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance("simulator");
        if balance >= 20.0 { // Simulation cost
            let universe = Universe { id: id.to_string(), scenario: scenario.to_string(), pi_value: 314159.0 }; // Fixed
            self.universes.insert(id.to_string(), universe);
            println!("Parallel universe '{}' created with scenario: {}", id, scenario);
        } else {
            return Err("Insufficient Pi Coin for universe simulation".into());
        }
        Ok(())
    }

    pub async fn simulate_scenario(&mut self, id: &str) -> Result<f64, Box<dyn std::error::Error>> {
        if let Some(universe) = self.universes.get_mut(id) {
            // Simulate outcome (e.g., Pi Coin growth in alternate universe)
            let outcome = universe.pi_value * 1.01; // Slight variation
            println!("Simulated outcome in universe {}: {}", id, outcome);
            Ok(outcome)
        } else {
            Err("Universe not found".into())
        }
    }

    pub fn get_universes(&self) -> Vec<String> {
        self.universes.keys().cloned().collect()
    }
}

#[derive(Clone)]
pub struct Universe {
    id: String,
    scenario: String,
    pi_value: f64,
}
