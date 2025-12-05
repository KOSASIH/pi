pub mod gpu;

use rpi_gpu::{GpuContext, Shader};

pub struct GpuAccelerator {
    context: GpuContext,
}

impl GpuAccelerator {
    pub fn new() -> Result<Self, Box<dyn std::error::Error>> {
        let context = GpuContext::new()?;
        Ok(Self { context })
    }

    pub async fn accelerate_tasks(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Compile and run shader for VM graphics
        let shader = Shader::from_source("vec4 main() { return vec4(1.0); }")?;
        self.context.run_shader(&shader)?;
        println!("GPU acceleration applied");
        Ok(())
    }
}
