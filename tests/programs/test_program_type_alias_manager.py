# Copyright (C) 2024 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

"""
Unit tests for managing quantum program type aliases.

"""
from unittest.mock import Mock

import pytest

from qbraid.programs.alias_manager import get_program_type_alias, parse_qasm_type_alias
from qbraid.programs.exceptions import ProgramTypeError, QasmError
from qbraid.programs.registry import derive_program_type_alias

from ..fixtures import packages_bell

QASM_BELL_DATA = [
    (
        """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];
        """,
        "qasm2",
    ),
    (
        """
OPENQASM 3;
include "stdgates.inc";
qubit[2] q;
h q[0];
cx q[0], q[1];
        """,
        "qasm3",
    ),
    (
        """
OPENQASM 3.0;
bit[2] __bits__;
qubit[2] __qubits__;
h __qubits__[0];
cnot __qubits__[0], __qubits__[1];
__bits__[0] = measure __qubits__[0];
__bits__[1] = measure __qubits__[1];
        """,
        "qasm3",
    ),
]

QASM_ERROR_DATA = [
    """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0;
cx q[0], q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];

        """,
    """
OPENQASM 3.0;
include "stdgates.inc";
bit c[2];
qubit q[2];
h q[0]
cx q[0], q[1];
measure q -> c;
        """,
]


@pytest.mark.parametrize("qasm_str, expected_version", QASM_BELL_DATA)
def test_parse_qasm_type_alias(qasm_str, expected_version):
    """Test getting QASM version"""
    assert parse_qasm_type_alias(qasm_str) == expected_version


@pytest.mark.parametrize("qasm_str", QASM_ERROR_DATA)
def test_parse_qasm_type_alias_error(qasm_str):
    """Test getting QASM version"""
    with pytest.raises(QasmError):
        parse_qasm_type_alias(qasm_str)


@pytest.mark.parametrize("bell_circuit", packages_bell, indirect=True)
def test_get_program_type_alias(bell_circuit):
    """Test that the correct package is returned for a given program."""
    circuit, expected_package = bell_circuit
    package_name = get_program_type_alias(circuit)
    assert package_name == expected_package


@pytest.mark.parametrize("program,expected_package", [(Mock(), "unittest")])
def test_get_program_type_alias_required_supported_false(program, expected_package):
    """Test that None or module name is returned for unsupported package when
    require supported is given as False."""
    package = derive_program_type_alias(program)
    assert package == expected_package


def test_raise_error_unuspported_source_program():
    """Test that an error is raised if source program is not supported."""
    with pytest.raises(ProgramTypeError):
        get_program_type_alias(Mock())


@pytest.mark.parametrize(
    "item",
    ["OPENQASM 2.0; bad operation", "OPENQASM 3.0; bad operation", "DECLARE ro BIT[1]", "circuit"],
)
def test_bad_source_openqasm_program(item):
    """Test raising ProgramTypeError converting invalid OpenQASM program string"""
    with pytest.raises(ProgramTypeError):
        get_program_type_alias(item)


@pytest.mark.parametrize("item", [1, None])
def test_bad_source_program_type(item):
    """Test raising ProgramTypeError converting circuit of non-supported type"""
    with pytest.raises(ProgramTypeError):
        get_program_type_alias(item)
