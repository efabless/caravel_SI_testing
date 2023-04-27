import os

device1_sn = "###"  # last 3 digits of your first Analog Discovery Kit, connected to 1v8

device2_sn = "###"  # last 3 digits of your second Analog Discovery Kit,connected to 3v3

device3_sn = "###"  # last 3 digits of your third Analog Discovery Kit

TestDict = [
    {
        "test_name": "uart",
        "uart": True,  # Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/uart/uart.hex",
        "passing_criteria": [
            "Monitor: Test UART passed"
        ],  # Passing criteria to be sent to UART
    },
    {
        "test_name": "send_packet",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
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
    {
        "test_name": "gpio_o_l",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": "low",
        "mode": "out",
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_o_l/gpio_o_l.hex",
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
        "mode": "out",
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_o_h/gpio_o_h.hex",
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
        "mode": "in",
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_i_l/gpio_i_l.hex",
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
        "mode": "in",
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/gpio_i_h/gpio_i_h.hex",
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
        "test_name": "mem_dff2_W",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff2_W/mem_dff2_W.hex",
        "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_dff2_test",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff2_test/mem_dff2_test.hex",
        "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_dff2_halfW",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff2_halfW/mem_dff2_halfW.hex",
        "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_dff_W",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff_W/mem_dff_W.hex",
        "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_dff_test",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff_test/mem_dff_test.hex",
        "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "mem_dff_halfW",
        "uart": False,  # NOT Testing UART
        "mem": False,  # Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/mem_dff_halfW/mem_dff_halfW.hex",
        "passing_criteria": [1, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "cpu_stress",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
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
    {
        "test_name": "IRQ_external",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_external/IRQ_external.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "IRQ_timer",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_timer/IRQ_timer.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "IRQ_uart",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/IRQ_uart/IRQ_uart.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "timer0_oneshot",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/timer0_oneshot/timer0_oneshot.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
    {
        "test_name": "timer0_periodic",
        "uart": False,  # NOT Testing UART
        "mem": False,  # NOT Testing mem
        "io": False,
        "voltage": [1.6],
        "hex_file_path": f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/timer0_periodic/timer0_periodic.hex",
        "passing_criteria": [1, 5, 3, 3, 3],  # Passing criteria to be sent to mgmt_gpio
    },
]
