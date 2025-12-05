pub mod blockchain_internal;

use super::pi_coin::PiCoin;
use std::collections::VecDeque;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct BlockchainInternal {
    pi_coin: Arc<Mutex<PiCoin>>,
    blocks: VecDeque<Block>,
}

impl BlockchainInternal {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, blocks: VecDeque::new() }
    }

    pub async fn add_block(&mut self, transactions: Vec<Transaction>) -> Result<(), Box<dyn std::error::Error>> {
        let prev_hash = self.blocks.back().map(|b| b.hash.clone()).unwrap_or("genesis".to_string());
        let block = Block::new(transactions, prev_hash);
        self.blocks.push_back(block);
        println!("Added block to internal blockchain");
        Ok(())
    }

    pub async fn mine_block(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Simulate mining for Pi Coin
        self.pi_coin.lock().await.mine("miner", 0.1);
        println!("Mined block on internal blockchain");
        Ok(())
    }

    pub fn verify_chain(&self) -> bool {
        // Simple verification
        true // Assume valid
    }
}

pub struct Block {
    transactions: Vec<Transaction>,
    hash: String,
}

impl Block {
    pub fn new(transactions: Vec<Transaction>, prev_hash: String) -> Self {
        let hash = format!("hash_{}", prev_hash); // Simplified
        Self { transactions, hash }
    }
}

pub struct Transaction {
    from: String,
    to: String,
    amount: f64,
}
