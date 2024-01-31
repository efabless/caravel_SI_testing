import argparse
import json
from caravel import Dio, FreqCounter, Test, accurate_delay, DATE_DIR
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
                test.console.print(f"Running test {test.test_name}...")
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
                    test.console.print("[red]failed")
                    status.append((test.test_name, False))
            if counter == 3:
                test.console.print("[green]passed")
                status.append((test.test_name, True))
            else:
                test.console.print("[red]failed")
                status.append((test.test_name, False))

        elif name == "uart_io":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.console.print(f"Running test {test.test_name}...")
                received = test.io_receive(4, 6)
                if not received:
                    test.console.print("[red]failed")
                    status.append((test.test_name, False))
                else:
                    if verbose:
                        test.console.print("IO[6] Passed")
                    pulse_count = test.receive_packet(250)
                    if pulse_count == 3:
                        if verbose:
                            test.console.print("Send 4 packets to IO[5]")
                        time.sleep(5)
                        test.send_pulse(4, 5, 5)
                        ack_pulse = test.receive_packet(250)
                        if ack_pulse == 9:
                            test.console.print("[red]failed")
                            status.append((test.test_name, False))
                        elif ack_pulse == 4:
                            test.console.print("[green]passed")
                            status.append((test.test_name, True))

        else:
            phase = 0
            test.console.print(f"Running test {test.test_name}...")
            for passing in test.passing_criteria:
                pulse_count = test.receive_packet(25)
                if pulse_count == passing:
                    if verbose:
                        test.console.print(f"pass phase {phase}")
                    phase = phase + 1

                if pulse_count == 9:
                    test.console.print("[red]failed")
                    status.append((test.test_name, False))

            if len(test.passing_criteria) == phase:
                test.console.print("[green]passed")
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
                test.console.print(f"Start test: {name}")

        if test.test_name == "uart":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.console.print(f"Running test {test.test_name}...")
            uart_data = uart.read_data(test)
            uart_data = uart_data.decode()
            if "UART Timeout!" in uart_data:
                test.console.print("[red]UART Timeout!")
                status.append((test.test_name, False))
            if "Monitor: Test UART passed" in uart_data:
                test.console.print("[green]passed")
                status.append((test.test_name, True))
            else:
                test.console.print("[red]failed")
                status.append((test.test_name, False))
            pulse_count = test.receive_packet(250)
            if pulse_count == 5:
                if verbose:
                    test.console.print("end UART transmission")

        elif test.test_name == "uart_reception":
            passed = True
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.console.print(f"Running test {test.test_name}...")
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
                        test.console.print(f"Received {i} successfully")
                if pulse_count == 9:
                    test.console.print("[red]failed")
                    uart.close()
                    passed = False
                    status.append((test.test_name, False))
                    break
                if time.time() > timeout:
                    test.console.print("[red]UART Timeout!")
                    uart.close()
                    passed = False
                    status.append((test.test_name, False))
                    break
            if passed:
                test.console.print("[green]passed")
                status.append((test.test_name, True))

        elif test.test_name == "uart_loopback":
            passed = True
            uart.open()
            timeout = time.time() + 50
            test.console.print(f"Running test {test.test_name}...")
            for i in range(0, 5):
                while time.time() < timeout:
                    uart_data, count = uart.read_uart()
                    if uart_data:
                        uart_data[count.value] = 0
                        dat = uart_data.value.decode()
                        # if dat in test.passing_criteria:
                        uart.write(dat)
                        pulse_count = test.receive_packet(250)
                        if pulse_count == 6:
                            passed = True
                            if verbose:
                                test.console.print(f"sent {dat} successfully")
                            break
                        if pulse_count == 9:
                            test.console.print("[red]failed")
                            uart.close()
                            status.append((test.test_name, False))
                            break
            if passed:
                test.console.print("[green]passed")
                status.append((test.test_name, True))

        elif test.test_name == "IRQ_uart_rx":
            pulse_count = test.receive_packet(25)
            if pulse_count == 2:
                test.console.print(f"Running test {test.test_name}...")
            uart.open()
            uart.write("I")
            pulse_count = test.receive_packet(25)
            if pulse_count == 5:
                test.console.print("[green]passed")
                status.append((test.test_name, True))
                break
            if pulse_count == 9:
                test.console.print("[red]failed")
                uart.close()
                status.append((test.test_name, False))

    return status


