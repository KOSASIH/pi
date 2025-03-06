# quantum_network_simulation.py

import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

class QuantumNetworkSimulation:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')

    def prepare_quantum_state(self, message):
        """Prepare a quantum state based on the binary representation of the message."""
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        circuit = QuantumCircuit(len(binary_message), len(binary_message))

        # Prepare the quantum states based on the binary message
        for i in range(len(binary_message)):
            if binary_message[i] == '1':
                circuit.x(i)  # Apply X gate for '1'

        # Apply Hadamard gates to create superposition
        circuit.h(range(len(binary_message)))

        return circuit

    def entangle_qubits(self, qubit1, qubit2):
        """Create entangled qubits."""
        circuit = QuantumCircuit(2)
        circuit.h(qubit1)  # Apply Hadamard to the first qubit
        circuit.cx(qubit1, qubit2)  # Apply CNOT to entangle
        return circuit

    def measure_circuit(self, circuit):
        """Measure the quantum circuit."""
        circuit.measure_all()
        return circuit

    def simulate_quantum_communication(self, message):
        """Simulate quantum communication of a message."""
        circuit = self.prepare_quantum_state(message)
        circuit = self.measure_circuit(circuit)

        # Execute the circuit
        result = execute(circuit, self.backend).result()
        counts = result.get_counts()

        return counts

    def simulate_entangled_communication(self):
        """Simulate communication using entangled qubits."""
        circuit = self.entangle_qubits(0, 1)
        circuit = self.measure_circuit(circuit)

        # Execute the circuit
        result = execute(circuit, self.backend).result()
        counts = result.get_counts()

        return counts

if __name__ == "__main__":
    simulator = QuantumNetworkSimulation()

    # Simulate quantum communication of a message
    message = "Hi"
    result = simulator.simulate_quantum_communication(message)
    print("Quantum Communication Result:", result)
    plot_histogram(result)
    plt.title("Quantum Communication Result")
    plt.show()

    # Simulate entangled communication
    entangled_result = simulator.simulate_entangled_communication()
    print("Entangled Communication Result:", entangled_result)
    plot_histogram(entangled_result)
    plt.title("Entangled Communication Result")
    plt.show()
