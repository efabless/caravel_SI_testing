import os

from devices import *

l_voltage = [1.62, 1.8, 1.98]
h_voltage = [3.0, 3.3, 3.6]
# voltage = [1.62, 1.70, 1.75, 1.80, 1.85, 1.90, 1.98]

TestDict = [
    {
        "test_name": "gpio_mgmt_tests",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": True,
        "io": False,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_mgmt_tests/gpio_mgmt_tests.hex",
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
        "io": False,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/uart_tests/uart_tests.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to UART
    },
    {
        "test_name": "mem_tests_dff",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_tests_dff/mem_tests_dff.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_tests_dff2",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_tests_dff2/mem_tests_dff2.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "soc_tests",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/soc_tests/soc_tests.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "gpio_o",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": True,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_o/gpio_o.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "gpio_i",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": True,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_i/gpio_i.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "bitbang_o",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": True,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/bitbang_o/bitbang_o.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "bitbang_i",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": True,
        "plud": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/bitbang_i/bitbang_i.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "gpio_lpu_ho",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lpu_ho/gpio_lpu_ho.hex",
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
        "test_name": "gpio_lpd_ho",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lpd_ho/gpio_lpd_ho.hex",
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
        "test_name": "gpio_lo_hpu",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lo_hpu/gpio_lo_hpu.hex",
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
        "test_name": "gpio_lo_hpd",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lo_hpd/gpio_lo_hpd.hex",
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
    #     "test_name": "clock_redirect",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": True,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/clock_redirect/clock_redirect.hex",
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
