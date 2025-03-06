# quantum_ml.py

import tensorflow as tf
import tensorflow_quantum as tfq
import cirq

def create_quantum_model():
    # Define a simple quantum circuit
    qubits = cirq.GridQubit.rect(1, 2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),  # Hadamard gate
        cirq.CNOT(qubits[0], qubits[1])  # CNOT gate
    )
    
    # Create a quantum layer
    model = tfq.layers.PQC(circuit, cirq.Z(qubits[1]))
    return model

def quantum_ml_model():
    # Create the quantum model
    model = create_quantum_model()
    
    # Example input data
    input_data = tfq.convert_to_tensor([cirq.Circuit(cirq.X(cirq.GridQubit(0, 0)))])
    
    # Get the output from the model
    output = model(input_data)
    print("Quantum ML Model Output:", output.numpy())

if __name__ == "__main__":
    quantum_ml_model()
