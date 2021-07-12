# Copyright 2019-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or at https://github.com/aws/amazon-braket-sdk-python/blob/main/LICENSE.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# NOTICE: This file has been modified from the original:
# https://github.com/aws/amazon-braket-sdk-python/blob/6926c1676dd5b465ef404614a44538c42ee2727d
# /src/braket/tasks/annealing_quantum_task_result.py

from ..result import ResultWrapper
from braket.tasks.gate_model_quantum_task_result import GateModelQuantumTaskResult
import numpy as np


class BraketGateModelResultWrapper(ResultWrapper):
    def __init__(self, gate_model_result: GateModelQuantumTaskResult):
        """Braket ``GateModelQuantumTaskResult`` wrapper class.
        Args:
            gate_model_result (GateModelQuantumTaskResult): a Braket ``Result`` object
        """
        super().__init__(gate_model_result)

    @property
    def measurements(self) -> np.ndarray:
        """2d array - row is shot and column is qubit. Default is None. Only available when
        shots > 0. The qubits in `measurements` are the ones in
        `GateModelQuantumTaskResult.measured_qubits`.
        """
        return self.vendor_rlo.measurements

    def data(self):
        return self.measurements