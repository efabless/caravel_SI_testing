import os

device1_sn = "7DA"  # last 3 digits of your first Analog Discovery Kit, connected to 1v8

device2_sn = (
    "AA0"  # last 3 digits of your second Analog Discovery Kit, connected to 3v3
)

TestDict = [
    {
        "test_name": "uart",
        "uart": True,
        "mem": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/uart/uart.hex",
        "passing_criteria": [
            "Monitor: Test UART passed"
        ],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "send_packet",
        "uart": False,
        "mem": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/send_packet/send_packet.hex",
        "passing_criteria": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
        ],  # Passing criteria to be sent to mgmt_gpio
    },
    # {
    #     "test_name": "mem_sram_W",
    #     "uart": False,
    #     "mem": True,
    #     "voltage": [1.6],
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_sram_W/mem_sram_W.hex",
    #     "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "mem_sram_test",
    #     "uart": False,
    #     "mem": True,
    #     "voltage": [1.6],
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_sram_test/mem_sram_test.hex",
    #     "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "mem_sram_halfW",
    #     "uart": False,
    #     "mem": True,
    #     "voltage": [1.6],
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_sram_halfW/mem_sram_halfW.hex",
    #     "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "mem_dff_W",
    #     "uart": False,
    #     "mem": True,
    #     "voltage": [1.6],
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff_W/mem_dff_W.hex",
    #     "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "mem_dff_test",
    #     "uart": False,
    #     "mem": True,
    #     "voltage": [1.6],
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff_test/mem_dff_test.hex",
    #     "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "mem_dff_halfW",
    #     "uart": False,
    #     "mem": True,
    #     "voltage": [1.6],
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff_halfW/mem_dff_halfW.hex",
    #     "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    {
        "test_name": "cpu_stress",
        "uart": False,
        "mem": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/cpu_stress/cpu_stress.hex",
        "passing_criteria": [
            1,
            2,
            3,
            4,
            5,
            1,
            1,
            1,
        ],  # Passing criteria to be sent to mgmt_gpio
    },
]
