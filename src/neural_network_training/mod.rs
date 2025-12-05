pub mod neural_network_training;

use tch::{nn, Device, Tensor, Kind};
use std::sync::Arc;
use tokio::sync::Mutex;
use super::pi_coin::PiCoin;

pub struct NeuralNetworkTraining {
    pi_coin: Arc<Mutex<PiCoin>>,
    model: nn::Sequential,
    optimizer: nn::Optimizer,
}

impl NeuralNetworkTraining {
    pub fn new(pi_coin: Arc<Mutex<PiCoin>>) -> Self {
        let device = Device::Cpu;
        let vs = nn::VarStore::new(device);
        let model = nn::seq()
            .add(nn::linear(&vs.root(), 10, 50, Default::default()))
            .add_fn(|xs| xs.relu())
            .add(nn::linear(&vs.root(), 50, 1, Default::default()));
        let optimizer = nn::Adam::default().build(&vs, 1e-3).unwrap();
        Self { pi_coin, model, optimizer }
    }

    pub async fn train_on_pi_data(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Train on synthetic Pi Coin data (value fixed, but predict usage)
        let input = Tensor::randn(&[32, 10], (Kind::Float, Device::Cpu));
        let target = Tensor::randn(&[32, 1], (Kind::Float, Device::Cpu));
        let output = self.model.forward(&input);
        let loss = output.mse_loss(&target, tch::Reduction::Mean);
        self.optimizer.backward_step(&loss);
        println!("NN trained, loss: {:?}", loss);
        Ok(())
    }

    pub async fn predict_anomaly(&mut self) -> Result<f64, Box<dyn std::error::Error>> {
        let input = Tensor::randn(&[1, 10], (Kind::Float, Device::Cpu));
        let prediction = self.model.forward(&input).double_value(&[0]);
        println!("Anomaly prediction: {}", prediction);
        Ok(prediction)
    }
}
