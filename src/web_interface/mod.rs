pub mod web_interface;

use hyper::{Body, Request, Response, Server};
use hyper::service::{make_service_fn, service_fn};
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct WebServer {
    hypervisor: Arc<Mutex<super::hypervisor::Hypervisor>>,
    network: Arc<Mutex<super::network::NetworkManager>>,
    gpu: Arc<Mutex<super::gpu::GpuAccelerator>>,
    ai: Arc<Mutex<super::ai_orchestrator::AiOrchestrator>>,
}

impl WebServer {
    pub fn new(hypervisor: Arc<Mutex<super::hypervisor::Hypervisor>>, network: Arc<Mutex<super::network::NetworkManager>>, gpu: Arc<Mutex<super::gpu::GpuAccelerator>>, ai: Arc<Mutex<super::ai_orchestrator::AiOrchestrator>>) -> Self {
        Self { hypervisor, network, gpu, ai }
    }

    pub async fn run(self) -> Result<(), Box<dyn std::error::Error>> {
        let make_svc = make_service_fn(|_conn| {
            let hypervisor = self.hypervisor.clone();
            async { Ok::<_, hyper::Error>(service_fn(move |req| handle_request(req, hypervisor.clone()))) }
        });

        let addr = ([127, 0, 0, 1], 3000).into();
        let server = Server::bind(&addr).serve(make_svc);
        println!("Web interface running on http://127.0.0.1:3000");
        server.await?;
        Ok(())
    }
}

async fn handle_request(_req: Request<Body>, _hypervisor: Arc<Mutex<super::hypervisor::Hypervisor>>) -> Result<Response<Body>, hyper::Error> {
    // Serve HTML dashboard with VM stats
    Ok(Response::new(Body::from("<html><body><h1>Hyper-Pi Dashboard</h1><p>VMs: Active</p></body></html>")))
}
