# quantum_data_visualization.py

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuantumDataVisualization:
    def __init__(self):
        self.backend = Aer.get_backend('statevector_simulator')

    def prepare_quantum_state(self, data):
        """Prepare a quantum state based on input data."""
        # Normalize data to create a quantum state
        norm_data = np.array(data) / np.linalg.norm(data)
        circuit = QuantumCircuit(len(norm_data))

        # Prepare the quantum state
        for i in range(len(norm_data)):
            if norm_data[i] > 0:
                circuit.ry(2 * np.arccos(norm_data[i]), i)  # Rotate around Y-axis
                if i > 0:
                    circuit.cx(i - 1, i)  # Create entanglement

        return circuit

    def visualize_state(self, circuit):
        """Visualize the quantum state using Bloch sphere."""
        # Execute the circuit to get the state vector
        statevector = execute(circuit, self.backend).result().get_statevector()
        logging.info(f"Quantum state vector: {statevector}")

        # Plot Bloch sphere
        plot_bloch_multivector(statevector)
        plt.title("Quantum State Visualization")
        plt.show()

    def measure_and_visualize(self, circuit):
        """Measure the quantum state and visualize the results."""
        circuit.measure_all()  # Measure all qubits

        # Execute the circuit
        result = execute(circuit, self.backend).result()
        counts = result.get_counts()

        # Plot measurement results
        plot_histogram(counts)
        plt.title("Measurement Results")
        plt.show()

if __name__ == "__main__":
    # Example usage
    visualizer = QuantumDataVisualization()

    # Example input data (can be any normalized vector)
    input_data = [0.6, 0.8]  # Example data for a 2-qubit state

    # Prepare quantum state
    circuit = visualizer.prepare_quantum_state(input_data)

    # Visualize the quantum state
    visualizer.visualize_state(circuit)

    # Measure and visualize the results
    visualizer.measure_and_visualize(circuit)
