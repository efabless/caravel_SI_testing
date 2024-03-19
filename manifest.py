import os

from devices import *

l_voltage = [1.62, 1.8, 1.98]
h_voltage = [3.0, 3.3, 3.6]
# voltage = [1.62, 1.70, 1.75, 1.80, 1.85, 1.90, 1.98]

TestDict = [
    {
        "test_name": "gpio_mgmt_tests",
        "mgmt_gpio": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/gpio_mgmt_tests/gpio_mgmt_tests.hex",
    },
    {
        "test_name": "uart_tests",
        "uart": True,  # Testing UART
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/uart_tests/uart_tests.hex",
    },
    {
        "test_name": "mem_tests_dff",
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/mem_tests_dff/mem_tests_dff.hex",
    },
    {
        "test_name": "mem_tests_dff2",
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/mem_tests_dff2/mem_tests_dff2.hex",
    },
    {
        "test_name": "soc_tests",
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/soc_tests/soc_tests.hex",
    },
    {
        "test_name": "gpio_o",
        "io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/gpio_o/gpio_o.hex",
    },
    {
        "test_name": "gpio_i",
        "io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/gpio_i/gpio_i.hex",
    },
    {
        "test_name": "bitbang_o",
        "io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/bitbang_o/bitbang_o.hex",
    },
    {
        "test_name": "bitbang_i",
        "io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/bitbang_i/bitbang_i.hex",
    },
    {
        "test_name": "gpio_lpu_ho",
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/gpio_lpu_ho/gpio_lpu_ho.hex",
    },
    {
        "test_name": "gpio_lpd_ho",
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/gpio_lpd_ho/gpio_lpd_ho.hex",
    },
    {
        "test_name": "gpio_lo_hpu",
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/gpio_lo_hpu/gpio_lo_hpu.hex",
    },
    {
        "test_name": "gpio_lo_hpd",
        "plud": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/caravel/gpio_lo_hpd/gpio_lo_hpd.hex",
    },
]
