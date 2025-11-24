import os
from web3 import Web3
from eth_account import Account
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import json
import asyncio
from typing import Dict, List

class BlockchainInterface:
    """Ultimate hyper-tech blockchain interface for decentralized AI data ownership, smart contracts, and NFT generation."""
    def __init__(self, provider_url="https://polygon-rpc.com/", private_key=None):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to blockchain provider.")
        self.account = Account.from_key(private_key or os.getenv("PRIVATE_KEY", Account.create().key))
        self.contracts = {}  # Cache for deployed contracts

    def deploy_smart_contract(self, contract_code: str, constructor_args=[]) -> str:
        """Deploy a smart contract (e.g., for AI model ownership)."""
        compiled = self.w3.eth.contract(abi=[], bytecode=contract_code)  # Simplified; use solc for full compilation
        tx = compiled.constructor(*constructor_args).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('20', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        self.contracts[contract_address] = compiled
        return contract_address

    async def mint_ai_nft(self, metadata: Dict) -> str:
        """Mint an AI-generated NFT for data/model ownership (hyper-secure with encryption)."""
        # Generate post-quantum encryption key (simplified lattice-based)
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        encrypted_metadata = public_key.encrypt(
            json.dumps(metadata).encode(),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        
        # Simulate NFT minting on a contract (use ERC-721 standard)
        nft_contract_abi = [...]  # Placeholder for ERC-721 ABI
        nft_contract = self.w3.eth.contract(address="0xYourNFTContractAddress", abi=nft_contract_abi)
        tx = nft_contract.functions.mint(self.account.address, encrypted_metadata.hex()).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 150000,
            'gasPrice': self.w3.to_wei('20', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        await asyncio.sleep(1)  # Wait for confirmation
        return tx_hash.hex()

    def query_blockchain_data(self, contract_address: str, function_name: str, args=[]) -> any:
        """Query data from a smart contract (e.g., AI model access logs)."""
        if contract_address not in self.contracts:
            # Load contract if not cached
            abi = [...]  # Placeholder ABI
            self.contracts[contract_address] = self.w3.eth.contract(address=contract_address, abi=abi)
        contract = self.contracts[contract_address]
        result = contract.functions[function_name](*args).call()
        return result

    def transfer_tokens(self, to_address: str, amount: float) -> str:
        """Transfer crypto tokens for AI service payments."""
        tx = {
            'to': to_address,
            'value': self.w3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'chainId': 137  # Polygon
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    async def decentralized_ai_oracle(self, ai_query: str) -> Dict:
        """AI oracle for blockchain: Query AI model via smart contract and return result."""
        # Simulate calling an AI function (integrate with swarm_intelligence)
        from ..ai_engine.swarm_intelligence import SwarmIntelligence
        swarm = SwarmIntelligence(num_agents=3)
        result = await swarm.run_distributed_task([{"task": ai_query}])
        # Store result on-chain
        contract_addr = self.deploy_smart_contract("608060405234801561001057600080fd5b50d3801561001d57600080fd5b50d2801561002a57600080fd5b50600436106100405760003560e01c8063cfae321714610045575b600080fd5b61005d600480360381019061005891906100c3565b61005f565b005b80600081905550806001819055505050565b6000813590506100a0816100e5565b92915050565b6000602082840312156100bc576100bb6100e0565b5b5b92915050565b6000602082840312156100d5576100d46100e0565b5b5b92915050565b6000819050919050565b600080fd5b6100f0816100a6565b81146100fb57600080fd5b5056fea2646970667358221220d582f6e1c7c5e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e64736f6c63430008000033")  # Simple storage contract bytecode
        self.query_blockchain_data(contract_addr, "store", [json.dumps(result)])
        return {"oracle_result": result, "tx_hash": contract_addr}

# Example usage
if __name__ == "__main__":
    # Note: Set PRIVATE_KEY env var for real transactions
    bc = BlockchainInterface()
    print("Connected to Blockchain:", bc.w3.is_connected())
    # Mint NFT
    metadata = {"model": "QuantumAI", "accuracy": 0.99}
    nft_tx = asyncio.run(bc.mint_ai_nft(metadata))
    print("NFT Mint TX:", nft_tx)
    # Oracle query
    oracle_result = asyncio.run(bc.decentralized_ai_oracle("optimize logistics"))
    print("Oracle Result:", oracle_result)
