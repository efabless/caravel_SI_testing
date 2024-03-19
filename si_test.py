import argparse
import importlib
import json
from caravel import Dio, Test
from io_config import Device, device, connect_devices, UART, SPI
import os
import csv
import time
import datetime
import subprocess
import signal
import sys
from rich.table import Table
from WF_SDK import logic, wavegen, static, scope
import matplotlib.pyplot as plt
import numpy as np


def init_ad_ios(device1_data, device2_data, device3_data):
    """
    Initialize the DIO maps for three devices and return them as a tuple.

    Args:
        device1_data: Data for device 1
        device2_data: Data for device 2
        device3_data: Data for device 3

    Returns:
        Tuple: Three DIO maps for device 1, device 2, and device 3
    """
    device1_dio_map = {
        # "rstb": Dio(0, device1_data, True),
        "rstb": Dio(0, device1_data),
        "gpio_mgmt": Dio(1, device1_data),
        0: Dio(2, device1_data),
        1: Dio(3, device1_data),
        2: Dio(4, device1_data),
        3: Dio(5, device1_data),
        4: Dio(6, device1_data),
        5: Dio(7, device1_data),
        6: Dio(8, device1_data),
        7: Dio(9, device1_data),
        8: Dio(10, device1_data),
        9: Dio(11, device1_data),
        10: Dio(12, device1_data),
        11: Dio(13, device1_data),
        12: Dio(14, device1_data),
        13: Dio(15, device1_data),
    }

    device2_dio_map = {
        22: Dio(0, device2_data),
        23: Dio(1, device2_data),
        24: Dio(2, device2_data),
        25: Dio(3, device2_data),
        26: Dio(4, device2_data),
        27: Dio(5, device2_data),
        28: Dio(6, device2_data),
        29: Dio(7, device2_data),
        30: Dio(8, device2_data),
        31: Dio(9, device2_data),
        32: Dio(10, device2_data),
        33: Dio(11, device2_data),
        34: Dio(12, device2_data),
        35: Dio(13, device2_data),
        36: Dio(14, device2_data),
        37: Dio(15, device2_data),
    }

    device3_dio_map = {
        14: Dio(2, device3_data),
        15: Dio(3, device3_data),
        16: Dio(4, device3_data),
        17: Dio(5, device3_data),
        18: Dio(6, device3_data),
        19: Dio(7, device3_data),
        20: Dio(8, device3_data),
        21: Dio(9, device3_data),
    }

    return device1_dio_map, device2_dio_map, device3_dio_map


def process_mgmt_gpio(test, verbose):
    """
    Process the management of GPIO, running various tests and returning the status of each test.
    Args:
        test: The test object used to run the tests.
        verbose: A boolean indicating whether to print detailed logs.
    Returns:
        A list of tuples containing the test name and a boolean indicating the test status.
    """
    test_names = ["send_packet", "receive_packet", "uart_io"]
    status = []
    counter = 0
    for name in test_names:
        test.test_name = name
        if test.test_name == "receive_packet":
            io = test.device1v8.dio_map[0]
            pulse_count = test.receive_packet(25)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
            for i in range(5, 8):
                while not io.get_value():
                    pass
                test.send_packet(i, 1)
                while io.get_value():
                    pass
                pulse_count = test.receive_packet(25)
                if pulse_count == i:
                    counter += 1
                else:
                    test.print_and_log("[red]failed")
                    status.append((test.test_name, False))
            if counter == 3:
                test.print_and_log("[green]passed")
                status.append((test.test_name, True))
            else:
                test.print_and_log("[red]failed")
                status.append((test.test_name, False))

        elif name == "uart_io":
            pulse_count = test.receive_packet(25)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
                received = test.io_receive(4, 6)
                if not received:
                    test.print_and_log("[red]failed")
                    status.append((test.test_name, False))
                else:
                    if verbose:
                        test.print_and_log("IO[6] Passed")
                    pulse_count = test.receive_packet(25)
                    if pulse_count == 3:
                        if verbose:
                            test.print_and_log("Send 4 packets to IO[5]")
                        time.sleep(5)
                        test.send_pulse(4, 5, 5)
                        ack_pulse = test.receive_packet(25)
                        if ack_pulse == 9:
                            test.print_and_log("[red]failed")
                            status.append((test.test_name, False))
                        elif ack_pulse == 4:
                            test.print_and_log("[green]passed")
                            status.append((test.test_name, True))

        else:
            phase = 0
            test.print_and_log(f"Running test {test.test_name}...")
            for passing in [8]:
                pulse_count = test.receive_packet(25)
                if pulse_count == passing:
                    if verbose:
                        test.print_and_log(f"pass phase {phase}")
                    phase = phase + 1

                if pulse_count == 9:
                    test.print_and_log("[red]failed")
                    status.append((test.test_name, False))

            if len([8]) == phase:
                test.print_and_log("[green]passed")
                status.append((test.test_name, True))
    return status


def process_uart(test, uart, verbose):
    """Function to test all UART functionality
    First test: IO[5] as input to caravel and IO[6] as output from caravel
    Second test: UART as output from caravel
    Third test: UART as input to caravel
    Fourth test: UART loopback (tests both input and output)
    """

    test_names = ["uart", "uart_reception", "uart_loopback", "IRQ_uart_rx"]
    status = []
    for name in test_names:
        test.test_name = name
        pulse_count = test.receive_packet(25)
        if pulse_count == 1:
            if verbose:
                test.print_and_log(f"Start Test: {name}")

        if test.test_name == "uart":
            pulse_count = test.receive_packet(25)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
            uart_data = uart.read_data(test)
            uart_data = uart_data.decode("utf-8", "ignore")
            if "UART Timeout!" in uart_data:
                test.print_and_log("[red]UART Timeout!")
                status.append((test.test_name, False))
            if "Monitor: Test UART passed" in uart_data:
                test.print_and_log("[green]passed")
                status.append((test.test_name, True))
            else:
                test.print_and_log("[red]failed")
                status.append((test.test_name, False))
            pulse_count = test.receive_packet(25)
            if pulse_count == 5:
                if verbose:
                    test.print_and_log("end UART transmission")

        elif test.test_name == "uart_reception":
            passed = True
            pulse_count = test.receive_packet(25)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
            uart.open()
            timeout = time.time() + 50
            for i in ["M", "B", "A"]:
                pulse_count = test.receive_packet(25)
                if pulse_count == 4:
                    uart.write(i)
                pulse_count = test.receive_packet(25)
                if pulse_count == 6:
                    passed = True
                    if verbose:
                        test.print_and_log(f"Received {i} successfully")
                if pulse_count == 9:
                    test.print_and_log("[red]failed")
                    uart.close()
                    passed = False
                    status.append((test.test_name, False))
                    break
                if time.time() > timeout:
                    test.print_and_log("[red]UART Timeout!")
                    uart.close()
                    passed = False
                    status.append((test.test_name, False))
                    break
            if passed:
                test.print_and_log("[green]passed")
                status.append((test.test_name, True))

        elif test.test_name == "uart_loopback":
            passed = True
            uart.open()
            timeout = time.time() + 50
            test.print_and_log(f"Running test {test.test_name}...")
            for i in range(0, 5):
                while time.time() < timeout:
                    uart_data, count = uart.read_uart()
                    if uart_data:
                        uart_data[count.value] = 0
                        dat = uart_data.value.decode("utf-8", "ignore")
                        uart.write(dat)
                        pulse_count = test.receive_packet(25)
                        if pulse_count == 6:
                            passed = True
                            if verbose:
                                test.print_and_log(f"sent {dat} successfully")
                            break
                        if pulse_count == 9:
                            test.print_and_log("[red]failed")
                            uart.close()
                            status.append((test.test_name, False))
                            break
            if passed:
                test.print_and_log("[green]passed")
                status.append((test.test_name, True))

        elif test.test_name == "IRQ_uart_rx":
            pulse_count = test.receive_packet(25)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
            uart.open()
            uart.write("I")
            pulse_count = test.receive_packet(25)
            if pulse_count == 5:
                test.print_and_log("[green]passed")
                status.append((test.test_name, True))
                break
            if pulse_count == 9:
                test.print_and_log("[red]failed")
                uart.close()
                status.append((test.test_name, False))

    return status


