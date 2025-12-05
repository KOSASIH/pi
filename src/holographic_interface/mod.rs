pub mod holographic_interface;

use super::gpu::GpuAccelerator;
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct HolographicInterface {
    gpu: Arc<Mutex<GpuAccelerator>>,
    holograms: Vec<Hologram>,
}

impl HolographicInterface {
    pub fn new(gpu: Arc<Mutex<GpuAccelerator>>) -> Self {
        Self { gpu, holograms: Vec::new() }
    }

    pub async fn render_hologram(&mut self, data: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Simulate 3D rendering with GPU
        self.gpu.lock().await.accelerate_tasks().await?;
        let hologram = Hologram { data: data.to_string(), position: [0.0, 0.0, 0.0] };
        self.holograms.push(hologram);
        println!("Hologram rendered for: {}", data);
        Ok(())
    }

    pub async fn update_hologram_position(&mut self, index: usize, pos: [f64; 3]) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(holo) = self.holograms.get_mut(index) {
            holo.position = pos;
            println!("Hologram position updated");
        }
        Ok(())
    }

    pub fn get_holograms(&self) -> Vec<Hologram> {
        self.holograms.clone()
    }
}

#[derive(Clone)]
pub struct Hologram {
    data: String,
    position: [f64; 3],
}
