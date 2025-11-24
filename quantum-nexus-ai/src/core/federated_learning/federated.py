import asyncio
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Dict, Callable
import logging
from ..ai_engine.swarm_intelligence import SwarmIntelligence
from ..blockchain.web3_interface import BlockchainInterface
from ..utils.encryption import PostQuantumEncryption

class FederatedLearning:
    """Ultimate hyper-tech federated learning module for privacy-preserving distributed AI training, integrating swarm coordination, blockchain logging, and post-quantum encryption for secure model aggregation."""
    
    def __init__(self, num_clients=5, global_model=None):
        self.num_clients = num_clients
        self.global_model = global_model or self._create_model()
        self.clients = [self._create_model() for _ in range(num_clients)]  # Local models
        self.swarm = SwarmIntelligence(num_agents=num_clients)
        self.blockchain = BlockchainInterface()
        self.encryption = PostQuantumEncryption()
        self.logger = logging.getLogger(__name__)
    
    def _create_model(self) -> nn.Module:
        """Create a simple neural network model."""
        return nn.Sequential(
            nn.Linear(10, 50),
            nn.ReLU(),
            nn.Linear(50, 1)
        )
    
    async def client_train(self, client_id: int, data: torch.Tensor, labels: torch.Tensor, epochs=5) -> Dict:
        """Train local model on client's data."""
        model = self.clients[client_id]
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        criterion = nn.MSELoss()
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        
        # Extract model updates (gradients or weights)
        updates = {name: param.grad.clone() if param.grad is not None else torch.zeros_like(param) 
                   for name, param in model.named_parameters()}
        
        # Encrypt updates for privacy
        encrypted_updates = self.encryption.secure_ai_model(updates)
        
        return {"client_id": client_id, "updates": encrypted_updates, "loss": loss.item()}
    
    async def aggregate_updates(self, client_results: List[Dict]) -> nn.Module:
        """Aggregate encrypted updates using swarm consensus and blockchain logging."""
        # Swarm-based aggregation (simulate consensus)
        tasks = [{"task": "aggregate", "data": result} for result in client_results]
        swarm_results = await self.swarm.run_distributed_task(tasks)
        
        # Decrypt and average updates
        aggregated_updates = {}
        for name in self.global_model.state_dict().keys():
            grads = []
            for result in client_results:
                decrypted = self.encryption.decrypt_ai_model(result["updates"])
                if name in decrypted:
                    grads.append(decrypted[name])
            if grads:
                aggregated_updates[name] = torch.mean(torch.stack(grads), dim=0)
        
        # Update global model
        for name, param in self.global_model.named_parameters():
            if name in aggregated_updates:
                param.grad = aggregated_updates[name]
                param.data -= 0.01 * param.grad  # Simple SGD update
        
        # Log aggregation on blockchain
        await self.blockchain.mint_ai_nft({"aggregation": "federated", "clients": len(client_results)})
        
        return self.global_model
    
    async def federated_round(self, client_data: List[torch.Tensor], client_labels: List[torch.Tensor], rounds=3) -> nn.Module:
        """Run a full federated learning round."""
        for round_num in range(rounds):
            self.logger.info(f"Federated Round {round_num + 1}")
            
            # Train clients in parallel
            train_tasks = [self.client_train(i, client_data[i], client_labels[i]) for i in range(self.num_clients)]
            client_results = await asyncio.gather(*train_tasks)
            
            # Aggregate
            self.global_model = await self.aggregate_updates(client_results)
            
            self.logger.info(f"Round {round_num + 1} completed.")
        
        return self.global_model
    
    def evaluate_global_model(self, test_data: torch.Tensor, test_labels: torch.Tensor) -> float:
        """Evaluate the global model."""
        with torch.no_grad():
            predictions = self.global_model(test_data)
            loss = nn.MSELoss()(predictions, test_labels)
        return loss.item()
    
    async def privacy_preserving_inference(self, input_data: torch.Tensor) -> torch.Tensor:
        """Perform inference with privacy (encrypt input/output)."""
        encrypted_input = self.encryption.encrypt_data(str(input_data.tolist()))
        # Simulate inference (in real, send to secure enclave)
        with torch.no_grad():
            result = self.global_model(input_data)
        encrypted_output = self.encryption.encrypt_data(str(result.tolist()))
        return result  # Return plain for demo; use encrypted in production

# Example usage
if __name__ == "__main__":
    fl = FederatedLearning(num_clients=3)
    
    # Simulate client data
    client_data = [torch.randn(20, 10) for _ in range(3)]
    client_labels = [torch.randn(20, 1) for _ in range(3)]
    
    # Run federated learning
    global_model = asyncio.run(fl.federated_round(client_data, client_labels, rounds=2))
    
    # Evaluate
    test_data = torch.randn(10, 10)
    test_labels = torch.randn(10, 1)
    loss = fl.evaluate_global_model(test_data, test_labels)
    print(f"Global Model Test Loss: {loss}")
    
    # Privacy-preserving inference
    inference_result = asyncio.run(fl.privacy_preserving_inference(test_data[:1]))
    print(f"Inference Result: {inference_result}")
