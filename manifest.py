import os

from devices import *

gf180mcu = True

if gf180mcu:
    voltage = [5.0]
else:
    voltage = [1.62, 1.8, 1.98]
# voltage = [1.62, 1.70, 1.75, 1.80, 1.85, 1.90, 1.98]

TestDict = [
    {
        "test_name": "mgmt_gpio_tests",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mgmt_gpio_tests/mgmt_gpio_tests.hex",
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
    {
        "test_name": "uart_tests",
        "uart": True,  # Testing UART
        "mgmt_gpio": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/uart_tests/uart_tests.hex",
        "passing_criteria": [
            "Monitor: Test UART passed"
        ],  # Passing criteria to be sent to UART
    },
    {
        "test_name": "mem_tests_lower",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_tests_lower/mem_tests_lower.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_tests_upper",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_tests_upper/mem_tests_upper.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "soc_tests",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/soc_tests/soc_tests.hex",
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
    #     "test_name": "gpio_o_l",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "low",
    #     "mode": "output",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_o_l/gpio_o_l.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_o_h",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "high",
    #     "mode": "output",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_o_h/gpio_o_h.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_i_l",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "low",
    #     "mode": "input",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_i_l/gpio_i_l.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_i_h",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "high",
    #     "mode": "input",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_i_h/gpio_i_h.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "bitbang_o_l",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "low",
    #     "mode": "output",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/bitbang_o_l/bitbang_o_l.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "bitbang_o_h",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "high",
    #     "mode": "output",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/bitbang_o_h/bitbang_o_h.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "bitbang_i_l",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "low",
    #     "mode": "input",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/bitbang_i_l/bitbang_i_l.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "bitbang_i_h",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "high",
    #     "mode": "input",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/bitbang_i_h/bitbang_i_h.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_lpu_ho",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": True,
    #     "mode": "plud",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lpu_ho/gpio_lpu_ho.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_lpd_ho",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": True,
    #     "mode": "plud",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lpd_ho/gpio_lpd_ho.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_lo_hpu",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": True,
    #     "mode": "plud",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lo_hpu/gpio_lo_hpu.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_lo_hpd",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": True,
    #     "mode": "plud",
    #     "spi": False,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lo_hpd/gpio_lo_hpd.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         6,
    #         7,
    #         8,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
]
