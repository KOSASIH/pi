pub mod time_travel_simulation;

use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct TimeTravelSimulation {
    pi_coin: Arc<Mutex<PiCoin>>,
    timelines: Vec<Timeline>,
}

impl TimeTravelSimulation {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, timelines: Vec::new() }
    }

    pub async fn simulate_future(&mut self, years: u32) -> Result<(), Box<dyn std::error::Error>> {
        // Predict Pi Coin growth (fixed value, but simulate rewards)
        let future_balance = 100.0 + (years as f64 * 10.0); // Linear simulation
        let timeline = Timeline { year: years, pi_balance: future_balance };
        self.timelines.push(timeline);
        println!("Simulated future: {} PI in {} years", future_balance, years);
        Ok(())
    }

    pub async fn rewind_to_past(&mut self, year: u32) -> Result<(), Box<dyn std::error::Error>> {
        // Simulate rollback (for recovery)
        self.timelines.retain(|t| t.year <= year);
        println!("Rewound to year {}", year);
        Ok(())
    }

    pub fn get_timelines(&self) -> Vec<Timeline> {
        self.timelines.clone()
    }
}

#[derive(Clone)]
pub struct Timeline {
    year: u32,
    pi_balance: f64,
}
