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

import numpy as np
import pytest
from braket.circuits import Circuit
from braket.devices import LocalSimulator

from braket.experimental.algorithms.deutsch_jozsa import (
    balanced_oracle,
    constant_oracle,
    deutsch_jozsa_circuit,
    get_deutsch_jozsa_results,
)


def test_constant_oracle_circuit():
    circ = constant_oracle(3)
    assert circ.qubit_count == 4


@pytest.xfail(raises=ValueError)
def test_fail_constant_oracle_circuit():
    constant_oracle(0)


def test_balanced_oracle_circuit():
    circ = balanced_oracle(3)
    assert circ.qubit_count == 4


@pytest.xfail(raises=ValueError)
def test_fail_balanced_oracle_circuit():
    balanced_oracle(0)


def test_dj_circuit():
    dj = deutsch_jozsa_circuit(Circuit(), 0)
    expected = Circuit().x(0).h(0).probability()
    assert dj == expected


def test_get_deutsch_jozsa_results_constant():
    device = LocalSimulator()
    const_oracle = constant_oracle(3)
    dj_circuit = deutsch_jozsa_circuit(const_oracle, 3)
    task = device.run(dj_circuit, shots=0)
    dj_probabilities = get_deutsch_jozsa_results(task)
    assert np.isclose(dj_probabilities["000"], 1.0)


def test_get_deutsch_jozsa_results_balanced():
    device = LocalSimulator()
    bal_oracle = balanced_oracle()(3)
    dj_circuit = deutsch_jozsa_circuit(bal_oracle, 3)
    task = device.run(dj_circuit, shots=0)
    dj_probabilities = get_deutsch_jozsa_results(task)
    assert np.isclose(dj_probabilities["111"], 1.0)
