pub mod ai_filter;

use tch::{nn, Device, Tensor};

pub struct AiFilter {
    model: nn::Sequential,
}

impl AiFilter {
    pub fn new() -> Result<Self, Box<dyn std::error::Error>> {
        let device = Device::Cpu;
        let model = nn::seq()
            .add(nn::linear(100, 50, Default::default()))
            .add_fn(|xs| xs.relu())
            .add(nn::linear(50, 2, Default::default())); // Output: 0=safe, 1=volatile
        Ok(Self { model })
    }

    pub async fn filter_input(&mut self, input: &str) -> Result<bool, Box<dyn std::error::Error>> {
        // Tokenize input (simplified) and predict
        let input_tensor = Tensor::randn(&[1, 100], (tch::Kind::Float, Device::Cpu)); // Mock tokenization
        let output = self.model.forward(&input_tensor);
        let prediction = output.argmax(1, false).int64_value(&[0]);
        if prediction == 1 {
            println!("Rejected volatile input: {}", input);
            Ok(false) // Reject
        } else {
            Ok(true) // Accept
        }
    }

    pub async fn filter_output(&mut self, output: &str) -> Result<bool, Box<dyn std::error::Error>> {
        // Same as input filter
        self.filter_input(output).await
    }
}
