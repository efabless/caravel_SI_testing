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

blizzard_test_dict = [
    {
        "test_name": "chain_check",
        "chain": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/chain_check/chain_check.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "and_gate",
        "and_flag": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/and_gate/and_gate.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "inv_1",
        "fpga_io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/inv_1/inv_1.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "inv_2",
        "fpga_io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/inv_2/inv_2.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "ALU_4bits",
        "alu": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/ALU_4bits/ALU_4bits.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "seconds_decoder",
        "sec_count": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/seconds_decoder/seconds_decoder.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "fpga_ram8x20",
        "fpga_ram": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/fpga_ram8x20/fpga_ram8x20.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "adc_test",
        "ana": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/blizzard/adc_test/adc_test.hex",
        "chip_name": "Blizzard",
    },
    {
        "test_name": "dac_test",
        "ana": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/blizzard/dac_test/dac_test.hex",
        "chip_name": "Blizzard",
    },
]

for test in blizzard_test_dict:
    TestDict.append(test)
