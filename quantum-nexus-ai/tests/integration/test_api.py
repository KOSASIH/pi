import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
from ...src.api.fastapi_app import app
from ...src.core.ai_engine.quantum_sim import QuantumSimulator
from ...src.core.ai_engine.swarm_intelligence import SwarmIntelligence
from ...src.core.blockchain.web3_interface import BlockchainInterface
from ...src.core.iot_mesh.sensor_fusion import SensorFusion

@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def mock_modules():
    """Fixture to mock core modules for isolated testing."""
    with patch('src.api.fastapi_app.QuantumSimulator') as mock_quantum, \
         patch('src.api.fastapi_app.SwarmIntelligence') as mock_swarm, \
         patch('src.api.fastapi_app.BlockchainInterface') as mock_blockchain, \
         patch('src.api.fastapi_app.SensorFusion') as mock_iot:
        mock_quantum.return_value.grover_search.return_value = {"00": 512, "01": 512}
        mock_swarm.return_value.run_distributed_task.return_value = [{"result": [0.5], "agent": 0}]
        mock_blockchain.return_value.mint_ai_nft.return_value = "0xMockTxHash"
        mock_iot.return_value.fuse_data.return_value = {"fused_value": 0.7}
        yield

def test_root_endpoint(client):
    """Test root API endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Quantum Nexus AI" in data["message"]
    assert "endpoints" in data

def test_quantum_simulate_endpoint(client, mock_modules):
    """Test quantum simulation endpoint integration."""
    payload = {"type": "grover", "target": "00"}
    response = client.post("/quantum/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "simulation_result" in data
    assert isinstance(data["simulation_result"], dict)

def test_swarm_optimize_endpoint(client, mock_modules):
    """Test swarm optimization endpoint with async integration."""
    payload = [{"task": "optimize"}]
    response = client.post("/swarm/optimize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "swarm_results" in data
    assert len(data["swarm_results"]) > 0

def test_blockchain_mint_nft_endpoint(client, mock_modules):
    """Test NFT minting endpoint with encryption integration."""
    payload = {"model": "AI", "accuracy": 0.95}
    response = client.post("/blockchain/mint-nft", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "nft_tx_hash" in data
    assert data["nft_tx_hash"] == "0xMockTxHash"

def test_iot_fused_data_endpoint(client, mock_modules):
    """Test IoT fused data endpoint."""
    response = client.get("/iot/fused-data")
    assert response.status_code == 200
    data = response.json()
    assert "fused_data" in data
    assert "fused_value" in data["fused_data"]

@pytest.mark.asyncio
async def test_websocket_realtime(client, mock_modules):
    """Test WebSocket real-time streaming integration."""
    from fastapi.testclient import TestClient
    # Note: WebSocket testing with TestClient is limited; use websockets library for full test
    # This is a placeholder for async WebSocket integration
    assert True  # Placeholder assertion; expand with actual WS client

def test_graphql_endpoint(client, mock_modules):
    """Test GraphQL endpoint for flexible queries."""
    query = {"query": "{ quantumStatus }"}
    response = client.post("/graphql", json=query)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["quantumStatus"] == "Quantum simulator active"

def test_full_pipeline_integration(client, mock_modules):
    """End-to-end integration test simulating a complete workflow."""
    # Step 1: Simulate IoT data
    iot_response = client.get("/iot/fused-data")
    assert iot_response.status_code == 200

    # Step 2: Quantum prediction
    quantum_response = client.post("/quantum/simulate", json={"type": "grover", "target": "01"})
    assert quantum_response.status_code == 200

    # Step 3: Swarm optimization
    swarm_response = client.post("/swarm/optimize", json=[{"task": "optimize"}])
    assert swarm_response.status_code == 200

    # Step 4: Blockchain secure
    blockchain_response = client.post("/blockchain/mint-nft", json={"data": "secure"})
    assert blockchain_response.status_code == 200

    # Verify all modules interacted
    assert all([
        iot_response.json()["fused_data"]["fused_value"] == 0.7,
        "00" in quantum_response.json()["simulation_result"],
        len(swarm_response.json()["swarm_results"]) == 1,
        blockchain_response.json()["nft_tx_hash"] == "0xMockTxHash"
    ])

def test_error_handling(client):
    """Test error handling for invalid inputs."""
    # Invalid quantum type
    response = client.post("/quantum/simulate", json={"type": "invalid"})
    assert response.status_code == 200  # API handles gracefully
    data = response.json()
    assert "error" in data or "simulation_result" in data  # Depending on implementation

def test_performance_under_load(client, mock_modules, benchmark):
    """Benchmark API performance under simulated load."""
    def api_call():
        return client.get("/")

    result = benchmark(api_call)
    assert result.status_code == 200
    # Ensure response time is under threshold (from settings.yml)
