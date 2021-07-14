from cirq import Gate
from cirq.ops.measurement_gate import MeasurementGate
from sympy import Symbol as CirqParameter
from typing import Union

from qbraid.transpiler.gate import GateWrapper
from .utils import get_cirq_gate_data

CirqGate = Union[Gate, MeasurementGate]


class CirqGateWrapper(GateWrapper):
    def __init__(self, gate: CirqGate):

        super().__init__()

        self.gate = gate
        self.name = None

        data = get_cirq_gate_data(gate)

        self.matrix = data["matrix"]
        self.params = data["params"]
        self.num_controls = data["num_controls"]

        self._gate_type = data["type"]
        self._outputs["cirq"] = gate
        self._package = "cirq"

    def get_abstract_params(self):
        if not (self.params is None):
            return [p for p in self.params if isinstance(p, CirqParameter)]
        else:
            return []

    def parse_params(self, input_param_mapping):
        self.params = [
            input_param_mapping[p] if isinstance(p, CirqParameter) else p for p in self.params
        ]