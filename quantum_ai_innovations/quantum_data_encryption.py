# quantum_data_encryption.py

import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram

class QuantumDataEncryption:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')

    def generate_key(self, length):
        """Generate a random binary key of specified length."""
        return np.random.randint(2, size=length)

    def encode_message(self, message, key):
        """Encode the message using the key."""
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        encoded_message = ''.join(str(int(bm) ^ k) for bm, k in zip(binary_message, key))
        return encoded_message

    def encrypt_data(self, message):
        """Encrypt the message using quantum key distribution."""
        key_length = len(message) * 8  # Length of the key should match the message length in bits
        key = self.generate_key(key_length)

        # Create a quantum circuit for QKD
        circuit = QuantumCircuit(key_length, key_length)

        # Prepare the quantum states based on the key
        for i in range(key_length):
            if key[i] == 1:
                circuit.x(i)  # Apply X gate for '1'

        # Apply Hadamard gates to create superposition
        circuit.h(range(key_length))

        # Measure the circuit
        circuit.measure(range(key_length), range(key_length))

        # Execute the circuit
        transpiled_circuit = transpile(circuit, self.backend)
        qobj = assemble(transpiled_circuit)
        result = execute(qobj, self.backend).result()
        counts = result.get_counts()

        # Extract the key from the measurement results
        measured_key = max(counts, key=counts.get)  # Get the most frequent measurement
        measured_key = [int(bit) for bit in measured_key]  # Convert to list of integers

        # Encrypt the message using the measured key
        encrypted_message = self.encode_message(message, measured_key)
        return encrypted_message, measured_key

    def decrypt_data(self, encrypted_message, key):
        """Decrypt the message using the key."""
        decrypted_message = ''.join(str(int(em) ^ k) for em, k in zip(encrypted_message, key))
        # Convert binary string back to characters
        decrypted_chars = [chr(int(decrypted_message[i:i + 8], 2)) for i in range(0, len(decrypted_message), 8)]
        return ''.join(decrypted_chars)

if __name__ == "__main__":
    qde = QuantumDataEncryption()

    # Example message
    message = "Hello, Pi Coin!"

    # Encrypt the message
    encrypted_message, key = qde.encrypt_data(message)
    print("Encrypted Message:", encrypted_message)
    print("Key Used for Encryption:", key)

    # Decrypt the message
    decrypted_message = qde.decrypt_data(encrypted_message, key)
    print("Decrypted Message:", decrypted_message)
