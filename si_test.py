import argparse
import json
from caravel import Dio, FreqCounter, Test, accurate_delay
from io_config import Device, device, connect_devices, UART, SPI
import os
import csv
import time
import datetime
import subprocess
import signal
import sys
from rich.table import Table
from manifest import (
    TestDict,
    device1_sn,
    device2_sn,
    device3_sn,
    l_voltage,
    h_voltage,
    analog,
)
from WF_SDK import logic, wavegen, static, scope
import matplotlib.pyplot as plt
import numpy as np


def init_ad_ios(device1_data, device2_data, device3_data):
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
    test_names = ["send_packet", "receive_packet", "uart_io"]
    status = []
    counter = 0
    for name in test_names:
        test.test_name = name
        if test.test_name == "receive_packet":
            io = test.device1v8.dio_map[0]
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
            for i in range(5, 8):
                while not io.get_value():
                    pass
                test.send_packet(i, 25)
                while io.get_value():
                    pass
                pulse_count = test.receive_packet(250)
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
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
                received = test.io_receive(4, 6)
                if not received:
                    test.print_and_log("[red]failed")
                    status.append((test.test_name, False))
                else:
                    if verbose:
                        test.print_and_log("IO[6] Passed")
                    pulse_count = test.receive_packet(250)
                    if pulse_count == 3:
                        if verbose:
                            test.print_and_log("Send 4 packets to IO[5]")
                        time.sleep(5)
                        test.send_pulse(4, 5, 5)
                        ack_pulse = test.receive_packet(250)
                        if ack_pulse == 9:
                            test.print_and_log("[red]failed")
                            status.append((test.test_name, False))
                        elif ack_pulse == 4:
                            test.print_and_log("[green]passed")
                            status.append((test.test_name, True))

        else:
            phase = 0
            test.print_and_log(f"Running test {test.test_name}...")
            for passing in test.passing_criteria:
                pulse_count = test.receive_packet(25)
                if pulse_count == passing:
                    if verbose:
                        test.print_and_log(f"pass phase {phase}")
                    phase = phase + 1

                if pulse_count == 9:
                    test.print_and_log("[red]failed")
                    status.append((test.test_name, False))

            if len(test.passing_criteria) == phase:
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
        pulse_count = test.receive_packet(250)
        if pulse_count == 1:
            if verbose:
                test.print_and_log(f"Start Test: {name}")

        if test.test_name == "uart":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
            uart_data = uart.read_data(test)
            uart_data = uart_data.decode('utf-8', 'ignore')
            if "UART Timeout!" in uart_data:
                test.print_and_log("[red]UART Timeout!")
                status.append((test.test_name, False))
            if "Monitor: Test UART passed" in uart_data:
                test.print_and_log("[green]passed")
                status.append((test.test_name, True))
            else:
                test.print_and_log("[red]failed")
                status.append((test.test_name, False))
            pulse_count = test.receive_packet(250)
            if pulse_count == 5:
                if verbose:
                    test.print_and_log("end UART transmission")

        elif test.test_name == "uart_reception":
            passed = True
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.print_and_log(f"Running test {test.test_name}...")
            uart.open()
            timeout = time.time() + 50
            for i in ["M", "B", "A"]:
                pulse_count = test.receive_packet(250)
                if pulse_count == 4:
                    uart.write(i)
                pulse_count = test.receive_packet(250)
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
                        dat = uart_data.value.decode('utf-8', 'ignore')
                        # if dat in test.passing_criteria:
                        uart.write(dat)
                        pulse_count = test.receive_packet(250)
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
    status = []
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    while True:
        uart_data = uart.read_data(test)
        uart_data = uart_data.decode('utf-8', 'ignore')
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
        uart_data = uart_data.decode('utf-8', 'ignore')
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


# def process_clock(test, device):
#     fc = FreqCounter(device)
#     pulse_count = test.receive_packet(25)
#     if pulse_count == 2:
#         test.print_and_log("sT")
#     fc.open()
#     time.sleep(5)
#     data, data_time = fc.record(1)
#     counter = 0
#     state = 0
#     for i in range(len(data)):
#         if data[i] <= 0 and state == 1:
#             state = 0
#         if data[i] >= 2 and state == 0:
#             one_time = data_time[i]
#             state = 1
#             counter += 1
#         if counter == 2:
#             freq = 1 / one_time
#             frq_MHz_1 = freq / 1000000
#             test.print_and_log("Channel 14: Measured frequency: %.2f MHz" % (frq_MHz_1))
#             break

