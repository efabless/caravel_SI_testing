import os
from manifest import (
    TestDict,
    device1_sn,
    device2_sn,
    device3_sn,
    l_voltage,
    h_voltage,
    analog,
)

clear_test_dict = [
    {
        "test_name": "chain_check",
        "chain": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/chain_check/chain_check.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "and_gate",
        "and_flag": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/and_gate/and_gate.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "inv_1",
        "fpga_io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/inv_1/inv_1.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "inv_2",
        "fpga_io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/inv_2/inv_2.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "ALU_4bits",
        "alu": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/ALU_4bits/ALU_4bits.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "seconds_decoder",
        "sec_count": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/seconds_decoder/seconds_decoder.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "fpga_ram8x20",
        "fpga_ram": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/fpga_ram8x20/fpga_ram8x20.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
]

for test in clear_test_dict:
    TestDict.append(test)