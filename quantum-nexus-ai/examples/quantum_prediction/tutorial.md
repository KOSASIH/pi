# Quantum Prediction Demo Tutorial

## Overview
This tutorial guides you through running the **Quantum Prediction Demo** in Quantum Nexus AI, a hyper-tech integration of quantum simulations, swarm AI, blockchain security, and IoT data fusion for real-time stock market prediction and autonomous trading. By the end, you'll simulate a complete workflow, from data generation to secured trades.

**Prerequisites**:
- Python 3.9+
- Installed dependencies: `pip install -r requirements.txt`
- Optional: MQTT broker (e.g., Eclipse Mosquitto) for IoT simulation
- Optional: Ethereum testnet access for blockchain (set `PRIVATE_KEY` env var)

**Estimated Time**: 15-20 minutes

## Step 1: Set Up the Environment
1. Clone or navigate to the project: `cd pi/quantum-nexus-ai`
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables (for blockchain):
   ```bash
   export PRIVATE_KEY="your-testnet-private-key"
   export ENVIRONMENT="development"
   ```
4. (Optional) Start an MQTT broker: `docker run -p 1883:1883 eclipse-mosquitto`

## Step 2: Understand the Demo Components
The demo integrates:
- **IoT Fusion**: Generates synthetic market data (price, volume, sentiment).
- **Quantum Simulation**: Uses Grover's algorithm for trend prediction.
- **Swarm AI**: Optimizes trading decisions via distributed agents.
- **Blockchain**: Mints NFTs to secure trade data.
- **Visualization**: Real-time plots of prediction confidence.

Data flow: IoT → Quantum Predict → Swarm Optimize → Blockchain Secure → Visualize.

## Step 3: Run the Demo
1. Navigate to the demo folder: `cd examples/quantum_prediction`
2. Execute the demo: `python demo.py`
3. Observe the output:
   - IoT data generation and fusion.
   - Quantum prediction results (e.g., "bullish" or "bearish").
   - Swarm optimization with agent consensus.
   - Blockchain NFT minting (TX hash).
   - Matplotlib visualization of confidence over time.

**Sample Output**:
```
Starting Quantum Prediction Demo...
Generated market data shape: (20, 3)
Quantum Prediction: {'trend': 'bullish', 'confidence': 0.65, 'quantum_counts': {'00': 512, '01': 512}}
Swarm Trading Plan: [{'action': 'buy', 'agents_agreeing': 6, 'swarm_details': [...]}]
Trade Secured on Blockchain: TX 0xMockTxHash
Demo completed! All hyper-tech modules integrated.
```

## Step 4: Customize the Demo
- **Modify Data Input**: Edit `generate_market_data()` to use real APIs (e.g., Alpha Vantage for stock data).
- **Adjust Quantum Parameters**: Change `target_state` in `quantum_enhanced_prediction()` for different predictions.
- **Scale Swarm**: Increase `num_agents` in `SwarmIntelligence` for more distributed decisions.
- **Blockchain Integration**: Replace mock with real Web3 calls for testnet transactions.
- **Add Autonomous Actions**: Extend `autonomous_control()` to trigger real trades via APIs.

## Step 5: Integrate with API/CLI
- **API Mode**: Run the API (`uvicorn src.api.fastapi_app:app`) and call endpoints like `/quantum/simulate` for predictions.
- **CLI Mode**: Use `python src.cli.nexus_cli.py quantum --type grover --target 00` for command-line simulations.
- **Full Pipeline**: Combine demo with API for real-time streaming via WebSocket.

## Step 6: Visualize and Analyze
- The demo includes Matplotlib for live plots. For advanced viz, integrate with Grafana (from docker-compose).
- Analyze results: High confidence (>0.7) indicates strong quantum-enhanced predictions.
- Benchmark: Time the demo to measure hyper-tech performance.

## Troubleshooting
- **Import Errors**: Ensure all modules are in `PYTHONPATH` or run from project root.
- **Blockchain Failures**: Check testnet connection and gas fees.
- **IoT Issues**: Verify MQTT broker is running and ports are open.
- **Performance**: On low-end hardware, reduce `num_qubits` or `num_agents`.

## Next Steps in Hyper-Tech Exploration
- Extend to real financial data for live trading (use with caution).
- Add AR/VR viz for immersive quantum simulations.
- Deploy on Kubernetes for scalable production.

For code details, see `demo.py`. Contributions welcome—fork and enhance!