#     data, data_time = fc.record(2)
#     counter = 0
#     state = 0
#     for i in range(len(data)):
#         if data[i] <= 0 and state == 1:
#             state = 0
#         if data[i] >= 2 and state == 0:
#             one_time = data_time[i]
#             state = 1
#             counter += 1
#         if counter == 2:
#             freq = 1 / one_time
#             frq_MHz_2 = freq / 1000000
#             test.print_and_log("Channel 15: Measured frequency: %.2f MHz" % (frq_MHz_2))
#             break
#     if frq_MHz_1 > 5 or frq_MHz_2 > 5:
#         return "IO[14]:%.2f MHz, IO[15]:%.2f MHz" % (frq_MHz_1, frq_MHz_2)
#     else:
#         return False


# def process_mem(test):
#     phase = 0
#     mem_size = 0
#     while True:
#         pulse_count = test.receive_packet(25)
#         if pulse_count == 1:
#             test.print_and_log("sT")
#         if pulse_count == 5:
#             test.print_and_log(f"passed mem size {mem_size}")
#             mem_size = mem_size + 1
#         if pulse_count == 3:
#             if phase > 1:
#                 test.print_and_log("Test finished")
#                 return True
#             else:
#                 phase = phase + 1
#                 test.print_and_log("end test")

#         if pulse_count == 9:
#             test.print_and_log(
#                 f"[red]{test.test_name} test failed with {test.voltage}v supply, mem size {mem_size}"
#             )
#             return mem_size


