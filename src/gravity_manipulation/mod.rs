pub mod gravity_manipulation;

use super::pi_coin::PiCoin;
use super::resource_manager::ResourceManager;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct GravityManipulation {
    pi_coin: Arc<Mutex<PiCoin>>,
    resource_manager: Arc<Mutex<ResourceManager>>,
    gravitational_fields: Vec<GravitationalField>,
}

impl GravityManipulation {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>, resource_manager: Arc<Mutex<ResourceManager>>) -> Self {
        Self { pi_coin, resource_manager, gravitational_fields: Vec::new() }
    }

    pub async fn apply_gravity(&mut self, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        let gravity_strength = balance / 314159.0; // Based on Pi value
        let field = GravitationalField { user: user.to_string(), strength: gravity_strength };
        self.gravitational_fields.push(field);
        // Allocate resources based on gravity
        self.resource_manager.lock().await.allocate_resource(user, "cpu").await?;
        println!("Gravity applied for {}: strength {}", user, gravity_strength);
        Ok(())
    }

    pub async fn simulate_gravitational_pull(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        for field in &self.gravitational_fields {
            // Simulate resource attraction
            println!("Pulling resources towards {} with gravity {}", field.user, field.strength);
        }
        Ok(())
    }
}

#[derive(Clone)]
pub struct GravitationalField {
    user: String,
    strength: f64,
}
