from ...gate import Gate

class U2(Gate):

    def __init__(self, phi, lam):
        super().__init__("R", 1, [phi, lam], 0.0, 1.0)

    @property
    def name(self):
        return self._name

    @property
    def num_qubits(self):
        return self._num_qubits

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, phi, lam):
        self._params=[phi, lam]

    @property
    def global_phase(self):
        return self._global_phase

    @property
    def exponent(self):
        return self._exponent