def process_soc(test, uart):
    status = []
    while True:
        uart_data = uart.read_data(test)
        uart_data = uart_data.decode()
        if "UART Timeout!" in uart_data:
            test.console.print("[red]UART Timeout!")
            status.append((test.test_name, False))
            break
        if "Start Test:" in uart_data:
            test.test_name = uart_data.strip().split(": ")[1]
            test.console.print(f"Running test {test.test_name}...")
        elif "End Test" in uart_data:
            test.console.print("End Test")
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
        uart_data = uart_data.decode()
        if "UART Timeout!" in uart_data:
            test.console.print("[red]UART Timeout!")
            status.append((test.test_name, False))
            break
        if "passed" in uart_data:
            test.console.print("[green]passed")
            status.append((test.test_name, True))
        elif "failed" in uart_data:
            test.console.print("[red]failed")
            status.append((test.test_name, False))
    return status


# def process_clock(test, device):
#     fc = FreqCounter(device)
#     pulse_count = test.receive_packet(25)
#     if pulse_count == 2:
#         test.console.print("start test")
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
#             test.console.print("Channel 14: Measured frequency: %.2f MHz" % (frq_MHz_1))
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
#             test.console.print("Channel 15: Measured frequency: %.2f MHz" % (frq_MHz_2))
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
#             test.console.print("start test")
#         if pulse_count == 5:
#             test.console.print(f"passed mem size {mem_size}")
#             mem_size = mem_size + 1
#         if pulse_count == 3:
#             if phase > 1:
#                 test.console.print("Test finished")
#                 return True
#             else:
#                 phase = phase + 1
#                 test.console.print("end test")

#         if pulse_count == 9:
#             test.console.print(
#                 f"[red]{test.test_name} test failed with {test.voltage}v supply, mem size {mem_size}"
#             )
#             return mem_size


