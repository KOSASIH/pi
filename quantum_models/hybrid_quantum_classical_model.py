# hybrid_quantum_classical_model.py

import tensorflow as tf
import tensorflow_quantum as tfq
import cirq

# Define a simple quantum circuit
def create_quantum_circuit(qubits):
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))  # Hadamard gate
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))  # CNOT gate
    return circuit

# Define a hybrid model
class HybridQuantumClassicalModel(tf.keras.Model):
    def __init__(self):
        super(HybridQuantumClassicalModel, self).__init__()
        self.qubits = cirq.GridQubit.rect(1, 2)
        self.circuit = create_quantum_circuit(self.qubits)
        self.quantum_layer = tfq.layers.PQC(self.circuit, cirq.Z(self.qubits[1]))
        self.classical_layer = tf.keras.layers.Dense(10, activation='relu')

    def call(self, inputs):
        quantum_output = self.quantum_layer(inputs)
        classical_output = self.classical_layer(quantum_output)
        return classical_output

# Example usage
if __name__ == "__main__":
    hybrid_model = HybridQuantumClassicalModel()
    input_data = tfq.convert_to_tensor([cirq.Circuit(cirq.X(cirq.GridQubit(0, 0)))])
    output = hybrid_model(input_data)
    print("Hybrid Model Output:", output.numpy())
