import os

from devices import *

voltage = [1.62, 1.8, 1.98]
# voltage = [1.62, 1.70, 1.75, 1.80, 1.85, 1.90, 1.98]

TestDict = [
    {
        "test_name": "gpio_mgmt_tests",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": True,
        "io": False,
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
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/uart_tests/uart_tests.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to UART
    },
    {
        "test_name": "mem_tests_dff",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_tests_dff/mem_tests_dff.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_tests_dff2",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_tests_dff2/mem_tests_dff2.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "soc_tests",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/soc_tests/soc_tests.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "gpio_tests",
        "uart": False,  # NOT Testing UART
        "mgmt_gpio": False,
        "io": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_tests/gpio_tests.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    # {
    #     "test_name": "cpu_stress",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/cpu_stress/cpu_stress.hex",
    #     "passing_criteria": [
    #         1,
    #         2,
    #         3,
    #         4,
    #         5,
    #         1,
    #         1,
    #         1,
    #     ],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "timer0_oneshot",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/timer0_oneshot/timer0_oneshot.hex",
    #     "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "timer0_periodic",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/timer0_periodic/timer0_periodic.hex",
    #     "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # # {
    # #     "test_name": "spi_master",
    # #     "uart": False,  # NOT Testing UART
    # #     "mem": False,  # NOT Testing mem
    # #     "io": False,
    # #     "spi": True,
    # #     "external": False,
    #     # "clock": False,
    # #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/spi_master/spi_master.hex",
    # #     "passing_criteria": [
    # #         1,
    # #         2,
    # #         3,
    # #         4,
    # #         5,
    # #         1,
    # #         1,
    # #         1,
    # #     ],  # Passing criteria to be sent to mgmt_gpio
    # # },
    # {
    #     "test_name": "hk_regs_wr_wb_cpu",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/hk_regs_wr_wb_cpu/hk_regs_wr_wb_cpu.hex",
    #     "passing_criteria": [2, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "IRQ_external",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": True,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_external/IRQ_external.hex",
    #     "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "IRQ_external2",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": True,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_external2/IRQ_external2.hex",
    #     "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "IRQ_timer",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_timer/IRQ_timer.hex",
    #     "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "IRQ_spi",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_spi/IRQ_spi.hex",
    #     "passing_criteria": [2, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "IRQ_uart",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_uart/IRQ_uart.hex",
    #     "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "IRQ_uart_rx",
    #     "uart": True,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_uart_rx/IRQ_uart_rx.hex",
    #     "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    # },
    # {
    #     "test_name": "gpio_o_l",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": "low",
    #     "mode": "output",
    #     "spi": False,
    #     "external": False,
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_o_l/gpio_o_l.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_o_h/gpio_o_h.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_i_l/gpio_i_l.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_i_h/gpio_i_h.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/bitbang_o_l/bitbang_o_l.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/bitbang_o_h/bitbang_o_h.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/bitbang_i_l/bitbang_i_l.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/bitbang_i_h/bitbang_i_h.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lpu_ho/gpio_lpu_ho.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lpd_ho/gpio_lpd_ho.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lo_hpu/gpio_lo_hpu.hex",
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
    #     "clock": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_lo_hpd/gpio_lo_hpd.hex",
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