def hk_stop(close):
    global pid
    if not close:
        # test.console.print("running caravel_hkstop.py...")
        p = subprocess.Popen(
            ["python3", "caravel_board/firmware_vex/util/caravel_hkstop.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        pid = p.pid
        # test.console.print("subprocess pid:", pid)
    elif pid:
        # test.console.print("stopping caravel_hkstop.py...")
        os.kill(pid, signal.SIGTERM)
        pid = None


def process_io(test, uart, verbose):
    hk_stop(False)
    fail = []
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(1)
    time.sleep(5)
    test.reset()
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode()
    if "UART Timeout!" in uart_data:
        test.console.print("[red]UART Timeout!")
        return False, None
    if "Start Test:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.console.print(f"Running test {test.test_name}...")
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
                        test.console.print(f"IO[{channel}]")
                    timeout = time.time() + 5
                    state = "LOW"
                    while 1:
                        uart_data = uart.read_data(test)
                        if b"UART Timeout!" in uart_data:
                            test.console.print("[red]UART Timeout!")
                            fail.append(channel)
                            break
                        # uart_data = uart_data.decode()
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
                                test.console.print(f"[green]IO[{channel}] Passed")
                            break
                        if time.time() > timeout:
                            test.console.print(
                                f"[red]Timeout failure on IO[{channel}]!"
                            )
                            fail.append(channel)
                            break
            elif test.test_name == "gpio_i" or test.test_name == "bitbang_i":
                if verbose:
                    test.console.print(f"IO[{channel}]")
                test.send_pulse(4, channel, 1)
                uart_data = uart.read_data(test)
                if b"UART Timeout!" in uart_data:
                    test.console.print("[red]UART Timeout!")
                    fail.append(channel)
                if b"p" in uart_data:
                    if verbose:
                        test.console.print(f"[green]IO[{channel}] Passed")
                elif b"f" in uart_data:
                    test.console.print(f"[red]IO[{channel}] Failed")
                    fail.append(channel)

    if len(fail) == 0:
        test.console.print("[green]passed")
        return True, None
    else:
        test.console.print("[red]failed")
        return False, fail


def process_io_plud(test, uart):
    p1_rt = False
    p2_rt = False
    pulse_count = test.receive_packet(25)
    if pulse_count == 2:
        test.console.print(f"Running test {test.test_name}...")
    # uart_data = uart.read_data(test)
    # uart_data = uart_data.decode()
    # if "Start Test:" in uart_data:
    #     test.test_name = uart_data.strip().split(": ")[1]
    #     test.console.print(f"Running test {test.test_name}...")
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
    if p1_rt and p2_rt:
        test.console.print("[green]passed")
        return True
    else:
        test.console.print("[red]failed")
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
                time.sleep(10)
                flag = True
            io_state = io.get_value()
            if io_state == default_val_n:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.console.print(f"[red]channel {channel-19} FAILED!")
        else:
            if not flag:
                time.sleep(10)
                flag = True
            io_state = io.get_value()
            if io_state == default_val:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.console.print(f"[red]channel {channel-19} FAILED!")
    hk_stop(True)
    if test_counter == 19:
        # test.console.print(
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
                time.sleep(10)
                flag = True
            io_state = io.get_value()
            if io_state == default_val_n:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.console.print(f"[red]channel {channel+19} FAILED!")
        else:
            if not flag:
                time.sleep(10)
                flag = True
            io_state = io.get_value()
            if io_state == default_val:
                test_counter += 1
            elif analog and channel > 13 and channel < 25:
                test_counter += 1
            else:
                test.console.print(f"[red]channel {channel+19} FAILED!")
    hk_stop(True)
    if test_counter == 19:
        # test.console.print(
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
#             test.console.print(f"pass phase {phase}")
#             if phase == 0:
#                 channel = test.device1v8.dio_map[channel]
#                 channel.set_state(True)
#                 channel.set_value(1)
#             phase = phase + 1
#         if pulse_count == 9:
#             test.console.print(f"[red]{test.test_name} test failed with {test.voltage}v supply!")
#             return False

#     if len(test.passing_criteria) == phase:
#         test.console.print(f"[green]{test.test_name} test Passed with {test.voltage}v supply!")
#         return True


def config_fpga(test):
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
    test.console.print("Programming FPGA...")
    prog_rst.set_value(1)
    time.sleep(1)
    for i in binary_array:
        ccff_head.set_value(i)
        prog_clk.set_value(1)
        accurate_delay(0.1)
        prog_clk.set_value(0)
        accurate_delay(0.1)
    prog_clk.set_value(0)


def load_bitstream(bitstream):
    file_path = f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/blizzard/bit_streams/{bitstream}.bit"
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
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode()
    if "UART Timeout!" in uart_data:
        test.console.print("[red]UART Timeout!")
        return False
    if "Start Test:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.console.print(f"Running test {test.test_name}...")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    binary_array = load_bitstream("and_3")
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    tail_value = []
    test.console.print("Reading data from chain tail")
    time.sleep(1)
    for i in binary_array:
        chain_value = ccff_tail.get_value()
        if chain_value:
            chain_value = 1
        else:
            chain_value = 0
        tail_value.append(chain_value)
        prog_clk.set_value(1)
        accurate_delay(0.5)
        prog_clk.set_value(0)
        accurate_delay(0.5)

    if tail_value == binary_array:
        test.console.print("[green]Chain test passed")
        return True
    else:
        with open(f"bin_arr_and3.json", "w") as file:
            # Dump the array into the file using json.dump
            json.dump(binary_array, file)
        with open(f"tail_arr_and3.json", "w") as file:
            # Dump the array into the file using json.dump
            json.dump(tail_value, file)
        test.console.print("[red]Chain test failed")
        return False


def ALU_4bits(operand_A_bits, operand_B_bits, operation_bits, operand_a, operand_b):
    for i in range(4):
        bit_A = operand_A_bits[i]
        test.device1v8.dio_map[operand_a[i]].set_value(bit_A)
        time.sleep(1)
        bit_B = operand_B_bits[i]
        test.device1v8.dio_map[operand_b[i]].set_value(bit_B)
        time.sleep(1)


def config_alu(test, arr, dir):
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
    operand_a = [4, 3, 2, 0]
    operand_b = [8, 7, 6, 5]
    result = [30, 28, 26, 24]
    operator = [13, 12]
    operand_a_bits = [[0, 1, 1, 1]]  # Example operand A values
    operand_b_bits = [[0, 1, 0, 0]]  # Example operand B values
    operations = [[0, 0], [0, 1], [1, 0], [1, 1]]  # Example operations
    result_bits = [[1, 0, 1, 1], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 1, 1]]
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode()
    if "UART Timeout!" in uart_data:
        test.console.print("[red]UART Timeout!")
        return False
    if "Start Test:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.console.print(f"Running test {test.test_name}...")
    hk_stop(False)
    binary_array = load_bitstream("ALU_4bits")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    time.sleep(1)
    clk_sel.set_value(1)
    time.sleep(20)
    op_rst.set_value(1)
    time.sleep(20)
    config_alu(test, operand_a, True)
    config_alu(test, operand_b, True)
    config_alu(test, operator, True)
    config_alu(test, result, False)
    time.sleep(1)
    alu_res = []

    for operation in operations:
        for i in range(len(operand_a_bits)):
            for j in range(len(operation)):
                test.device1v8.dio_map[operator[j]].set_value(operation[j])
            time.sleep(1)
            ALU_4bits(
                operand_a_bits[i], operand_b_bits[i], operation, operand_a, operand_b
            )
            time.sleep(1)
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
        test.console.print("[green]ALU test passed")
        return True
    else:
        test.console.print("[red]ALU test failed")
        test.console.print(f"alu_res = {alu_res}")
        test.console.print(f"result_bits = {result_bits}")
        return False


def fpga_counter_test(test, uart):
    # uart_data = uart.read_data(test)
    # uart_data = uart_data.decode()
    # if "UART Timeout!" in uart_data:
    #     test.console.print("[red]UART Timeout!")
    #     return False
    # if "Start Test:" in uart_data:
    #     test.test_name = uart_data.strip().split(": ")[1]
    #     test.console.print(f"Running test {test.test_name}...")
    hk_stop(False)
    out_io = [3, 4, 5, 6, 7, 26, 28, 24]
    binary_array = load_bitstream("seconds_decoder_2")
    # pulse_count = test.receive_packet(250)
    # if pulse_count == 2:
    #     test.console.print("start test")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    for channel in out_io:
        if channel < 14:
            io = test.device1v8.dio_map[channel]
            io.set_state(False)
        else:
            io = test.device3v3.dio_map[channel]
            io.set_state(False)

    time.sleep(1)
    clk_sel.set_value(1)
    time.sleep(1)
    op_rst.set_value(1)
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
            print(result)
            print(io_arr)
            io_arr = []
            if result:
                count += 1
        io = []
        if count >= 3:
            test.console.print(f"[green]{test.test_name} passed")
            return True
        elif time.time() > timeout:
            test.console.print(f"[red]Error: {test.test_name} failed")
            return False


def fpga_io_test(test, uart, verbose):
    # uart_data = uart.read_data(test)
    # uart_data = uart_data.decode()
    # if "UART Timeout!" in uart_data:
    #     test.console.print("[red]UART Timeout!")
    #     return False
    # if "Start Test:" in uart_data:
    #     test.test_name = uart_data.strip().split(": ")[1]
    #     test.console.print(f"Running test {test.test_name}...")
    hk_stop(False)
    if test.test_name == "inv_1":
        out = [17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 30, 31, 32]
        inp = [0, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 15, 16]
        binary_array = load_bitstream("inv_1")
    elif test.test_name == "inv_2":
        inp = [18, 19, 20, 21, 24, 25, 26, 27, 28, 30, 31, 32, 33]
        out = [0, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 15, 16]
        binary_array = load_bitstream("inv_2")
    elif test.test_name == "inv_3":
        inp = [2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 15, 16, 17]
        out = [18, 19, 20, 21, 24, 25, 26, 27, 28, 30, 31, 32, 33]
        binary_array = load_bitstream("inv_3")
    prog_clk, prog_rst, io_isol_n, op_rst, ccff_head, ccff_tail, clk_sel = config_fpga(
        test
    )
    program_fpga(test, prog_clk, prog_rst, ccff_head, binary_array)
    io_isol_n.set_value(1)
    ccff_head.set_value(0)
    time.sleep(1)
    clk_sel.set_value(1)
    time.sleep(20)
    op_rst.set_value(1)
    time.sleep(20)
    fail = False
    count = 0
    for inp_ut in inp:
        if verbose:
            test.console.print(f"now testing {inp_ut} only {out[count]} should toggle")
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
        time.sleep(5)
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
                test.console.print(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            elif io_val and out[count] == channel:
                test.console.print(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            else:
                if verbose:
                    test.console.print(f"[green]io {channel} = {io_val}")

        time.sleep(5)
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

        time.sleep(5)
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
                test.console.print(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            elif not io_val and out[count] == channel:
                test.console.print(f"[red]ERROR: io {channel} = {io_val}")
                fail = True
            else:
                if verbose:
                    test.console.print(f"[green]io {channel} = {io_val}")
        count += 1

    if fail:
        hk_stop(True)
        return False
    else:
        hk_stop(True)
        return True


def and_test(test, uart):
    uart_data = uart.read_data(test)
    uart_data = uart_data.decode()
    if "UART Timeout!" in uart_data:
        test.console.print("[red]UART Timeout!")
        return False
    if "Start Test:" in uart_data:
        test.test_name = uart_data.strip().split(": ")[1]
        test.console.print(f"Running test {test.test_name}...")
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
    time.sleep(1)
    clk_sel.set_value(1)
    time.sleep(20)
    op_rst.set_value(1)
    time.sleep(20)
    a.set_value(0)
    b.set_value(0)
    time.sleep(10)
    c_val = c.get_value()
    if c_val:
        test.console.print(f"[red] a = 0, b = 0, c = {c_val}")
        return False
    a.set_value(0)
    b.set_value(1)
    time.sleep(10)
    c_val = c.get_value()
    if c_val:
        test.console.print(f"[red] a = 0, b = 1, c = {c_val}")
        return False
    a.set_value(1)
    b.set_value(0)
    time.sleep(10)
    c_val = c.get_value()
    if c_val:
        test.console.print(f"[red] a = 1, b = 0, c = {c_val}")
        return False
    a.set_value(1)
    b.set_value(1)
    time.sleep(10)
    c_val = c.get_value()
    if not c_val:
        test.console.print(f"[red] a = 1, b = 1, c = {c_val}")
        return False
    test.console.print("[green]fpga AND test passed")
    return True


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
    and_flag,
    chain,
    fpga_io,
    alu,
    sec_count,
):
    if flash_only:
        run_only = False
    else:
        run_only = True
    test.reset_devices()
    if flash_flag or flash_only:
        test.console.print(
            "=============================================================================="
        )
        test.console.print(
            f"  Flashing :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}"
        )
        test.console.print(
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
        test.gpio_mgmt.set_value(0)
        time.sleep(5)
        test.flash(hex_file)
        test.gpio_mgmt.set_state(True)
        test.gpio_mgmt.set_value(1)
        time.sleep(5)
        # test.power_down()
        # test.release_reset()
    else:
        test.power_down()
        time.sleep(5)
    test.power_up()
    test.device1v8.supply.set_voltage(test.l_voltage)
    test.device3v3.supply.set_voltage(test.h_voltage)
    test.reset()

    test.console.print(
        "=============================================================================="
    )
    test.console.print(
        f"  Running  :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}"
    )
    test.console.print(
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
        elif and_flag:
            results = and_test(test, uart_data)
        elif chain:
            results = chain_test(test, uart_data)
        elif fpga_io:
            results = fpga_io_test(test, uart_data, verbose)
        elif alu:
            results = fpga_ALU_test(test, uart_data)
        elif sec_count:
            results = fpga_counter_test(test, uart_data)
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
        #         test.console.print(f"ERROR : No {mode} mode")
        #         exit(1)
        # elif spi_flag:
        #     results = process_spi(test, spi)
        # elif external:
        #     results = process_external(test)
        # elif clock:
        #     results = process_clock(test, la_device)
        # else:
        #     results = process_data(test)

        # test.console.print("==============================================================================")
        # test.console.print(f"  Completed:  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
        # test.console.print("==============================================================================")
        return results
    else:
        return True


def reformat_csv(temp=None):
    # Read the original CSV file
    with open(f"{DATE_DIR}/results.csv", "r") as file:
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
    with open(f"{DATE_DIR}/formatted_results.csv", "w", newline="") as file:
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
    and_flag=False,
    chain=False,
    fpga_io=False,
    alu=False,
    sec_count=False,
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
        and_flag,
        chain,
        fpga_io,
        alu,
        sec_count,
    )
    test.gpio_mgmt.set_state(True)
    test.gpio_mgmt.set_value(0)
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
                    [result[0], test.l_voltage, test.h_voltage, "passed", end_time]
                )
            else:
                arr.append(
                    [result[0], test.l_voltage, test.h_voltage, "failed", end_time]
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

    with open(f"{DATE_DIR}/results.csv", "a", encoding="UTF8") as f:
        writer = csv.writer(f)
        for test in arr:
            writer.writerow(test)


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
            "-tmp",
            "--temperature",
            help="Temperature monitoring",
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

        test.console.print(
            "=============================================================================="
        )
        if analog:
            test.console.print("  Beginning Tests for analog project")
        else:
            test.console.print("  Beginning Tests for digital project")
        test.console.print(
            "=============================================================================="
        )

        csv_header = [
            "Test_name",
            "Low Voltage (v)",
            "High Voltage (v)",
            "Pass/Fail",
            "Time (s)",
        ]

        with open(f"{DATE_DIR}/results.csv", "a", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
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
                        elif t["and_flag"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                plud=t["plud"],
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                and_flag=t["and_flag"],
                            )
                        elif t["chain"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                plud=t["plud"],
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                chain=t["chain"],
                            )
                        elif t["fpga_io"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                plud=t["plud"],
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                fpga_io=t["fpga_io"],
                                verbose=args.verbose,
                            )
                        elif t["alu"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                plud=t["plud"],
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                alu=t["alu"],
                            )
                        elif t["sec_count"]:
                            exec_test(
                                test,
                                start_time,
                                t["hex_file_path"],
                                flash_flag,
                                plud=t["plud"],
                                flash_only=args.flash_only,
                                uart_data=uart_data,
                                sec_count=t["sec_count"],
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
                        time.sleep(5)

                        with open(os.devnull, "a") as f:
                            sys.stdout = f
                            devices = device.open_devices()
                            sys.stdout = sys.__stdout__

            if not test_flag:
                test.console.print(f"[red]ERROR : Coun't find test {args.test}")

        test.console.print(
            "=============================================================================="
        )
        test.console.print("  All Tests Complete")
        test.console.print(
            "=============================================================================="
        )
        test.close_devices()
        # Load CSV data
        with open(f"{DATE_DIR}/results.csv") as f:
            reader = csv.reader(f)
            headers = next(reader)

            table = Table(title="Regression Results")

            for header in headers:
                table.add_column(header)

            for row in reader:
                table.add_row(*row)

            test.console.print(table)

        reformat_csv(args.temperature)
        test.progress.stop()
        os._exit(0)
    except KeyboardInterrupt:
        test.console.print("Interrupted")
        test.progress.stop()
        try:
            test.close_devices()
            os._exit(1)
        except SystemExit:
            test.close_devices()
            os._exit(1)
