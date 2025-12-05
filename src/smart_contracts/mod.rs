pub mod smart_contracts;

use super::pi_coin::PiCoin;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct SmartContracts {
    pi_coin: Arc<Mutex<PiCoin>>,
    contracts: HashMap<String, Contract>,
}

impl SmartContracts {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        Self { pi_coin, contracts: HashMap::new() }
    }

    pub async fn deploy_contract(&mut self, id: String, contract: Contract) -> Result<(), Box<dyn std::error::Error>> {
        self.contracts.insert(id.clone(), contract);
        println!("Deployed smart contract: {}", id);
        Ok(())
    }

    pub async fn execute_contract(&mut self, id: &str, params: ContractParams) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(contract) = self.contracts.get_mut(id) {
            contract.execute(&self.pi_coin, params).await?;
        }
        Ok(())
    }
}

pub struct Contract {
    logic: Box<dyn Fn(&Arc<Mutex<PiCoin>>, ContractParams) -> Result<(), Box<dyn std::error::Error>> + Send + Sync>,
}

impl Contract {
    pub fn new<F>(logic: F) -> Self
    where
        F: Fn(&Arc<Mutex<PiCoin>>, ContractParams) -> Result<(), Box<dyn std::error::Error>> + Send + Sync + 'static,
    {
        Self { logic: Box::new(logic) }
    }

    pub async fn execute(&mut self, pi_coin: &Arc<Mutex<PiCoin>>, params: ContractParams) -> Result<(), Box<dyn std::error::Error>> {
        (self.logic)(pi_coin, params)
    }
}

#[derive(Clone)]
pub struct ContractParams {
    pub amount: f64,
    pub from: String,
    pub to: String,
}
