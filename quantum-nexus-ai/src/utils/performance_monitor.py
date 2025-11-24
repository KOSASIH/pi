import time
import psutil
import asyncio
from typing import Dict, List, Callable
import logging
from prometheus_client import Gauge, Counter, Histogram, start_http_server
import threading
from ..core.ai_engine.quantum_sim import QuantumSimulator
from ..core.ai_engine.swarm_intelligence import SwarmIntelligence
from ..core.blockchain.web3_interface import BlockchainInterface
from ..core.iot_mesh.sensor_fusion import SensorFusion

# Prometheus Metrics
QUANTUM_SIM_TIME = Histogram('quantum_sim_duration_seconds', 'Time for quantum simulations', ['algorithm'])
SWARM_OPTIMIZE_TIME = Histogram('swarm_optimize_duration_seconds', 'Time for swarm optimizations', ['num_agents'])
BLOCKCHAIN_TX_TIME = Histogram('blockchain_tx_duration_seconds', 'Time for blockchain transactions', ['action'])
IOT_FUSION_TIME = Histogram('iot_fusion_duration_seconds', 'Time for IoT data fusion')
CPU_USAGE = Gauge('cpu_usage_percent', 'Current CPU usage')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Current memory usage')
API_REQUESTS = Counter('api_requests_total', 'Total API requests', ['endpoint'])

class PerformanceMonitor:
    """Ultimate hyper-tech performance monitoring utility for real-time tracking of system metrics, including Prometheus integration for quantum AI, swarm, blockchain, and IoT workloads."""
    
    def __init__(self, prometheus_port=8001):
        self.prometheus_port = prometheus_port
        self.quantum = QuantumSimulator()
        self.swarm = SwarmIntelligence()
        self.blockchain = BlockchainInterface()
        self.iot = SensorFusion()
        self.logger = logging.getLogger(__name__)
        self.callbacks: List[Callable] = []
        self.monitoring_active = False
    
    def start_prometheus_server(self):
        """Start Prometheus metrics server in a background thread."""
        start_http_server(self.prometheus_port)
        self.logger.info(f"Prometheus metrics server started on port {self.prometheus_port}")
    
    def add_callback(self, callback: Callable):
        """Add callback for custom monitoring actions (e.g., alerts)."""
        self.callbacks.append(callback)
    
    async def monitor_system_resources(self):
        """Continuously monitor CPU and memory usage."""
        while self.monitoring_active:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            CPU_USAGE.set(cpu)
            MEMORY_USAGE.set(memory)
            self.logger.debug(f"CPU: {cpu}%, Memory: {memory}%")
            for callback in self.callbacks:
                await callback({"cpu": cpu, "memory": memory})
            await asyncio.sleep(5)
    
    async def benchmark_quantum_sim(self, algorithm="grover", target="00", runs=10):
        """Benchmark quantum simulation performance."""
        times = []
        for _ in range(runs):
            start = time.time()
            if algorithm == "grover":
                self.quantum.grover_search(target)
            elif algorithm == "shor":
                self.quantum.shor_factorization(15)
            duration = time.time() - start
            times.append(duration)
            QUANTUM_SIM_TIME.labels(algorithm).observe(duration)
        avg_time = sum(times) / len(times)
        self.logger.info(f"Quantum {algorithm} avg time: {avg_time:.4f}s over {runs} runs")
        return {"algorithm": algorithm, "avg_time": avg_time, "runs": runs}
    
    async def benchmark_swarm_optimize(self, num_agents=10, runs=5):
        """Benchmark swarm intelligence optimization."""
        self.swarm.num_agents = num_agents
        times = []
        for _ in range(runs):
            start = time.time()
            tasks = [{"task": "optimize"} for _ in range(num_agents)]
            await self.swarm.run_distributed_task(tasks)
            duration = time.time() - start
            times.append(duration)
            SWARM_OPTIMIZE_TIME.labels(str(num_agents)).observe(duration)
        avg_time = sum(times) / len(times)
        self.logger.info(f"Swarm optimize avg time: {avg_time:.4f}s for {num_agents} agents over {runs} runs")
        return {"num_agents": num_agents, "avg_time": avg_time, "runs": runs}
    
    async def benchmark_blockchain_tx(self, action="mint-nft", runs=3):
        """Benchmark blockchain transaction times."""
        times = []
        for _ in range(runs):
            start = time.time()
            if action == "mint-nft":
                await self.blockchain.mint_ai_nft({"test": "data"})
            elif action == "transfer":
                self.blockchain.transfer_tokens("0xRecipient", 0.001)
            duration = time.time() - start
            times.append(duration)
            BLOCKCHAIN_TX_TIME.labels(action).observe(duration)
        avg_time = sum(times) / len(times)
        self.logger.info(f"Blockchain {action} avg time: {avg_time:.4f}s over {runs} runs")
        return {"action": action, "avg_time": avg_time, "runs": runs}
    
    async def benchmark_iot_fusion(self, runs=10):
        """Benchmark IoT sensor fusion."""
        times = []
        for _ in range(runs):
            start = time.time()
            self.iot.fuse_data()
            duration = time.time() - start
            times.append(duration)
            IOT_FUSION_TIME.observe(duration)
        avg_time = sum(times) / len(times)
        self.logger.info(f"IoT fusion avg time: {avg_time:.4f}s over {runs} runs")
        return {"avg_time": avg_time, "runs": runs}
    
    def track_api_request(self, endpoint: str):
        """Track API request counts."""
        API_REQUESTS.labels(endpoint).inc()
    
    async def run_full_benchmark(self):
        """Run comprehensive benchmarks for all modules."""
        self.logger.info("Starting full hyper-tech benchmark...")
        results = {}
        results["quantum"] = await self.benchmark_quantum_sim()
        results["swarm"] = await self.benchmark_swarm_optimize()
        results["blockchain"] = await self.benchmark_blockchain_tx()
        results["iot"] = await self.benchmark_iot_fusion()
        self.logger.info(f"Benchmark results: {results}")
        return results
    
    async def start_monitoring(self):
        """Start all monitoring tasks asynchronously."""
        self.monitoring_active = True
        threading.Thread(target=self.start_prometheus_server, daemon=True).start()
        await asyncio.gather(
            self.monitor_system_resources(),
            self.run_full_benchmark()
        )
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring_active = False
        self.logger.info("Monitoring stopped.")

# Example usage
if __name__ == "__main__":
    monitor = PerformanceMonitor()
    asyncio.run(monitor.run_full_benchmark())
    # For continuous monitoring: asyncio.run(monitor.start_monitoring())