def process_soc(test, uart):
    """
    Process SOC function to control GPIO and UART, read UART data, and handle different test cases.
    This is the default test function.
    Parameters:
    - test: An object representing the test environment
    - uart: An object representing the UART communication
    Returns:
    - status: A list of tuples containing the test name and its corresponding status (True or False)
    """
    status = []
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    while True:
        uart_data = uart.read_data(test)
        uart_data = uart_data.decode("utf-8", "ignore")
        if "UART Timeout!" in uart_data:
            test.print_and_log("[red]UART Timeout!")
            status.append((test.test_name, False))
            break
        if "Start Test:" in uart_data:
            test.test_name = uart_data.strip().split(": ")[1]
            test.print_and_log(f"Running test {test.test_name}...")
        elif "End Test" in uart_data:
            test.print_and_log("End Test")
            break

        if test.test_name == "IRQ_external" or test.test_name == "IRQ_external2":
            if test.test_name == "IRQ_external":
                channel = 7
            else:
                channel = 12
            channel = test.device1v8.dio_map[channel]
            channel.set_state(True)
            channel.set_value(1)
        elif test.test_name == "IRQ_uart_rx":
            uart.open()
            uart.write("I")
        uart_data = uart.read_data(test)
        uart_data = uart_data.decode("utf-8", "ignore")
        if "UART Timeout!" in uart_data:
            test.print_and_log("[red]UART Timeout!")
            status.append((test.test_name, False))
            break
        if "passed" in uart_data:
            test.print_and_log("[green]passed")
            status.append((test.test_name, True))
        elif "failed" in uart_data:
            test.print_and_log("[red]failed")
            status.append((test.test_name, False))
    return status


