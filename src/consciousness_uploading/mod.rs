pub mod consciousness_uploading;

use super::data_storage::DataStorage;
use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct ConsciousnessUploading {
    storage: Arc<Mutex<DataStorage>>,
    pi_coin: Arc<Mutex<PiCoin>>,
    uploaded_minds: Vec<MindBackup>,
}

impl ConsciousnessUploading {
    pub fn new(storage: Arc<Mutex<DataStorage>>, pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { storage, pi_coin, uploaded_minds: Vec::new() }
    }

    pub async fn upload_consciousness(&mut self, user: &str, mind_data: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
        let balance = self.pi_coin.lock().await.get_balance(user);
        if balance >= 200.0 { // High cost for uploading
            self.storage.lock().await.store_data(&format!("mind_{}", user), mind_data).await?;
            let backup = MindBackup { user: user.to_string(), data_size: mind_data.len() };
            self.uploaded_minds.push(backup);
            println!("Consciousness uploaded for {}: {} bytes", user, mind_data.len());
        } else {
            return Err("Insufficient Pi Coin for consciousness uploading".into());
        }
        Ok(())
    }

    pub async fn revive_consciousness(&mut self, user: &str) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
        let data = self.storage.lock().await.retrieve_data(&format!("mind_{}", user)).await?;
        println!("Consciousness revived for {}", user);
        Ok(data)
    }

    pub fn get_uploaded_minds(&self) -> Vec<MindBackup> {
        self.uploaded_minds.clone()
    }
}

#[derive(Clone)]
pub struct MindBackup {
    user: String,
    data_size: usize,
}
