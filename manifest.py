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
        "test_name": "send_packet",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/send_packet/send_packet.hex",
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
        "test_name": "receive_packet",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/receive_packet/receive_packet.hex",
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
        "test_name": "uart",
        "uart": True,  # Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/uart/uart.hex",
        "passing_criteria": [
            "Monitor: Test UART passed"
        ],  # Passing criteria to be sent to UART
    },
    {
        "test_name": "uart_reception",
        "uart": True,  # Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/uart_reception/uart_reception.hex",
        "passing_criteria": ["M", "B", "A"],  # Passing criteria to be sent to UART
    },
    {
        "test_name": "uart_loopback",
        "uart": True,  # Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/uart_loopback/uart_loopback.hex",
        "passing_criteria": [
            "M",
            "B",
            "A",
            "5",
            "o",
        ],  # Passing criteria to be sent to UART
    },
    {
        "test_name": "mem_sram_W_lower",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_sram_W_lower/mem_sram_W_lower.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_sram_test_lower",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_sram_test_lower/mem_sram_test_lower.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_sram_halfW_lower",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_sram_halfW_lower/mem_sram_halfW_lower.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_sram_W_upper",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_sram_W_upper/mem_sram_W_upper.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_sram_test_upper",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_sram_test_upper/mem_sram_test_upper.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_sram_halfW_upper",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/mem_sram_halfW_upper/mem_sram_halfW_upper.hex",
        "passing_criteria": [1, 3, 4, 5],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "cpu_stress",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/cpu_stress/cpu_stress.hex",
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
    {
        "test_name": "timer0_oneshot",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/timer0_oneshot/timer0_oneshot.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "timer0_periodic",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/timer0_periodic/timer0_periodic.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    # {
    #     "test_name": "spi_master",
    #     "uart": False,  # NOT Testing UART
    #     "mem": False,  # NOT Testing mem
    #     "io": False,
    #     "spi": True,
    #     "external": False,
    #     "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/spi_master/spi_master.hex",
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
    {
        "test_name": "IRQ_external",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/IRQ_external/IRQ_external.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "IRQ_external2",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": True,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/IRQ_external2/IRQ_external2.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "IRQ_timer",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/IRQ_timer/IRQ_timer.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "IRQ_spi",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/IRQ_spi/IRQ_spi.hex",
        "passing_criteria": [2, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "IRQ_uart",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/IRQ_uart/IRQ_uart.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "IRQ_uart_rx",
        "uart": True,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/IRQ_uart_rx/IRQ_uart_rx.hex",
        "passing_criteria": [None],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "gpio_o_l",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": "low",
        "mode": "output",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_o_l/gpio_o_l.hex",
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
        "test_name": "gpio_o_h",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": "high",
        "mode": "output",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_o_h/gpio_o_h.hex",
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
        "test_name": "gpio_i_l",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": "low",
        "mode": "input",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_i_l/gpio_i_l.hex",
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
        "test_name": "gpio_i_h",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": "high",
        "mode": "input",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_i_h/gpio_i_h.hex",
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
        "test_name": "gpio_lpu_ho",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": True,
        "mode": "plud",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lpu_ho/gpio_lpu_ho.hex",
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
        "mem": False,  # NOT Testing mem
        "io": True,
        "mode": "plud",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lpd_ho/gpio_lpd_ho.hex",
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
        "mem": False,  # NOT Testing mem
        "io": True,
        "mode": "plud",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lo_hpu/gpio_lo_hpu.hex",
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
        "mem": False,  # NOT Testing mem
        "io": True,
        "mode": "plud",
        "spi": False,
        "external": False,
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/gf180mcu/gpio_lo_hpd/gpio_lo_hpd.hex",
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
]
