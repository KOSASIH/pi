pub mod pi_network;

use super::pi_coin::PiCoin;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::net::TcpStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

pub struct PiNetwork {
    pi_coin: Arc<Mutex<PiCoin>>,
    connection: Option<TcpStream>,
}

impl PiNetwork {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, connection: None }
    }

    pub async fn connect(&mut self, node_url: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Connect to Pi Network node (internal only, filtered by AI)
        let stream = TcpStream::connect(node_url).await?;
        self.connection = Some(stream);
        println!("Connected to Pi Network node: {}", node_url);
        Ok(())
    }

    pub async fn mine_pi(&mut self, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Simulate mining from Pi Network (original source)
        if let Some(ref mut stream) = self.connection {
            stream.write_all(b"MINE_REQUEST").await?;
            let mut buffer = [0; 1024];
            let n = stream.read(&mut buffer).await?;
            let mined = String::from_utf8_lossy(&buffer[..n]).parse::<f64>().unwrap_or(0.0);
            self.pi_coin.lock().await.mine(user, mined);
        }
        Ok(())
    }

    pub async fn claim_rewards(&mut self, user: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Claim contribution rewards from Pi Network
        if let Some(ref mut stream) = self.connection {
            stream.write_all(b"CLAIM_REWARDS").await?;
            let mut buffer = [0; 1024];
            let n = stream.read(&mut buffer).await?;
            let reward = String::from_utf8_lossy(&buffer[..n]).parse::<f64>().unwrap_or(0.0);
            self.pi_coin.lock().await.reward_contribution(user, reward);
        }
        Ok(())
    }

    pub async fn p2p_exchange(&mut self, from: &str, to: &str, amount: f64) -> Result<(), Box<dyn std::error::Error>> {
        // P2P transfer via Pi Network
        self.pi_coin.lock().await.p2p_transfer(from, to, amount)?;
        println!("P2P exchange via Pi Network: {} PI from {} to {}", amount, from, to);
        Ok(())
    }
}
