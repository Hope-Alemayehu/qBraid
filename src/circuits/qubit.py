from typing import Any, Sequence, Dict, Iterable, Union

from braket.circuits.qubit import Qubit as BraketQubit
from qiskit.circuit.quantumregister import Qubit as QiskitQubit
from cirq.ops.named_qubit import NamedQubit as CirqNamedQubit
from cirq.devices.line_qubit import LineQubit as CirqLineQubit

from qiskit.circuit.quantumregister import QuantumRegister as QiskitQuantumRegister

QubitInput = Union["BraketQubit", "CirqNamedQubit","QiskitQubit", int, str] 

class Qubit():
    
    """
    Qubit Class: hold qubit objects
    
    Args:
        qubit: input object, acceptable objects include:
            Braket, qiskit, cirq
    """
    
    def __init__(self, 
                 qubit: QubitInput = None, 
                 identifier: Union[int,str] = None):
        
        self.qubit = qubit
        self.id = identifier
        
        if isinstance(qubit,QiskitQubit):
            self.index = qubit.index
        elif isinstance(qubit,CirqLineQubit):
            self.index = qubit.x
        elif isinstance(qubit,CirqNamedQubit):
            self.name = qubit.name
        
        self.outputs = {}
        
    def _create_cirq_object(self):
        
        if isinstance(self.qubit,QiskitQubit):
            self.outputs['cirq'] = CirqLineQubit(self.index)
        
    def _create_qiskit_object(self,register: QiskitQuantumRegister, index: int):
        
        self.outputs['qiskit'] = QiskitQubit(register, index)
        
    def to_cirq(self):
        
        if 'cirq' not in self.outputs.keys() or not self.outputs['cirq']:
            self._create_cirq_object()
        
        return self.outputs['cirq']
        
    def to_qiskit(self):
        
        try:
            return self.outputs['qiskit']
        except:
            print("qiskit output not initialized in qubit {}".format(self.id))
            
            
        
        
        