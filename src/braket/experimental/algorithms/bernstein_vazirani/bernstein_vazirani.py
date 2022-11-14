# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from braket.circuits import Circuit
from braket.tasks import QuantumTask


def bernstein_vazirani_circuit(hidden_string: str = "011") -> Circuit:
    """Bernstein–Vazirani circuit on a hidden string.

    Args:
        hidden_string (str): Hidden bitstring. Defaults to "011".

    Returns:
        Circuit: Bernstein–Vazirani circuit
    """
    num_qubits = len(hidden_string)

    bv_circuit = Circuit()
    bv_circuit.h(num_qubits)
    bv_circuit.z(num_qubits)
    bv_circuit.h(range(num_qubits))

    for q in range(num_qubits):
        if hidden_string[q] == "0":
            bv_circuit.i(q)
        else:
            bv_circuit.cnot(q, num_qubits)

    bv_circuit.h(range(num_qubits))

    bv_circuit.probability(range(num_qubits))
    return bv_circuit


def get_bernstein_vazirani_results(task: QuantumTask) -> Dict[str, float]:
    """Return the probabilities and corresponding bitstrings.

    Args:
        task (QuantumTask): Quantum task to process.

    Returns:
        Dict[str, float]: Results as a dictionary of bitstrings
    """

    probabilities = task.result().result_types[-1].value
    probabilities = np.round(probabilities, 10)  # round off floating-point errors
    num_qubits = int(np.log2(len(probabilities)))
    binary_strings = [format(i, "b").zfill(num_qubits) for i in range(2**num_qubits)]
    return dict(zip(binary_strings, probabilities))


def plot_bitstrings(probabilities: Dict[str, float], title: str = None) -> None:
    """Plot the measure results

    Args:
        probabilities (Dict[str, float]): Measurement probabilities.
        title (str): Title for the plot.
    """
    plt.bar(probabilities.keys(), probabilities.values())
    plt.xlabel("bitstrings")
    plt.ylabel("probabilities")
    plt.title(title)
    plt.xticks(rotation=90)