def hk_stop(close):
    """
    A function stops the housekeeping from interrupting the test.
    """
    global pid
    if not close:
        # test.print_and_log("running caravel_hkstop.py...")
        p = subprocess.Popen(
            ["python3", "silicon_tests/util/caravel_hkstop.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        pid = p.pid
        # test.print_and_log("subprocess pid:", pid)
    elif pid:
        # test.print_and_log("stopping caravel_hkstop.py...")
        os.kill(pid, signal.SIGTERM)
        pid = None


def process_io(test, uart, verbose, analog):
    """
    Function that tests the GPIO Input and Output.

    Args:
        test: The test object for GPIO management.
        uart: The UART object for communication.
        verbose: A boolean indicating whether to print verbose output.

    Returns:
        A tuple containing a boolean indicating success or failure, and a list of failed channels if any.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    hk_stop(False)
    fail = []
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode("utf-8", "ignore")
    if "UART Timeout!" in uart_data:
        test.print_and_log("[red]UART Timeout!")
        return False, None
    if "Start Test:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.print_and_log(f"Running test {test.test_name}...")
    for i in range(38):
        if i == 5 or i == 6:
            pass
        else:
            io_pulse = 0
            uart.write("g: " + str(i) + "\n")
            channel = i
            if channel > 4:
                hk_stop(True)
            if test.test_name == "gpio_o" or test.test_name == "bitbang_o":
                if channel > 13 and channel < 22:
                    io = test.deviced.dio_map[channel]
                elif channel > 21:
                    io = test.device3v3.dio_map[channel]
                else:
                    io = test.device1v8.dio_map[channel]
                if analog and channel > 13 and channel < 25:
                    pass
                else:
                    if verbose:
                        test.print_and_log(f"IO[{channel}]")
                    timeout = time.time() + 5
                    state = "LOW"
                    while 1:
                        uart_data = uart.read_data(test, 5)
                        if b"UART Timeout!" in uart_data:
                            test.print_and_log(
                                f"[red]Timeout failure on IO[{channel}]!"
                            )
                            fail.append(channel)
                            break
                        # uart_data = uart_data.decode('utf-8', 'ignore')
                        if b"d" in uart_data and state == "HI":
                            if not io.get_value():
                                state = "LOW"
                                io_pulse += 1
                        if b"u" in uart_data and state == "LOW":
                            if io.get_value():
                                state = "HI"
                                io_pulse += 1
                        if io_pulse == 4:
                            io_pulse = 0
                            if verbose:
                                test.print_and_log(f"[green]IO[{channel}] Passed")
                            break
                        if time.time() > timeout:
                            test.print_and_log(
                                f"[red]Timeout failure on IO[{channel}]!"
                            )
                            fail.append(channel)
                            break
            elif test.test_name == "gpio_i" or test.test_name == "bitbang_i":
                if verbose:
                    test.print_and_log(f"IO[{channel}]")
                test.send_pulse(4, channel, 1)
                uart_data = uart.read_data(test, 5)
                if b"UART Timeout!" in uart_data:
                    test.print_and_log("[red]UART Timeout!")
                    fail.append(channel)
                if b"p" in uart_data:
                    if verbose:
                        test.print_and_log(f"[green]IO[{channel}] Passed")
                elif b"f" in uart_data:
                    test.print_and_log(f"[red]IO[{channel}] Failed")
                    fail.append(channel)
    hk_stop(True)
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(1)
    time.sleep(1)

    if len(fail) == 0:
        test.print_and_log("[green]passed")
        return True, None
    else:
        test.print_and_log("[red]failed")
        return False, fail


def process_io_plud(test, uart, analog):
    """
    Process IO polarity test function to handle IO operations and test results.

    Args:
        test: The test object containing GPIO management and test information.
        uart: The UART object for reading data.

    Returns:
        bool: True if the test passed, False if it failed.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    p1_rt = False
    p2_rt = False
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode("utf-8", "ignore")
    if "UART Timeout!" in uart_data:
        test.print_and_log("[red]UART Timeout!")
        return False, None
    if "Start Test:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.print_and_log(f"Running test {test.test_name}...")
    # uart_data = uart.read_data(test)
    # uart_data = uart_data.decode('utf-8', 'ignore')
    # if "Start Test:" in uart_data:
    #     test.test_name = uart_data.strip().split(": ")[1]
    #     test.print_and_log(f"Running test {test.test_name}...")
    if test.test_name == "gpio_lpu_ho":
        default_val = 1
        default_val_n = 0
        p1_rt = run_io_plud(default_val, default_val_n, False, analog)
        p2_rt = run_io_plud(default_val, default_val_n, True, analog)
    elif test.test_name == "gpio_lpd_ho":
        default_val = 0
        default_val_n = 1
        p1_rt = run_io_plud(default_val, default_val_n, False, analog)
        p2_rt = run_io_plud(default_val, default_val_n, True, analog)
    elif test.test_name == "gpio_lo_hpu":
        default_val = 1
        default_val_n = 0
        p1_rt = run_io_plud_h(default_val, default_val_n, False, analog)
        p2_rt = run_io_plud_h(default_val, default_val_n, True, analog)
    elif test.test_name == "gpio_lo_hpd":
        default_val = 0
        default_val_n = 1
        p1_rt = run_io_plud_h(default_val, default_val_n, False, analog)
        p2_rt = run_io_plud_h(default_val, default_val_n, True, analog)
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(1)
    if p1_rt and p2_rt:
        test.print_and_log("[green]passed")
        return True
    else:
        test.print_and_log("[red]failed")
        return False


def run_io_plud(default_val, default_val_n, first_itter, analog):
    """
    A function to run the IO_PLUD test.

    Args:
    - default_val: the default value
    - default_val_n: the default value for N
    - first_itter: a flag indicating if it's the first iteration

    Returns:
    - True if the test passes, False otherwise
    """
    test_counter = 0
    flag = False
    hk_stop(False)
    for channel in range(0, 38):
        if channel - 19 == 5 or channel - 19 == 6:
            continue
        if channel > 13 and channel < 22:
            io = test.deviced.dio_map[channel]
        elif channel > 21:
            io = test.device3v3.dio_map[channel]
        else:
            io = test.device1v8.dio_map[channel]
        if channel < 19 and first_itter:
            io.set_state(True)
            io.set_value(default_val_n)
        elif channel < 19:
            io.set_state(False)
        elif first_itter:
            if not flag:
                time.sleep(1)
                flag = True
            io_state = io.get_value()
            if io_state == default_val_n:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.print_and_log(f"[red]channel {channel-19} FAILED!")
        else:
            if not flag:
                time.sleep(1)
                flag = True
            io_state = io.get_value()
            if io_state == default_val:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.print_and_log(f"[red]channel {channel-19} FAILED!")
    hk_stop(True)
    if test_counter >= 17:
        # test.print_and_log(
        #     f"[green]{test.test_name} test passed"
        # )
        return True
    else:
        return False


def run_io_plud_h(default_val, default_val_n, first_itter, analog):
    """
    Function to run a series of IO operations based on specified conditions.

    Parameters:
    - default_val: the default value for IO operations
    - default_val_n: the default value for IO operations when first_itter is true
    - first_itter: a boolean flag indicating if it's the first iteration

    Returns:
    - True if the test passed, False if it failed
    """
    test_counter = 0
    flag = False
    hk_stop(False)
    for channel in range(37, -1, -1):
        if channel == 5 or channel == 6:
            continue
        if channel > 13 and channel < 22:
            io = test.deviced.dio_map[channel]
        elif channel > 21:
            io = test.device3v3.dio_map[channel]
        else:
            io = test.device1v8.dio_map[channel]
        if channel > 18 and first_itter:
            io.set_state(True)
            io.set_value(default_val_n)
        elif channel > 18:
            io.set_state(False)
        elif first_itter:
            if not flag:
                time.sleep(1)
                flag = True
            io_state = io.get_value()
            if io_state == default_val_n:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.print_and_log(f"[red]channel {channel+19} FAILED!")
        else:
            if not flag:
                time.sleep(1)
                flag = True
            io_state = io.get_value()
            if io_state == default_val:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.print_and_log(f"[red]channel {channel+19} FAILED!")
    hk_stop(True)
    if test_counter >= 17:
        # test.print_and_log(
        #     f"[green]{test.test_name} test Passed"
        # )
        return True
    else:
        return False


def concat_csv(root_directory, file_name):
    """
    Concatenates CSV files from a specified run directory into a single output file.

    Args:
        root_directory (str): The run directory containing the CSV files to be concatenated.
        file_name (str): The name of the CSV file to be concatenated.

    Returns:
        None
    """
    # Initialize a flag to track whether the header has been written
    header_written = False

    # Open the output file in write mode
    with open(
        f"{root_directory}/concatenated_{file_name}.csv", "w", newline=""
    ) as outfile:
        writer = csv.writer(outfile)

        # Traverse the directory tree
        for dirpath, dirnames, filenames in os.walk(root_directory):
            # Loop through each file
            for filename in filenames:
                if filename == f"{file_name}.csv":
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, "r", newline="") as infile:
                        reader = csv.reader(infile)

                        # Skip header except for the first file
                        if not header_written:
                            header_written = True
                        else:
                            next(reader)  # Skip the header

                        # Write rows to the output file
                        writer.writerows(reader)


def flash_test(
    test,
    hex_file,
    flash_flag,
    uart,
    uart_data,
    mgmt_gpio,
    io,
    plud,
    flash_only,
    verbose,
    analog,
    and_flag,
    chain,
    fpga_io,
    alu,
    sec_count,
    fpga_ram,
    ana,
):
    """
    A function to perform flash testing with various parameters and return the results.

    Args:
        test: The test object
        hex_file: The hex file to be flashed
        flash_flag: Flag to indicate if flashing is required
        uart: Flag to indicate if UART is required
        uart_data: Data for UART
        mgmt_gpio: Flag to indicate if management GPIO is required
        io: Flag to indicate if IO is required
        plud: Flag to indicate if PLUD is required
        flash_only: Flag to indicate if only flash is required
        verbose: Flag to indicate if verbose output is required

    Returns:
        The results of the flash test or a boolean value
    """
    if flash_only:
        run_only = False
    else:
        run_only = True
    test.reset_devices()
    test.reset()
    if flash_flag or flash_only:
        test.print_and_log(
            "=============================================================================="
        )
        test.print_and_log(
            f"  Flashing :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}"
        )
        test.print_and_log(
            "=============================================================================="
        )

        test.progress.update(
            test.task,
            description=f"Flashing {test.test_name}",
        )
        # test.power_down()
        # test.apply_reset()
        # test.power_up_1v8()
        test.gpio_mgmt.set_state(True)
        test.gpio_mgmt.set_value(1)
        # time.sleep(1)
        test.reset()
        test.flash(hex_file)
        # test.power_down()
        # test.release_reset()
    # else:
    #     test.power_down()
    #     time.sleep(0.1)
    # test.power_up()
    # test.device1v8.supply.set_voltage(test.l_voltage)
    # test.device3v3.supply.set_voltage(test.h_voltage)
    # test.reset()

    test.print_and_log(
        "=============================================================================="
    )
    test.print_and_log(
        f"  Running  :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}"
    )
    test.print_and_log(
        "=============================================================================="
    )

    results = None

    if run_only:
        test.progress.update(
            test.task,
            advance=1,
            description=f"Running {test.test_name} on low voltage {test.l_voltage}v and high voltage {test.h_voltage}v",
            visible=True,
        )
        if uart:
            results = process_uart(test, uart_data, verbose)
        elif mgmt_gpio:
            results = process_mgmt_gpio(test, verbose)
        elif io:
            results = process_io(test, uart_data, verbose, analog)
        elif plud:
            results = process_io_plud(test, uart_data, analog)
        elif and_flag:
            results = and_test(test, uart_data)
        elif chain:
            results = chain_test(test, uart_data)
        elif fpga_io:
            results = fpga_io_test(test, uart_data)
        elif alu:
            results = fpga_ALU_test(test, uart_data)
        elif sec_count:
            results = fpga_counter_test(test, uart_data)
        elif fpga_ram:
            results = fpga_ram_test(test)
        elif ana:
            results = adc_test(test, uart_data, verbose)
            if "adc" in test.test_name:
                concat_csv(test.date_dir, "adc_data")
            else:
                concat_csv(test.date_dir, "dac_data")
        else:
            results = process_soc(test, uart_data)
        return results
    else:
        return True


def reformat_csv(test, temp=None):
    """
    Read the original CSV file, create a new CSV file with the desired format, and write the reformatted data to the new CSV file.
    Parameters:
        test: The test object containing the date directory.
        temp: The temperature value (optional).
    """
    # Read the original CSV file
    with open(f"{test.date_dir}/results.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    ran_tests = []
    for d in data:
        if d[0] != "Test_name" and d[0] not in ran_tests:
            ran_tests.append(d[0])

    voltage_combinations = []
    for d in data:
        if d[0] != "Test_name":
            if [d[1], d[2]] not in voltage_combinations:
                voltage_combinations.append([d[1], d[2]])

    # Create a new CSV file with the desired format
    with open(f"{test.date_dir}/formatted_results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        if temp:
            header_row = ["Temp (C)", temp]
        else:
            header_row = ["Temp (C)", "N/A"]
        writer.writerow(header_row)

        header_row = ["VCCD (v)"]
        for v in voltage_combinations:
            header_row.append(v[0])
        writer.writerow(header_row)

        header_row = ["VDDIO (v)"]
        for v in voltage_combinations:
            header_row.append(v[1])
        writer.writerow(header_row)

        for t in ran_tests:
            header_row = [t]
            for d in data:
                if d[0] != "Test_name" and d[0] == t:
                    header_row.append(d[3])
            writer.writerow(header_row)


def config_fpga(test):
    """
    Configures the FPGA by setting the state and value of various pins. Returns the states and values of the configured pins.
    """
    prog_clk = test.device3v3.dio_map[37]
    prog_rst = test.device3v3.dio_map[29]
    io_isol_n = test.device1v8.dio_map[1]
    op_rst = test.device1v8.dio_map[11]
    ccff_head = test.device3v3.dio_map[34]
    ccff_tail = test.device3v3.dio_map[23]
    clk_sel = test.device3v3.dio_map[35]
    prog_clk.set_state(True)
    prog_rst.set_state(True)
    io_isol_n.set_state(True)
    ccff_head.set_state(True)
    clk_sel.set_state(True)
    op_rst.set_state(True)
    ccff_tail.set_state(False)
    prog_rst.set_value(0)
    prog_clk.set_value(0)
    clk_sel.set_value(0)
    io_isol_n.set_value(0)
    ccff_head.set_value(0)
    op_rst.set_value(0)
    return prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel


def program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array):
    """
    Program the FPGA using the provided test, programming clock, programming reset, ccff head, and binary array.
    """
    test.print_and_log("Programming FPGA...")
    prog_rst.set_value(1)
    time.sleep(0.1)
    for i in binary_array:
        ccff_head.set_value(i)
        prog_clk.set_value(1)
        prog_clk.set_value(0)
    prog_clk.set_value(0)


def load_bitstream(bitstream):
    """
    Load a bitstream from the specified file path and return it as a binary array.

    Parameters:
    bitstream (str): The name of the bitstream file to load.

    Returns:
    list: The binary array representing the loaded bitstream.
    """
    file_path = f"{os.path.dirname(os.path.realpath(__file__))}/silicon_tests/clear/bit_streams/{bitstream}.bit"
    binary_array = []
    with open(file_path, "r") as file:
        # Skip lines until reaching the binary data
        for line in file:
            if line.startswith("//"):
                continue
            else:
                # Remove any leading/trailing whitespace and append the binary values
                binary_array.extend([int(bit) for bit in line.strip()])

    return binary_array


def chain_test(test, uart):
    """
    Function to perform chain test using UART communication and FPGA programming.

    Args:
    - test: Test object containing GPIO management and UART communication methods.
    - uart: UART object for reading data from the test.

    Returns:
    - bool: True if the chain test passed, False otherwise.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode("utf-8", "ignore")
    if "UART Timeout!" in uart_data:
        test.print_and_log("[red]UART Timeout!")
        return False
    if "ST:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.print_and_log(f"Running test {test.test_name}...")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    binary_array = load_bitstream("and_3")
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    tail_value = []
    test.print_and_log("Reading data from chain tail")
    # time.sleep(0.1)
    for i in binary_array:
        chain_value = ccff_tail.get_value()
        if chain_value:
            chain_value = 1
        else:
            chain_value = 0
        tail_value.append(chain_value)
        prog_clk.set_value(1)
        prog_clk.set_value(0)

    if tail_value == binary_array:
        test.print_and_log("[green]Chain test passed")
        return True
    else:
        with open(f"bin_arr_and3.json", "w") as file:
            # Dump the array into the file using json.dump
            json.dump(binary_array, file)
        with open(f"tail_arr_and3.json", "w") as file:
            # Dump the array into the file using json.dump
            json.dump(tail_value, file)
        test.print_and_log("[red]Chain test failed")
        return False


def ALU_4bits(operand_A_bits, operand_B_bits, operation_bits, operand_a, operand_b):
    """
    Perform the 4-bit ALU operation using the given operand bits and operation bits.

    Parameters:
    - operand_A_bits: list of 4 bits representing operand A
    - operand_B_bits: list of 4 bits representing operand B
    - operation_bits: list of bits representing the operation
    - operand_a: list of indices for setting operand A bits
    - operand_b: list of indices for setting operand B bits
    """
    for i in range(4):
        bit_A = operand_A_bits[i]
        test.device1v8.dio_map[operand_a[i]].set_value(bit_A)
        # time.sleep(0.1)
        bit_B = operand_B_bits[i]
        test.device1v8.dio_map[operand_b[i]].set_value(bit_B)
        # time.sleep(0.1)


def config_alu(test, arr, dir):
    """
    Configures the ALU based on the input test, array, and direction.

    Parameters:
    test (obj): The test object containing device information.
    arr (list): The array of values to iterate through.
    dir (str): The direction for setting the state of the device.

    Returns:
    None
    """
    for i in arr:
        if i <= 13:
            a = test.device1v8.dio_map[i]
            a.set_state(dir)
        elif i > 21:
            a = test.device3v3.dio_map[i]
            a.set_state(dir)
        else:
            a = test.deviced.dio_map[i]
            a.set_state(dir)


def fpga_ALU_test(test, uart):
    """
    Function to perform testing of FPGA ALU functionality.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    operand_a = [4, 3, 2, 0]
    operand_b = [8, 7, 6, 5]
    result = [30, 28, 26, 24]
    operator = [13, 12]
    operand_a_bits = [[0, 1, 1, 1]]  # Example operand A values
    operand_b_bits = [[0, 1, 0, 0]]  # Example operand B values
    operations = [[0, 0], [0, 1], [1, 0], [1, 1]]  # Example operations
    result_bits = [[1, 0, 1, 1], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 1, 1]]
    # uart_data = uart.read_data(test)
    # uart_data = uart_data.decode('utf-8', 'ignore')
    # if "UART Timeout!" in uart_data:
    #     test.print_and_log("[red]UART Timeout!")
    #     return False
    # if "ST:" in uart_data:
    #     test.test_name = uart_data.strip().split(": ")[1]
    #     test.print_and_log(f"Running test {test.test_name}...")
    time.sleep(0.1)
    hk_stop(False)
    binary_array = load_bitstream("ALU_4bits")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    # time.sleep(0.1)
    clk_sel.set_value(1)
    # time.sleep(0.1)
    op_rst.set_value(1)
    # time.sleep(0.1)
    config_alu(test, operand_a, True)
    config_alu(test, operand_b, True)
    config_alu(test, operator, True)
    config_alu(test, result, False)
    # time.sleep(0.1)
    alu_res = []

    for operation in operations:
        for i in range(len(operand_a_bits)):
            for j in range(len(operation)):
                test.device1v8.dio_map[operator[j]].set_value(operation[j])
            # time.sleep(0.1)
            ALU_4bits(
                operand_a_bits[i], operand_b_bits[i], operation, operand_a, operand_b
            )
            # time.sleep(0.1)
            out_res = []
            for result_io in result:
                val = test.device3v3.dio_map[result_io].get_value()
                if val:
                    out_res.append(1)
                else:
                    out_res.append(0)
            alu_res.append(out_res)

    hk_stop(True)
    if alu_res == result_bits:
        test.print_and_log("[green]ALU test passed")
        return True
    else:
        test.print_and_log("[red]ALU test failed")
        test.print_and_log(f"alu_res = {alu_res}")
        test.print_and_log(f"result_bits = {result_bits}")
        return False


def fpga_counter_test(test, uart):
    """
    Function for testing FPGA counter. It takes a 'test' object and a 'uart' object as parameters and returns a boolean indicating the success of the test.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    # uart_data = uart.read_data(test)
    # uart_data = uart_data.decode('utf-8', 'ignore')
    # if "UART Timeout!" in uart_data:
    #     test.print_and_log("[red]UART Timeout!")
    #     return False
    # if "ST:" in uart_data:
    #     test.test_name = uart_data.strip().split(": ")[1]
    #     test.print_and_log(f"Running test {test.test_name}...")
    hk_stop(False)
    out_io = [3, 4, 5, 6, 7, 26, 28, 24]
    binary_array = load_bitstream("seconds_decoder_2")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)

    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    # time.sleep(0.1)
    clk_sel.set_value(1)
    # time.sleep(0.1)
    op_rst.set_value(1)
    # time.sleep(0.1)
    for channel in out_io:
        if channel < 14:
            io = test.device1v8.dio_map[channel]
            io.set_state(False)
        else:
            io = test.device3v3.dio_map[channel]
            io.set_state(False)
    count = 0
    io = []
    io_arr = []
    timeout = time.time() + 50
    while True:
        for channel in out_io:
            if channel < 14:
                io.append(test.device1v8.dio_map[channel].get_value())
            else:
                io.append(test.device3v3.dio_map[channel].get_value())
        if io.count(True) > 1:
            pass
        elif io not in io_arr:
            io_arr.append(io)

        if len(io_arr) == len(out_io):
            # Check that each sub-array has the True value shifted by 1 index
            result = all(
                io_arr[i][j]
                for i, row in enumerate(io_arr)
                for j, val in enumerate(row)
                if (i - j) == 1 and val
            )

            # Check that the total number of True values is equal to the length of the array
            total_true = sum(row.count(True) for row in io_arr)
            length = len(io_arr)
            result = result and total_true == length
            io_arr = []
            if result:
                count += 1
        io = []
        hk_stop(True)
        if count >= 3:
            test.print_and_log(f"[green]{test.test_name} passed")
            return True
        elif time.time() > timeout:
            test.print_and_log(f"[red]Error: {test.test_name} failed")
            return False


def fpga_io_test(test, uart):
    """
    Test the FPGA I/O by setting states and values, checking for errors, and returning a boolean value.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    # uart_data = uart.read_data(test)
    # uart_data = uart_data.decode('utf-8', 'ignore')
    # if "UART Timeout!" in uart_data:
    #     test.print_and_log("[red]UART Timeout!")
    #     return False
    # if "ST:" in uart_data:
    #     test.test_name = uart_data.strip().split(": ")[1]
    #     test.print_and_log(f"Running test {test.test_name}...")
    time.sleep(0.1)
    hk_stop(False)
    if test.test_name == "inv_1":
        out = [21, 20, 19, 18, 17, 16, 15, 13, 12, 8, 7, 6]
        inp = [5, 4, 3, 2, 0, 33, 32, 31, 30, 28, 26, 24]
        binary_array = load_bitstream("inv_all_1")
    elif test.test_name == "inv_2":
        inp = [21, 20, 19, 18, 17, 16, 15, 13, 12, 8, 7, 6]
        out = [5, 4, 3, 2, 0, 33, 32, 31, 30, 28, 26, 24]
        binary_array = load_bitstream("inv_all_2")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    # time.sleep(1)
    clk_sel.set_value(1)
    # time.sleep(20)
    op_rst.set_value(1)
    # time.sleep(20)
    fail = False
    count = 0
    for inp_ut in inp:
        # test.print_and_log(f"now testing {inp_ut} only {out[count]} should toggle")
        for channel in inp:
            if channel > 13 and channel < 22:
                io = test.deviced.dio_map[channel]
            elif channel > 21:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            io.set_state(True)
            io.set_value(0)

        if inp_ut > 13 and inp_ut < 22:
            io_ut = test.deviced.dio_map[inp_ut]
        elif inp_ut > 21:
            io_ut = test.device3v3.dio_map[inp_ut]
        else:
            io_ut = test.device1v8.dio_map[inp_ut]
        io_ut.set_state(True)
        io_ut.set_value(1)
        # time.sleep(5)
        for channel in out:
            if channel > 13 and channel < 22:
                io = test.deviced.dio_map[channel]
            elif channel > 21:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            io.set_state(False)
            # time.sleep(1)
            io_val = io.get_value()
            if not io_val and not out[count] == channel:
                test.print_and_log(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            elif io_val and out[count] == channel:
                test.print_and_log(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            # else:
            #     test.print_and_log(f"[green]io {channel} = {io_val}")

        # time.sleep(5)
        for channel in inp:
            if channel > 13 and channel < 22:
                io = test.deviced.dio_map[channel]
            elif channel > 21:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            io.set_state(True)
            io.set_value(1)

        io_ut.set_value(0)

        # time.sleep(5)
        for channel in out:
            if channel > 13 and channel < 22:
                io = test.deviced.dio_map[channel]
            elif channel > 21:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            io.set_state(False)
            # time.sleep(1)
            io_val = io.get_value()
            if io_val and not out[count] == channel:
                test.print_and_log(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            elif not io_val and out[count] == channel:
                test.print_and_log(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            # else:
            #     test.print_and_log(f"[green]io {channel} = {io_val}")
        count += 1

    hk_stop(True)
    if fail:
        return False
    else:
        test.print_and_log("[green]Test Passed!")
        return True


def and_test(test, uart):
    """
    This function performs a series of operations to test the functionality of an FPGA AND gate. It takes 'test' and 'uart' as parameters and returns a boolean value indicating the success of the test.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode("utf-8", "ignore")
    if "UART Timeout!" in uart_data:
        test.print_and_log("[red]UART Timeout!")
        return False
    if "ST:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.print_and_log(f"Running test {test.test_name}...")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    a = test.deviced.dio_map[21]
    b = test.deviced.dio_map[20]
    c = test.deviced.dio_map[19]
    a.set_state(True)
    b.set_state(True)
    c.set_state(False)
    a.set_value(0)
    b.set_value(0)
    binary_array = load_bitstream("and_3")
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    # time.sleep(0.1)
    clk_sel.set_value(1)
    # time.sleep(0.1)
    op_rst.set_value(1)
    # time.sleep(0.1)
    a.set_value(0)
    b.set_value(0)
    time.sleep(0.1)
    c_val = c.get_value()
    if c_val:
        test.print_and_log(f"[red] a = 0, b = 0, c = {c_val}")
        return False
    a.set_value(0)
    b.set_value(1)
    time.sleep(0.1)
    c_val = c.get_value()
    if c_val:
        test.print_and_log(f"[red] a = 0, b = 1, c = {c_val}")
        return False
    a.set_value(1)
    b.set_value(0)
    time.sleep(0.1)
    c_val = c.get_value()
    if c_val:
        test.print_and_log(f"[red] a = 1, b = 0, c = {c_val}")
        return False
    a.set_value(1)
    b.set_value(1)
    time.sleep(0.1)
    c_val = c.get_value()
    if not c_val:
        test.print_and_log(f"[red] a = 1, b = 1, c = {c_val}")
        return False
    test.print_and_log("[green]fpga AND test passed")
    return True


def ram_write_data(test, data, addr, wdata_io, addr_io, we_io):
    """
    Writes data to the RAM using the specified parameters.
    Parameters:
    - test: the test object
    - data: the data to be written to RAM
    - addr: the address to write the data to
    - wdata_io: the I/O for the data
    - addr_io: the I/O for the address
    - we_io: the write enable I/O
    """
    if we_io > 16:
        io = test.device3v3.dio_map[we_io]
    else:
        io = test.device1v8.dio_map[we_io]
    io.set_state(True)
    io.set_value(0)
    time.sleep(0.1)
    for channel_idx in range(len(data)):
        if wdata_io[channel_idx] > 13 and wdata_io[channel_idx] < 22:
            io = test.deviced.dio_map[wdata_io[channel_idx]]
        elif wdata_io[channel_idx] > 21:
            io = test.device3v3.dio_map[wdata_io[channel_idx]]
        else:
            io = test.device1v8.dio_map[wdata_io[channel_idx]]
        io.set_state(True)
        io.set_value(data[channel_idx])
    for channel_idx in range(len(addr)):
        if addr_io[channel_idx] > 13 and addr_io[channel_idx] < 22:
            io = test.deviced.dio_map[addr_io[channel_idx]]
        elif addr_io[channel_idx] > 21:
            io = test.device3v3.dio_map[addr_io[channel_idx]]
        else:
            io = test.device1v8.dio_map[addr_io[channel_idx]]
        io.set_state(True)
        io.set_value(addr[channel_idx])
    time.sleep(0.1)
    if we_io > 16:
        io = test.device3v3.dio_map[we_io]
    else:
        io = test.device1v8.dio_map[we_io]
    io.set_state(True)
    io.set_value(1)
    time.sleep(0.1)


def ram_read_data(test, wdata_io, addr_io, we_io, rdata_io, addr):
    """
    Reads data from the RAM and performs corresponding I/O operations based on the given parameters.

    Args:
        test: The test object.
        wdata_io: List of I/O channels for write data.
        addr_io: List of I/O channels for memory address.
        we_io: The I/O channel for write enable signal.
        rdata_io: List of I/O channels for read data.
        addr: Memory address to read from.

    Returns:
        List of boolean values representing the read data from RAM.
    """
    if we_io > 16:
        io = test.device3v3.dio_map[we_io]
    else:
        io = test.device1v8.dio_map[we_io]
    io.set_state(True)
    io.set_value(0)
    rdata = []
    for channel_idx in range(len(wdata_io)):
        if wdata_io[channel_idx] > 13 and wdata_io[channel_idx] < 22:
            io = test.deviced.dio_map[wdata_io[channel_idx]]
        elif wdata_io[channel_idx] > 21:
            io = test.device3v3.dio_map[wdata_io[channel_idx]]
        else:
            io = test.device1v8.dio_map[wdata_io[channel_idx]]
        io.set_state(True)
        io.set_value(0)
    for channel_idx in range(len(addr_io)):
        if addr_io[channel_idx] > 13 and addr_io[channel_idx] < 22:
            io = test.deviced.dio_map[addr_io[channel_idx]]
        elif addr_io[channel_idx] > 21:
            io = test.device3v3.dio_map[addr_io[channel_idx]]
        else:
            io = test.device1v8.dio_map[addr_io[channel_idx]]
        io.set_state(True)
        io.set_value(addr[channel_idx])
    time.sleep(0.1)
    for channel_idx in range(len(rdata_io)):
        if rdata_io[channel_idx] > 16:
            io = test.device3v3.dio_map[rdata_io[channel_idx]]
        else:
            io = test.device1v8.dio_map[rdata_io[channel_idx]]
        io.set_state(False)
        rdata.append(io.get_value())

    rdata_bool = [int(boolean) for boolean in rdata]

    return rdata_bool


def fpga_ram_test(test):
    """
    This function performs a test on FPGA RAM. It sets the GPIO management state, configures the FPGA based on the test name, and then performs a series of RAM write and read operations. If the test passes, it returns True; otherwise, it returns False.
    """
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    hk_stop(False)
    if test.test_name == "fpga_ram8x20":
        we_io = 32
        wdata_io = [20, 19, 18, 17, 16, 15, 13, 12]
        addr_io = [31, 30, 28, 26, 24]
        rdata_io = [8, 7, 6, 5, 4, 3, 2, 0]
        reg_size = 20
        binary_array = load_bitstream("fpga_ram8x20")
    elif test.test_name == "fpga_ram6x26":
        we_io = 7
        wdata_io = [18, 17, 16, 15, 13, 12]
        addr_io = [31, 30, 28, 26, 24]
        rdata_io = [6, 5, 4, 3, 2, 0]
        reg_size = 26
        binary_array = load_bitstream("fpga_ram6x26")

    time.sleep(0.1)
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    # time.sleep(0.1)
    clk_sel.set_value(1)
    # time.sleep(0.1)
    op_rst.set_value(1)
    # time.sleep(0.1)
    flag = True
    for j in range(0, reg_size):
        wdata_word = bin(j)[2:].zfill(len(wdata_io))
        wdata_bits = [int(bit) for bit in wdata_word]
        addr_word = bin(j)[2:].zfill(len(addr_io))
        addr_bits = [int(bit) for bit in addr_word]
        ram_write_data(test, wdata_bits, addr_bits, wdata_io, addr_io, we_io)
        # time.sleep(2)
        # for j in range(0, reg_size):
        #     wdata_word = bin(j)[2:].zfill(len(wdata_io))
        #     wdata_bits = [int(bit) for bit in wdata_word]
        addr_word = bin(j)[2:].zfill(len(addr_io))
        addr_bits = [int(bit) for bit in addr_word]
        rdata = ram_read_data(test, wdata_io, addr_io, we_io, rdata_io, addr_bits)

        if rdata != wdata_bits:
            # test.print_and_log(
            #     f"[red]wdata = {wdata_bits}, addr = {addr_bits}, rdata = {rdata}"
            # )
            flag = False
        # else:
        # test.print_and_log(
        #     f"[green]wdata = {wdata_bits}, addr = {addr_bits}, rdata = {rdata}"
        # )

    hk_stop(True)
    if flag:
        test.print_and_log("[green]Test passed")
        return True
    else:
        test.print_and_log("[green]Test failed")
        return False


def adc_test(test, uart, verbose):
    """
    Function to perform ADC test and return True if successful, False otherwise.
    Parameters:
    - test: object representing test parameters
    - uart: object for UART communication
    - verbose: boolean indicating whether to print additional information
    Return type: boolean
    """
    volt_dir = os.path.join(test.date_dir, f"{test.l_voltage}_{test.h_voltage}")
    os.makedirs(volt_dir, exist_ok=True)
    if test.test_name == "adc_test":
        test.device3v3.dio_map[22].set_state(True)
        test.device3v3.dio_map[22].set_value(1)
        # Prepare the Digilent logic analyzer
        # open(device_data, sampling_frequency=100e06, buffer_size=0)
        logic.open(test.device3v3.ad_device, 1e5, 1)

        # trigger(device_data, enable, channel, position=0, timeout=0,
        #      rising_edge=True, length_min=0, length_max=20, count=0)
        # logic.trigger(devdata, False, 0)
        #
        # Better:  Define a trigger channel and trigger on pulse
        # from Caravel to be defined whenever it runs a new ADC conversion
        # logic.trigger(test.device3v3.ad_device, True, 10)

        uart_data = uart.read_data(test)
        uart_data = uart_data.decode("utf-8", "ignore")
        if "UART Timeout!" in uart_data:
            test.print_and_log("[red]UART Timeout!")
            return False
        if "ST:" in uart_data:
            test.test_name = uart_data.strip().split(": ")[1]
            test.print_and_log(f"Running test {test.test_name}...")
        # test.reset()

        numvals = 1024
        uart_data = ""

        data = [
            [
                "VDDIO (v)",
                "VCCD (v)",
                "clk freq (MHz)",
                "clk div",
                "ABS Max INL (lsb)",
                "ABS Max INL (lsb 0 to 2.6V)",
                "Corrected Max INL (lsb)",
                "Corrected Max INL (lsb 0 to 2.6V)",
                "Max DNL (lsb)",
                "Offset error (mV)",
                "Gain error (%)",
            ]
        ]

        clk_freq = ["2.5", "1.67", "1", "0.813", "0.714", "0.385"]

        # Write data to a CSV file
        adc_dir = os.path.join(volt_dir, "ADC")
        os.makedirs(adc_dir, exist_ok=True)
        csv_filename = f"{adc_dir}/adc_data.csv"
        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        for clkdiv in range(0, 6):
            invals = []
            outvals = []
            mult_outvals = []
            uart_data = uart.read_data(test)
            uart_data = uart_data.decode("utf-8", "ignore")
            if "UART Timeout!" in uart_data:
                test.print_and_log("[red]UART Timeout!")
                return False
            if "clkdiv:" in uart_data:
                clk_div = uart_data.strip().split(": ")[1]
            test.print_and_log(f"clk_div value: {clk_div}")
            test.print_and_log(f"clk freq (MHz): {clk_freq[clkdiv]}")
            test.device3v3.dio_map[22].set_value(0)
            for i in range(0, 40):
                invals = []
                outvals = []
                for v in range(0, numvals):
                    volt = 3.3 * (float(v) / float(numvals))
                    # Set value on W1:  Test DC value at 1.5V (set by offset, not amplitude)
                    # generate(device_data, channel, function, offset, frequency=1e03,
                    #      amplitude=1, symmetry=50, wait=0, run_time=0, repeat=0, data=[])
                    wavegen.generate(
                        test.device3v3.ad_device,
                        1,
                        wavegen.function.dc,
                        volt,
                        1e3,
                        0,
                        50,
                        0,
                        0,
                        0,
                    )
                    logic.trigger(test.device3v3.ad_device, True, 10)
                    # time.sleep(0.05)
                    # print("triggered!")

                    # Read ADC value back from GPIO 24-31, connected to Digilent 2-9.
                    # Use "recordall" (function added to existing SDK)

                    value = 0
                    buffer = logic.recordall(test.device3v3.ad_device)
                    for i in range(2, 10):
                        value += buffer[i][0]

                    if verbose:
                        test.print_and_log(
                            "Input voltage = "
                            + str(volt)
                            + ";  captured value = "
                            + str(value)
                        )
                    invals.append(volt)
                    outvals.append(value)

                mult_outvals.append(outvals)

            # Transpose the array to get columns as rows
            transposed_a1 = list(map(list, zip(*mult_outvals)))

            # Calculate the average for each column
            averages = [sum(column) / len(column) for column in transposed_a1]

            # Calculate the noise for each column
            noises = [max(column) - min(column) for column in transposed_a1]

            # Create a figure with two subplots
            fig = plt.figure()

            # Plot the average against the input values
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.plot(invals, averages, "b", label="Average")
            ax1.set_ylabel("Average")

            # Plot the noise against the input values
            ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
            ax2.plot(invals, noises, "r", label="Noise")
            ax2.set_xlabel("Input Values")
            ax2.set_ylabel("Noise")

            # Add legend to the plots
            ax1.legend()
            ax2.legend()

            # Set title
            fig.suptitle(
                f"Average and Noise Plot for {clk_freq[clkdiv]}MHz clock Freqency"
            )

            # Adjust layout
            plt.tight_layout()

            # Save the plot as a PNG file
            plt.savefig(f"{adc_dir}/average_and_noise_{clk_freq[clkdiv]}.png")

            # Show the plot
            # plt.show()

            # print(averages)

            with open(f"{adc_dir}/adc_results_{clk_freq[clkdiv]}.dat", "w") as ofile:
                print(" ".join(map(str, invals)), file=ofile)
                print(" ".join(map(str, averages)), file=ofile)
            with open(f"{adc_dir}/adc_noise_{clk_freq[clkdiv]}.dat", "w") as ofile:
                print(" ".join(map(str, invals)), file=ofile)
                print(" ".join(map(str, noises)), file=ofile)

            vhighval = 3.3
            vlowval = 0.0
            fsr = vhighval - vlowval
            alsb = fsr / 256.0

            x0 = np.arange(1024)
            y = np.floor(x0 / 4)

            # Curve fit to get gain and offset values
            p = np.polyfit(y, averages, 1)
            slope = p[0]
            offset = p[1]

            # Calculate INL for this result (absolute)
            vin = np.arange(1024) * (3.3 / 1024)
            iout = np.array(averages)
            vout = iout * alsb
            inl = (vout - vin) / alsb

            max_inl_abs = np.max(np.abs(inl))
            max_inl_abs_0_to_2_6V = np.max(np.abs(inl[2:807]))

            # Curve fit to vout(1:800) to get offset and gain
            p = np.polyfit(np.arange(2, 801), vout[1:800], 1)

            # Calculate INL for this result (accounting for gain and offset)
            ioutcor = (vout - p[1]) / p[0]
            voutcor = (ioutcor / 4) * alsb
            inlcor = (voutcor - vin) / alsb

            max_inl_cor = np.max(np.abs(inlcor))
            max_inl_cor_0_to_2_6V = np.max(np.abs(inlcor[2:807]))

            # Calculate DNL for this result
            dnl = ((vout[6:1023:4] - vout[2:1019:4]) / alsb) - 1
            max_dnl = np.max(np.abs(dnl))

            # Report offset and gain error
            slope = p[0]
            offset = p[1]
            offset_error = offset * 1000
            gain_error = 100 * abs((slope * 4 / alsb) - 1)

            test.print_and_log("Absolute INL:")
            test.print_and_log(f"Maximum INL (in lsb) = {max_inl_abs}")
            test.print_and_log(
                f"Maximum INL (in lsb) from 0 to 2.6V = {max_inl_abs_0_to_2_6V}"
            )

            test.print_and_log("INL corrected for gain and offset:")
            test.print_and_log(f"Maximum INL (in lsb) = {max_inl_cor}")
            test.print_and_log(
                f"Maximum INL (in lsb) from 0 to 2.6V = {max_inl_cor_0_to_2_6V}"
            )

            test.print_and_log(f"Maximum DNL (in lsb) = {max_dnl}")

            test.print_and_log("Offset error = {:.3f}mV".format(offset_error))
            test.print_and_log("Gain error = {:.3f}%".format(gain_error))

            data = [
                [
                    test.h_voltage,
                    test.l_voltage,
                    clk_freq[clkdiv],
                    clk_div,
                    max_inl_abs,
                    max_inl_abs_0_to_2_6V,
                    max_inl_cor,
                    max_inl_cor_0_to_2_6V,
                    max_dnl,
                    offset_error,
                    gain_error,
                ]
            ]

            # Write data to a CSV file
            csv_filename = f"{adc_dir}/adc_data.csv"
            with open(csv_filename, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
            test.device3v3.dio_map[22].set_value(1)
        return True

    elif test.test_name == "dac_test":
        uart_data = uart.read_data(test)
        uart_data = uart_data.decode("utf-8", "ignore")
        if "UART Timeout!" in uart_data:
            test.print_and_log("[red]UART Timeout!")
            return False
        if "ST:" in uart_data:
            test.test_name = uart_data.strip().split(": ")[1]
            test.print_and_log(f"Running test {test.test_name}...")
        # Prepare the Digilent I/O for static function
        for k in range(2, 10):
            # Enable channel for digital output (output=True is output)
            # set_mode(device_data, channel, output)
            static.set_mode(test.device3v3.ad_device, k, True)

        # Prepare the Digilent scope for signal capture
        # open(device_data, sampling_frequency=20e06, buffer_size=0,
        # 	offset=0, amplitude_range=5)
        #
        scope.open(test.device3v3.ad_device, 20e6, 1, 0, 10)

        # Set up the scope to trigger on T1, and connect T1 to GPIO 33.
        # The "blizzard_dac_test.c" outputs on that pin.
        # trigger(device_data, enable, source=trigger_source.none, channel=1,
        # 	timeout=0, edge_rising=True, level=0)
        # scope.trigger(test.device3v3.ad_device, True, scope.trigger_source.external[1], 1, 0, True, 1.65)

        digvals = []
        invals = []
        outvals = []
        captured_voltage = []
        expected_voltage = []
        digital_values = []
        diff_arr = []
        numvals = 256
        for v in range(0, numvals):
            volt = 3.3 * (float(v) / float(numvals))

            scope.trigger(
                test.device3v3.ad_device,
                True,
                scope.trigger_source.external[1],
                1,
                0,
                True,
                1.65,
            )

            # Apply binary value as pattern to GPIO 24-31
            for k in range(0, 8):
                test.device3v3.dio_map[k + 24].set_state(True)
                # print(f"v: {v}, k: {k}, value: {(v >> k) & 1}")
                # print((v >> k) & 1)
                test.device3v3.dio_map[k + 24].set_value((v >> k) & 1)
                # static.set_allstates(test.device3v3.ad_device, v)

            time.sleep(0.05)
            # pulse_count = test.receive_packet(250)
            # test.print_and_log("clk_div value:", pulse_count)

            # Read DAC value back from GPIO 15
            samples = 64
            value = 0
            for i in range(0, samples):
                # scope.trigger(test.device3v3.ad_device, True, scope.trigger_source.external[1], 1, 0, True, 1.65)
                value += scope.measure(test.device3v3.ad_device, 1)
            value /= float(samples)

            if verbose:
                test.print_and_log(
                    "Output value = "
                    + str(v)
                    + ";  expected voltage = "
                    + str(volt)
                    + ";  captured voltage = "
                    + str(value)
                )
            digvals.append(str(v))
            invals.append(str(volt))
            outvals.append(str(value))

            # Calculate the difference between the captured voltage and expected voltage
            diff = volt - value

            # Append the values to the corresponding lists
            digital_values.append(v)
            captured_voltage.append(value)
            expected_voltage.append(volt)
            diff_arr.append(diff)

        # Create a single figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

        # Plot captured voltage and expected voltage against digital values
        # plt.figure()
        ax1.plot(digital_values, captured_voltage, "b", label="Captured Voltage")
        ax1.plot(digital_values, expected_voltage, "r", label="Expected Voltage")
        ax1.set_xlabel("Digital Values")
        ax1.set_ylabel("Voltage")
        ax1.legend()
        ax1.set_title("Captured Voltage and Expected Voltage")
        # ax1.savefig('DAC_captured_vs_expected.png')

        # Create the plot for the difference between captured voltage and expected voltage against digital values
        # plt.figure()
        ax2.plot(digital_values, diff_arr, "g", label="Difference")
        ax2.set_xlabel("Digital Values")
        ax2.set_ylabel("Voltage Difference")
        ax2.legend()
        ax2.set_title("Difference between Captured Voltage and Expected Voltage")
        # Adjust spacing between subplots
        plt.tight_layout()
        dac_dir = os.path.join(volt_dir, "DAC")
        os.makedirs(dac_dir, exist_ok=True)
        plt.savefig(f"{dac_dir}/DAC_captured_vs_expected.png")
        plt.close(fig)

        with open(f"{dac_dir}/dac_results.dat", "w") as ofile:
            print(" ".join(digvals), file=ofile)
            print(" ".join(invals), file=ofile)
            print(" ".join(outvals), file=ofile)

        # Full Scale Range (FSR) and Least Significant Bit (LSB)
        fsr = 3.3 - 0.0
        alsb = fsr / 256.0

        # Calculate INL for this result
        vin = np.arange(256) * (3.3 / 256)
        vout = np.array(captured_voltage)
        inl = (vout - vin) / alsb

        max_inl_abs = np.max(np.abs(inl))
        max_inl_abs_0_to_2_6V = np.max(np.abs(inl[:202]))

        # Curve fit to vout(1:215) to get offset and gain
        p = np.polyfit(vin[:215], vout[:215], 1)

        # Calculate INL for this result (accounting for gain and offset)
        voutcor = (vout - p[1]) / p[0]
        inlcor = (voutcor - vin) / alsb

        max_inl_cor = np.max(np.abs(inlcor))
        max_inl_cor_0_to_2_6V = np.max(np.abs(inlcor[:202]))

        # Calculate DNL for this result
        dnl = ((vout[1:] - vout[:-1]) / alsb) - 1
        max_dnl = np.max(np.abs(dnl))

        # Report gain and offset error
        slope = p[0]
        offset = p[1]

        offset_error = offset * 1000
        gain_error = 100 * abs(slope - 1)

        # Print calculated values
        test.print_and_log("Absolute INL:")
        test.print_and_log(f"Maximum INL (in lsb) = {max_inl_abs}")
        test.print_and_log(
            f"Maximum INL (in lsb) from 0 to 2.6V = {max_inl_abs_0_to_2_6V}"
        )

        test.print_and_log("INL corrected for gain and offset:")
        test.print_and_log(f"Maximum INL (in lsb) = {max_inl_cor}")
        test.print_and_log(
            f"Maximum INL (in lsb) from 0 to 2.6V = {max_inl_cor_0_to_2_6V}"
        )

        test.print_and_log(f"Maximum DNL (in lsb) = {max_dnl}")

        test.print_and_log("Offset error = {:.3f}mV".format(offset_error))
        test.print_and_log("Gain error = {:.3f}%".format(gain_error))
        data = [
            [
                "VDDIO (v)",
                "VCCD (v)",
                "Absolute max INL",
                "Abs max INL from 0 to 2.6v",
                "Corrected max INL",
                "Corrected max INL from 0 to 2.6v",
                "Max DNL",
                "Offset error",
                "Gain error",
            ],
            [
                test.h_voltage,
                test.l_voltage,
                max_inl_abs,
                max_inl_abs_0_to_2_6V,
                max_inl_cor,
                max_inl_cor_0_to_2_6V,
                max_dnl,
                gain_error,
            ],
        ]

        # Write data to a CSV file
        csv_filename = f"{dac_dir}/dac_data.csv"
        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        return True


def exec_test(
    test,
    start_time,
    hex_file,
    flash_flag=True,
    uart=False,
    uart_data=None,
    mgmt_gpio=False,
    io=False,
    plud=False,
    flash_only=False,
    verbose=False,
    analog=False,
    and_flag=False,
    chain=False,
    fpga_io=False,
    alu=False,
    sec_count=False,
    fpga_ram=False,
    ana=False,
):
    """
    Executes a test and writes the results to a CSV file.

    Args:
        test: The test to be executed.
        start_time: The start time of the test.
        hex_file: The hex file to be used for the test.
        flash_flag: A boolean indicating whether flashing is required (default is True).
        uart: A boolean indicating whether UART is required (default is False).
        uart_data: Data for UART, if UART is required (default is None).
        mgmt_gpio: A boolean indicating whether management GPIO is required (default is False).
        io: A boolean indicating whether IO is required (default is False).
        plud: A boolean indicating whether PLUD is required (default is False).
        flash_only: A boolean indicating whether only flashing is required (default is False).
        verbose: A boolean indicating whether verbose output is required (default is False).

    Returns:
        None
    """
    results = False
    results = flash_test(
        test,
        hex_file,
        flash_flag,
        uart,
        uart_data,
        mgmt_gpio,
        io,
        plud,
        flash_only,
        verbose,
        analog,
        and_flag,
        chain,
        fpga_io,
        alu,
        sec_count,
        fpga_ram,
        ana,
    )
    end_time = time.time() - start_time
    arr = []

    if type(results) is bool:
        if results:
            arr.append(
                [test.test_name, test.l_voltage, test.h_voltage, "passed", end_time]
            )
        else:
            arr.append(
                [test.test_name, test.l_voltage, test.h_voltage, "failed", end_time]
            )
    elif type(results) is tuple:
        if type(results[0]) is bool:
            if results[0]:
                arr.append(
                    [test.test_name, test.l_voltage, test.h_voltage, "passed", end_time]
                )
            else:
                arr.append(
                    [
                        test.test_name,
                        test.l_voltage,
                        test.h_voltage,
                        f"failed, {results[1]}",
                        end_time,
                    ]
                )
    elif type(results) is list:
        for result in results:
            if result[1]:
                arr.append(
                    [
                        result[0],
                        test.l_voltage,
                        test.h_voltage,
                        "passed",
                        end_time / len(results),
                    ]
                )
            else:
                arr.append(
                    [
                        result[0],
                        test.l_voltage,
                        test.h_voltage,
                        "failed",
                        end_time / len(results),
                    ]
                )
    elif type(results) is str:
        arr.append(
            [
                test.test_name,
                test.l_voltage,
                test.h_voltage,
                results,
                "%.2f" % (end_time),
            ]
        )

    with open(f"{test.date_dir}/results.csv", "a", encoding="UTF8") as f:
        writer = csv.writer(f)
        for test in arr:
            writer.writerow(test)


def get_last_test_name(test):
    """
    Get the last test name and its date directory.

    Parameters:
    test (object): The test object containing the runs directory.

    Returns:
    tuple: A tuple containing the last flashed test name and its date directory.
    """
    # Get the last test.date_dir
    date_dirs = sorted(
        [
            d
            for d in os.listdir(test.runs_dir)
            if os.path.isdir(os.path.join(test.runs_dir, d))
        ]
    )
    last_date_dir = date_dirs[-1]

    # Read the results.csv file in the last test.date_dir
    with open(os.path.join(test.runs_dir, last_date_dir, "flash.log"), "r") as file:
        lines = file.readlines()

    # Search for the last occurrence of the "Flashed <test_name>" pattern
    last_flashed_test = None
    for line in reversed(lines):
        if "Flashed" in line:
            last_flashed_test = line.split("Flashed ")[1].split(" ")[0]
            break

    return last_flashed_test, last_date_dir


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="SI validation.")
        parser.add_argument(
            "-f",
            "--flash_only",
            help="Only Flash test",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-r",
            "--run_only",
            help="Run test without flash",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help="Run with high verbosity",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-t",
            "--test",
            help="Run Standalone test if in manifest",
        )
        parser.add_argument(
            "-temp",
            "--temperature",
            help="Temperature monitoring",
        )
        parser.add_argument(
            "-l",
            "--last_test",
            action="store_true",
            default=False,
            help="Start the regression from the last test in the runs directory",
        )
        parser.add_argument("--manifest", type=str, help="Path to the manifest file")
        args = parser.parse_args()
        # Import specified manifest file
        if args.manifest is None:
            manifest_path = "manifest.py"
        else:
            manifest_path = args.manifest
        if not os.path.exists(manifest_path):
            print(f"Manifest file not found: {manifest_path}")
            sys.exit(1)

        spec = importlib.util.spec_from_file_location("manifest_module", manifest_path)
        manifest_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(manifest_module)
        # open multiple devices
        devices = device.open_devices()
        # connect devices using hardcoded serial numbers
        d1_sn = bytes(manifest_module.device1_sn, "utf-8")
        d2_sn = bytes(manifest_module.device2_sn, "utf-8")
        d3_sn = bytes(manifest_module.device3_sn, "utf-8")
        device1_data, device2_data, device3_data = connect_devices(
            devices, d1_sn, d2_sn, d3_sn
        )

        # logging.info("   Initializing I/Os for both devices")
        # Initializing I/Os
        device1_dio_map, device2_dio_map, device3_dio_map = init_ad_ios(
            device1_data, device2_data, device3_data
        )
        # Initilizing devices
        device1 = Device(device1_data, 0, device1_dio_map)
        device2 = Device(device2_data, 1, device2_dio_map)
        device3 = Device(device3_data, 2, device3_dio_map)

        test = Test(device1, device2, device3)
        uart_data = UART(device1_data)
        spi = SPI(device1_data)

        csv_header = [
            "Test_name",
            "Low Voltage (v)",
            "High Voltage (v)",
            "Pass/Fail",
            "Time (s)",
        ]

        if args.last_test:
            last_test_name, last_date_dir = get_last_test_name(test)
            # Find the index of the test to start from
            start_index = next(
                (
                    i
                    for i, test in enumerate(manifest_module.TestDict)
                    if test["test_name"] == last_test_name
                ),
                None,
            )

            if start_index is not None:
                # Create a new TestDict list starting from the specified test
                manifest_module.TestDict = manifest_module.TestDict[start_index:]
            test.date_dir = f"{test.runs_dir}/{last_date_dir}"
        else:
            test.make_runs_dirs()
            with open(f"{test.date_dir}/results.csv", "a", encoding="UTF8") as f:
                writer = csv.writer(f)
                writer.writerow(csv_header)

        test.print_and_log(
            "=============================================================================="
        )
        if manifest_module.analog:
            test.print_and_log("  Beginning Tests for analog project")
        else:
            test.print_and_log("  Beginning Tests for digital project")
        test.print_and_log(
            "=============================================================================="
        )

        test_flag = False

        test.task = test.progress.add_task(
            "SI validation",
            total=(
                len(manifest_module.TestDict)
                * len(manifest_module.l_voltage)
                * len(manifest_module.h_voltage)
            ),
        )
        test.progress.start()
        # if not args.run_only:
        #     test.power_down()
        #     test.apply_reset()
        #     test.power_up_1v8()
        #     test.flash(f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/blizzard/setup/setup.hex")
        #     test.power_down()
        #     test.release_reset()
        for v in manifest_module.l_voltage:
            for h in manifest_module.h_voltage:
                test.l_voltage = v
                test.h_voltage = h
                test.power_down()
                test.device1v8.supply.set_voltage(test.l_voltage)
                test.device3v3.supply.set_voltage(test.h_voltage)
                test.power_up()
                # test.reset()
                for t in manifest_module.TestDict:
                    if not args.test or args.test == t["test_name"]:
                        test.test_name = t["test_name"]
                        test.passing_criteria = t["passing_criteria"]
                        flash_flag = True
                        counter = 0
                        test_flag = True
                        start_time = time.time()
                        if counter > 0 or args.run_only:
                            flash_flag = False
                        if t.get("uart"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                uart=t.get("uart"),
                                uart_data=uart_data,
                                flash_only=args.flash_only,
                                verbose=args.verbose,
                                analog=manifest_module.analog,
                            )
                        elif t.get("mgmt_gpio"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                mgmt_gpio=t.get("mgmt_gpio"),
                                flash_only=args.flash_only,
                                verbose=args.verbose,
                                analog=manifest_module.analog,
                            )
                        elif t.get("io"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                io=t.get("io"),
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                verbose=args.verbose,
                                analog=manifest_module.analog,
                            )
                        elif t.get("plud"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                plud=t.get("plud"),
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                verbose=args.verbose,
                                analog=manifest_module.analog,
                            )
                        elif t.get("and_flag"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                and_flag=t.get("and_flag"),
                                analog=manifest_module.analog,
                            )
                        elif t.get("chain"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                chain=t.get("chain"),
                                analog=manifest_module.analog,
                            )
                        elif t.get("fpga_io"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                fpga_io=t.get("fpga_io"),
                                analog=manifest_module.analog,
                            )
                        elif t.get("alu"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                alu=t.get("alu"),
                                analog=manifest_module.analog,
                            )
                        elif t.get("sec_count"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                sec_count=t.get("sec_count"),
                                analog=manifest_module.analog,
                            )
                        elif t.get("fpga_ram"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                fpga_ram=t.get("fpga_ram"),
                                analog=manifest_module.analog,
                            )
                        elif t.get("ana"):
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                ana=t.get("ana"),
                                analog=manifest_module.analog,
                            )
                        else:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                verbose=args.verbose,
                                analog=manifest_module.analog,
                            )
                        counter += 1
                        test.close_devices()
                        time.sleep(1)

                        with open(os.devnull, "a") as f:
                            sys.stdout = f
                            devices = device.open_devices()
                            sys.stdout = sys.__stdout__

        if not test_flag:
            test.print_and_log(f"[red]ERROR : couldn't find test {args.test}")

        test.print_and_log(
            "=============================================================================="
        )
        test.print_and_log("  All Tests Complete")
        test.print_and_log(
            "=============================================================================="
        )
        test.close_devices()
        # Load CSV data
        with open(f"{test.date_dir}/results.csv") as f:
            reader = csv.reader(f)
            headers = next(reader)

            table = Table(title="Regression Results")

            for header in headers:
                table.add_column(header)

            for row in reader:
                table.add_row(*row)

            test.print_and_log(table)

        reformat_csv(test, args.temperature)
        test.progress.stop()
        os._exit(0)
    except KeyboardInterrupt:
        test.gpio_mgmt.set_state(True)
        test.gpio_mgmt.set_value(1)
        hk_stop(True)
        time.sleep(0.1)
        test.print_and_log("Interrupted")
        test.progress.stop()
        try:
            test.close_devices()
            os._exit(1)
        except SystemExit:
            test.close_devices()
            os._exit(1)