def hk_stop(close):
    global pid
    if not close:
        # test.print_and_log("running caravel_hkstop.py...")
        p = subprocess.Popen(
            ["python3", "caravel_board/firmware_vex/util/caravel_hkstop.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        pid = p.pid
        # test.print_and_log("subprocess pid:", pid)
    elif pid:
        # test.print_and_log("stopping caravel_hkstop.py...")
        os.kill(pid, signal.SIGTERM)
        pid = None


def process_io(test, uart, verbose):
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    hk_stop(False)
    fail = []
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode('utf-8', 'ignore')
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


def process_io_plud(test, uart):
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
    p1_rt = False
    p2_rt = False
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode('utf-8', 'ignore')
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
        p1_rt = run_io_plud(default_val, default_val_n, False)
        p2_rt = run_io_plud(default_val, default_val_n, True)
    elif test.test_name == "gpio_lpd_ho":
        default_val = 0
        default_val_n = 1
        p1_rt = run_io_plud(default_val, default_val_n, False)
        p2_rt = run_io_plud(default_val, default_val_n, True)
    elif test.test_name == "gpio_lo_hpu":
        default_val = 1
        default_val_n = 0
        p1_rt = run_io_plud_h(default_val, default_val_n, False)
        p2_rt = run_io_plud_h(default_val, default_val_n, True)
    elif test.test_name == "gpio_lo_hpd":
        default_val = 0
        default_val_n = 1
        p1_rt = run_io_plud_h(default_val, default_val_n, False)
        p2_rt = run_io_plud_h(default_val, default_val_n, True)
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(1)
    if p1_rt and p2_rt:
        test.print_and_log("[green]passed")
        return True
    else:
        test.print_and_log("[red]failed")
        return False


def run_io_plud(default_val, default_val_n, first_itter):
    test_counter = 0
    flag = False
    hk_stop(False)
    for channel in range(0, 38):
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
    if test_counter == 19:
        # test.print_and_log(
        #     f"[green]{test.test_name} test passed"
        # )
        return True
    else:
        return False


def run_io_plud_h(default_val, default_val_n, first_itter):
    test_counter = 0
    flag = False
    hk_stop(False)
    for channel in range(37, -1, -1):
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
    if test_counter == 19:
        # test.print_and_log(
        #     f"[green]{test.test_name} test Passed"
        # )
        return True
    else:
        return False


# def process_external(test):
#     if test.test_name == "IRQ_external":
#         channel = 7
#     elif test.test_name == "IRQ_external2":
#         channel = 12
#     phase = 0
#     for passing in test.passing_criteria:
#         pulse_count = test.receive_packet(25)
#         if pulse_count == passing:
#             test.print_and_log(f"pass phase {phase}")
#             if phase == 0:
#                 channel = test.device1v8.dio_map[channel]
#                 channel.set_state(True)
#                 channel.set_value(1)
#             phase = phase + 1
#         if pulse_count == 9:
#             test.print_and_log(f"[red]{test.test_name} test failed with {test.voltage}v supply!")
#             return False

#     if len(test.passing_criteria) == phase:
#         test.print_and_log(f"[green]{test.test_name} test Passed with {test.voltage}v supply!")
#         return True

def concat_csv(root_directory, file_name):
    # Initialize a flag to track whether the header has been written
    header_written = False

    # Open the output file in write mode
    with open(f'{root_directory}/concatenated_{file_name}.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Traverse the directory tree
        for dirpath, dirnames, filenames in os.walk(root_directory):
            # Loop through each file
            for filename in filenames:
                if filename == f"{file_name}.csv":
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, 'r', newline='') as infile:
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
):
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
        test.power_down()
        test.apply_reset()
        test.power_up_1v8()
        st = time.time()
        test.flash(hex_file)
        test.print_and_log(f"flash took {time.time() - st} seconds")
        test.power_down()
        test.release_reset()
    else:
        test.power_down()
        time.sleep(5)
    test.power_up()
    test.device1v8.supply.set_voltage(test.l_voltage)
    test.device3v3.supply.set_voltage(test.h_voltage)
    test.reset()

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
            results = process_io(test, uart_data, verbose)
        elif plud:
            results = process_io_plud(test, uart_data)
        else:
            results = process_soc(test, uart_data)
        # if uart:
        #     results = process_uart(test, uart_data)
        # elif mem:
        #     results = process_mem(test)
        # elif io:
        #     if mode == "output":
        #         results = process_io(test, io)
        #     elif mode == "input":
        #         results = process_input_io(test, io)
        #     elif mode == "plud":
        #         results = process_io_plud(test)
        #     else:
        #         test.print_and_log(f"ERROR : No {mode} mode")
        #         exit(1)
        # elif spi_flag:
        #     results = process_spi(test, spi)
        # elif external:
        #     results = process_external(test)
        # elif clock:
        #     results = process_clock(test, la_device)
        # else:
        #     results = process_data(test)

        # test.print_and_log("==============================================================================")
        # test.print_and_log(f"  Completed:  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
        # test.print_and_log("==============================================================================")

        return results
    else:
        return True


def reformat_csv(test, temp=None):
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
):
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
    )
    end_time = time.time() - start_time
    arr = []

    if type(results) == bool:
        if results:
            arr.append(
                [test.test_name, test.l_voltage, test.h_voltage, "passed", end_time]
            )
        else:
            arr.append(
                [test.test_name, test.l_voltage, test.h_voltage, "failed", end_time]
            )
    elif type(results) == tuple:
        if type(results[0]) == bool:
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
    elif type(results) == list:
        for result in results:
            if result[1]:
                arr.append(
                    [result[0], test.l_voltage, test.h_voltage, "passed", end_time / len(results)]
                )
            else:
                arr.append(
                    [result[0], test.l_voltage, test.h_voltage, "failed", end_time / len(results)]
                )
    elif type(results) == str:
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
    # Get the last test.date_dir
    date_dirs = sorted([d for d in os.listdir(test.runs_dir) if os.path.isdir(os.path.join(test.runs_dir, d))])
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
        args = parser.parse_args()
        # open multiple devices
        devices = device.open_devices()
        # connect devices using hardcoded serial numbers
        d1_sn = bytes(device1_sn, "utf-8")
        d2_sn = bytes(device2_sn, "utf-8")
        d3_sn = bytes(device3_sn, "utf-8")
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
            start_index = next((i for i, test in enumerate(TestDict) if test["test_name"] == last_test_name), None)

            if start_index is not None:
                # Create a new TestDict list starting from the specified test
                TestDict = TestDict[start_index:]
            test.date_dir = f"{test.runs_dir}/{last_date_dir}"
        else:
            test.make_runs_dirs()
            with open(f"{test.date_dir}/results.csv", "a", encoding="UTF8") as f:
                writer = csv.writer(f)
                writer.writerow(csv_header)

        test.print_and_log(
            "=============================================================================="
        )
        if analog:
            test.print_and_log("  Beginning Tests for analog project")
        else:
            test.print_and_log("  Beginning Tests for digital project")
        test.print_and_log(
            "=============================================================================="
        )

        test_flag = False

        test.task = test.progress.add_task(
            "SI validation", total=(len(TestDict) * len(l_voltage) * len(h_voltage))
        )
        test.progress.start()
        for t in TestDict:
            if not args.test or args.test == t["test_name"]:
                test.test_name = t["test_name"]
                test.passing_criteria = t["passing_criteria"]
                flash_flag = True
                counter = 0
                test_flag = True
                for v in l_voltage:
                    for h in h_voltage:
                        start_time = time.time()
                        test.l_voltage = v
                        test.h_voltage = h
                        if counter > 0 or args.run_only:
                            flash_flag = False
                        if t["uart"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                uart=t["uart"],
                                uart_data=uart_data,
                                flash_only=args.flash_only,
                                verbose=args.verbose,
                            )
                        elif t["mgmt_gpio"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                mgmt_gpio=t["mgmt_gpio"],
                                flash_only=args.flash_only,
                                verbose=args.verbose,
                            )
                        elif t["io"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                io=t["io"],
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                verbose=args.verbose,
                            )
                        elif t["plud"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                plud=t["plud"],
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                verbose=args.verbose,
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
                            )
                        counter += 1
                        test.close_devices()
                        time.sleep(1)

                        with open(os.devnull, 'a') as f:
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
