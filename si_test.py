import argparse
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
from manifest import TestDict, device1_sn, device2_sn, device3_sn, voltage, analog


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


def process_mgmt_gpio(test):
    test_names = ["send_packet", "receive_packet", "uart_io"]
    for name in test_names:
        test.test_name = name
        if test.test_name == "receive_packet":
            io = test.device1v8.dio_map[0]
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.console.print("Test started")
            for i in range(5, 8):
                while not io.get_value():
                    pass
                test.send_packet(i, 25)
                while io.get_value():
                    pass
                pulse_count = test.receive_packet(250)
                if pulse_count == i:
                    test.console.print(f"sent {i} pulses successfully")
                else:
                    test.console.print(f"{test.test_name} test failed with {test.voltage}v supply!")
                    return False

        elif name == "uart_io":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                received = test.io_receive(4, 6)
                if received:
                    test.console.print("IO[6] Passed")
                else:
                    test.console.print("Timeout failure on IO[6]!")
                    return False
            pulse_count = test.receive_packet(250)
            if pulse_count == 3:
                test.console.print("Send 4 packets to IO[5]")
                time.sleep(5)
                test.send_pulse(4, 5, 5)
                ack_pulse = test.receive_packet(250)
                if ack_pulse == 9:
                    test.console.print("IO[5] Failed to send pulse")
                    return False
                elif ack_pulse == 4:
                    test.console.print("IO[5] sent pulse successfully")

        else:
            phase = 0
            for passing in test.passing_criteria:
                pulse_count = test.receive_packet(250)
                if pulse_count == passing:
                    test.console.print(f"pass phase {phase}")
                    phase = phase + 1

                if pulse_count == 9:
                    test.console.print(f"{test.test_name} test failed with {test.voltage}v supply!")
                    return False

            if len(test.passing_criteria) == phase:
                test.console.print(f"{test.test_name} test Passed with {test.voltage}v supply!")
    return True


def process_uart(test, uart):
    """Function to test all UART functionality
    First test: IO[5] as input to caravel and IO[6] as output from caravel
    Second test: UART as output from caravel
    Third test: UART as input to caravel
    Fourth test: UART loopback (tests both input and output)
    """

    test_names = ["uart", "uart_reception", "uart_loopback"]
    for name in test_names:
        test.test_name = name
        pulse_count = test.receive_packet(250)
        if pulse_count == 1:
            test.console.print(f"Start test: {name}")

        if test.test_name == "uart":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.console.print("Start UART transmission")
            uart_data = uart.read_data(test)
            uart_data = uart_data.decode()
            if "Monitor: Test UART passed" in uart_data:
                test.console.print("UART test passed")
            else:
                test.console.print("UART test failed")
                return False
            pulse_count = test.receive_packet(250)
            if pulse_count == 5:
                test.console.print("end UART transmission")

        elif test.test_name == "uart_reception":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                test.console.print("Start UART transmission")
            uart.open()
            timeout = time.time() + 50
            for i in ["M", "B", "A"]:
                pulse_count = test.receive_packet(250)
                if pulse_count == 4:
                    uart.write(i)
                pulse_count = test.receive_packet(250)
                if pulse_count == 6:
                    test.console.print(f"Successfully sent {i} over UART!")
                if pulse_count == 9:
                    test.console.print(f"Couldn't send {i} over UART!")
                    uart.close()
                    return False
                if time.time() > timeout:
                    test.console.print("UART Timeout!")
                    uart.close()
                    return False

        elif test.test_name == "uart_loopback":
            uart.open()
            timeout = time.time() + 50
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
                            test.console.print(f"Successfully sent {dat} over UART!")
                            break
                        if pulse_count == 9:
                            test.console.print(f"Couldn't send {dat} over UART!")
                            uart.close()
                            return False
    return True

def process_soc(test, uart):
    while True:
        uart_data = uart.read_data(test)
        uart_data = uart_data.decode()
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
        if "passed" in uart_data:
            test.console.print("[green]passed")
        elif "failed" in uart_data:
            test.console.print("[red]failed")
            return False
    return True


# def process_clock(test, device):
#     fc = FreqCounter(device)
#     pulse_count = test.receive_packet(250)
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
#         pulse_count = test.receive_packet(250)
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


# def hk_stop(close):
#     global pid
#     if not close:
#         test.console.print("running caravel_hkstop.py...")
#         p = subprocess.Popen(
#             ["python3", "caravel_board/firmware_vex/util/caravel_hkstop.py"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#         )
#         pid = p.pid
#         # test.console.print("subprocess pid:", pid)
#     elif pid:
#         test.console.print("stopping caravel_hkstop.py...")
#         os.kill(pid, signal.SIGTERM)
#         pid = None


# def process_io(test, io):
#     phase = 0
#     io_pulse = 0
#     if io == "low":
#         hk_stop(False)
#         rst = 0
#     if io == "high":
#         rst = 2
#     end_pulses = 0
#     while end_pulses < 2:
#         pulse_count = test.receive_packet(25)
#         if phase == 0 and pulse_count == 1:
#             test.console.print("Start test")
#             phase = phase + 1
#         elif phase > 0 and pulse_count == 1:
#             rst = rst + 1
#             end_pulses = end_pulses + 1
#         elif pulse_count > 1:
#             end_pulses = 0
#             if rst < 2:
#                 channel = (pulse_count - 2) + (9 * rst)
#             elif rst == 2:
#                 channel = 37 - (pulse_count - 2)
#             elif rst == 3:
#                 channel = 28 - (pulse_count - 2)
#             phase = phase + 1
#             if channel == 5:
#                 hk_stop(True)
#             if channel > 13 and channel < 22:
#                 io = test.deviced.dio_map[channel]
#             elif channel > 21:
#                 io = test.device3v3.dio_map[channel]
#             else:
#                 io = test.device1v8.dio_map[channel]
#             if analog and channel > 13 and channel < 25:
#                 pass
#             else:
#                 test.console.print(f"start sending pulses to gpio[{channel}]")
#                 state = "HI"
#                 timeout = time.time() + 20
#                 accurate_delay(12.5)
#                 while 1:
#                     accurate_delay(25)
#                     x = io.get_value()
#                     if state == "LOW":
#                         if x:
#                             state = "HI"
#                     elif state == "HI":
#                         if not x:
#                             state = "LOW"
#                             io_pulse = io_pulse + 1
#                     if io_pulse == 4:
#                         io_pulse = 0
#                         test.console.print(f"gpio[{channel}] Passed")
#                         break
#                     if time.time() > timeout:
#                         test.console.print(f"Timeout failure on gpio[{channel}]!")
#                         return False, channel
#     return True, None


# def process_io_plud(test):
#     p1_rt = False
#     p2_rt = False
#     pulse_count = test.receive_packet(250)

#     if pulse_count == 1:
#         test.console.print("Start test")
#     if test.test_name == "gpio_lpu_ho":
#         default_val = 1
#         default_val_n = 0
#         p1_rt = run_io_plud(default_val, default_val_n, False)
#         p2_rt = run_io_plud(default_val, default_val_n, True)
#     elif test.test_name == "gpio_lpd_ho":
#         default_val = 0
#         default_val_n = 1
#         p1_rt = run_io_plud(default_val, default_val_n, False)
#         p2_rt = run_io_plud(default_val, default_val_n, True)
#     elif test.test_name == "gpio_lo_hpu":
#         default_val = 1
#         default_val_n = 0
#         p1_rt = run_io_plud_h(default_val, default_val_n, False)
#         p2_rt = run_io_plud_h(default_val, default_val_n, True)
#     elif test.test_name == "gpio_lo_hpd":
#         default_val = 0
#         default_val_n = 1
#         p1_rt = run_io_plud_h(default_val, default_val_n, False)
#         p2_rt = run_io_plud_h(default_val, default_val_n, True)
#     if p1_rt and p2_rt:
#         return True
#     else:
#         return False


# def run_io_plud(default_val, default_val_n, first_itter):
#     test_counter = 0
#     flag = False
#     hk_stop(False)
#     for channel in range(0, 38):
#         if channel > 13 and channel < 22:
#             io = test.deviced.dio_map[channel]
#         elif channel > 21:
#             io = test.device3v3.dio_map[channel]
#         else:
#             io = test.device1v8.dio_map[channel]
#         if channel < 19 and first_itter:
#             io.set_state(True)
#             io.set_value(default_val_n)
#         elif channel < 19:
#             io.set_state(False)
#         elif first_itter:
#             if not flag:
#                 time.sleep(10)
#                 flag = True
#             io_state = io.get_value()
#             if io_state == default_val_n:
#                 test_counter += 1
#             elif analog and channel > 13 and channel < 25:
#                 test_counter += 1
#             else:
#                 test.console.print(f"[red]channel {channel} FAILED!")
#                 return False
#         else:
#             if not flag:
#                 time.sleep(10)
#                 flag = True
#             io_state = io.get_value()
#             if io_state == default_val:
#                 test_counter += 1
#             elif analog and channel > 13 and channel < 25:
#                 test_counter += 1
#             else:
#                 test.console.print(f"[red]channel {channel} FAILED!")
#                 return False
#     hk_stop(True)
#     if test_counter == 19:
#         test.console.print(
#             f"[green]{test.test_name} test passed"
#         )
#         return True
#     else:
#         return False


# def run_io_plud_h(default_val, default_val_n, first_itter):
#     test_counter = 0
#     flag = False
#     hk_stop(False)
#     for channel in range(37, -1, -1):
#         if channel > 13 and channel < 22:
#             io = test.deviced.dio_map[channel]
#         elif channel > 21:
#             io = test.device3v3.dio_map[channel]
#         else:
#             io = test.device1v8.dio_map[channel]
#         if channel > 18 and first_itter:
#             io.set_state(True)
#             io.set_value(default_val_n)
#         elif channel > 18:
#             io.set_state(False)
#         elif first_itter:
#             if not flag:
#                 time.sleep(10)
#                 flag = True
#             io_state = io.get_value()
#             if io_state == default_val_n:
#                 test_counter += 1
#             elif analog and channel > 13 and channel < 25:
#                 test_counter += 1
#             else:
#                 test.console.print(f"[red]channel {channel} FAILED!")
#                 return False
#         else:
#             if not flag:
#                 time.sleep(10)
#                 flag = True
#             io_state = io.get_value()
#             if io_state == default_val:
#                 test_counter += 1
#             elif analog and channel > 13 and channel < 25:
#                 test_counter += 1
#             else:
#                 test.console.print(f"[red]channel {channel} FAILED!")
#                 return False
#     test.console.print(test_counter)
#     hk_stop(True)
#     if test_counter == 19:
#         test.console.print(
#             f"[green]{test.test_name} test Passed"
#         )
#         return True
#     else:
#         return False


# def process_external(test):
#     if test.test_name == "IRQ_external":
#         channel = 7
#     elif test.test_name == "IRQ_external2":
#         channel = 12
#     phase = 0
#     for passing in test.passing_criteria:
#         pulse_count = test.receive_packet(250)
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


# def process_spi(test, spi):
#     spi.open()
#     test.console.print(spi.read(1))
#     # csb = spi.device_data.dio_map[spi.cs]

#     # while not csb.get_value():
#     #     pass

#     # test.console.print("CSB is high")

#     # spi.enabled()
#     # spi.rw_mode = "r"
#     # data1 = ""
#     # data2 = ""
#     # for i in range(0, 8):
#     #     spi.clk_trig()
#     #     data1 = data1 + str(spi.data[i])
#     # spi.data = []
#     # for i in range(0, 8):
#     #     spi.clk_trig()
#     #     data2 = data2 + str(spi.data[i])
#     # test.console.print(int(data1, 2))
#     # test.console.print(int(data2, 2))
#     return False


# def process_input_io(test, io):
#     count = 0
#     if io == "low":
#         hk_stop(False)
#         channel = 0
#     else:
#         channel = 37
#     while count < 19:
#         if analog and channel > 13 and channel < 25:
#             count = count + 1
#         else:
#             pulse_count = test.receive_packet(25)
#             if channel == 5:
#                 hk_stop(True)
#             if pulse_count == 1:
#                 test.console.print(f"Sending 4 pulses on gpio[{channel}]")
#                 test.send_pulse(4, channel, 5)
#                 ack_pulse = test.receive_packet(25)
#                 if ack_pulse == 5:
#                     test.console.print(f"[red]gpio[{channel}] Failed to send pulse")
#                     return False, channel
#                 elif ack_pulse == 3:
#                     test.console.print(f"[green]gpio[{channel}] sent pulse successfully")
#                 if io == "low":
#                     channel = channel + 1
#                 else:
#                     channel = channel - 1
#                 count = count + 1
#     return True, None


def flash_test(
    test, hex_file, flash_flag, uart, uart_data, mgmt_gpio, flash_only
):
    if flash_only:
        run_only = False
    else:
        run_only = True
    test.reset_devices()
    if flash_flag or flash_only:
        test.console.print("==============================================================================")
        test.console.print(f"  Flashing :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
        test.console.print("==============================================================================")

        test.progress.update(
            test.task,
            description=f"Flashing {test.test_name}",
        )
        test.power_down()
        test.apply_reset()
        test.power_up_1v8()
        test.flash(hex_file)
        test.power_down()
        test.release_reset()
    else:
        test.power_down()
        time.sleep(5)
    test.power_up()
    test.device1v8.supply.set_voltage(test.voltage)
    test.reset()

    test.console.print("==============================================================================")
    test.console.print(f"  Running  :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
    test.console.print("==============================================================================")

    results = None

    if run_only:
        test.progress.update(
            test.task,
            advance=1,
            description=f"Running {test.test_name} on {test.voltage}V",
            visible=True,
        )
        if uart:
            results = process_uart(test, uart_data)
        elif mgmt_gpio:
            results = process_mgmt_gpio(test)
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

        test.console.print("==============================================================================")
        test.console.print(f"  Completed:  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
        test.console.print("==============================================================================")

        return results
    else:
        return True


def exec_test(
    test,
    start_time,
    writer,
    hex_file,
    flash_flag=True,
    uart=False,
    uart_data=None,
    mgmt_gpio=False,
    flash_only=False,
):
    results = False
    results = flash_test(
        test,
        hex_file,
        flash_flag,
        uart,
        uart_data,
        mgmt_gpio,
        flash_only,
    )
    end_time = time.time() - start_time

    if type(results) == bool:
        if results:
            arr = [test.test_name, test.voltage, "passed", end_time]
        else:
            arr = [test.test_name, test.voltage, "failed", end_time]
    elif type(results) == tuple:
        if type(results[0]) == bool:
            if results[0]:
                arr = [test.test_name, test.voltage, "passed", end_time]
            else:
                arr = [test.test_name, test.voltage, f"failed, {results[1]}", end_time]
    elif type(results) == str:
        arr = [test.test_name, test.voltage, results, "%.2f" % (end_time)]

    writer.writerow(arr)


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
            "-t",
            "--test",
            help="Run Standalone test if in manifest",
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

        test.console.print("==============================================================================")
        if analog:
            test.console.print("  Beginning Tests for analog project")
        else:
            test.console.print("  Beginning Tests for digital project")
        test.console.print("==============================================================================")

        csv_header = ["Test_name", "Voltage (v)", "Pass/Fail", "Time (s)"]
        if os.path.exists("./results.csv"):
            os.remove("./results.csv")
        if os.path.exists("./flash.log"):
            os.remove("./flash.log")

        with open("results.csv", "a", encoding="UTF8") as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(csv_header)
            test_flag = False
            test.task = test.progress.add_task("SI validation", total=(len(TestDict) * len(voltage)))
            test.progress.start()
            for t in TestDict:
                if not args.test or args.test == t["test_name"]:
                    test.test_name = t["test_name"]
                    test.passing_criteria = t["passing_criteria"]
                    flash_flag = True
                    counter = 0
                    test_flag = True
                    for v in voltage:
                        start_time = time.time()
                        test.voltage = v
                        if counter > 0 or args.run_only:
                            flash_flag = False
                        if t["uart"]:
                            exec_test(
                                test,
                                start_time,
                                writer,
                                t["hex_file_path"],
                                flash_flag,
                                uart=t["uart"],
                                uart_data=uart_data,
                                flash_only=args.flash_only,
                            )
                        elif t["mgmt_gpio"]:
                            exec_test(
                                test,
                                start_time,
                                writer,
                                t["hex_file_path"],
                                flash_flag,
                                mgmt_gpio=t["mgmt_gpio"],
                                flash_only=args.flash_only,
                            )
                        # elif t["io"]:
                        #     exec_test(
                        #         test,
                        #         start_time,
                        #         writer,
                        #         t["hex_file_path"],
                        #         flash_flag,
                        #         io=t["io"],
                        #         mode=t["mode"],
                        #         flash_only=args.flash_only,
                        #     )
                        # elif t["spi"]:
                        #     exec_test(
                        #         test,
                        #         start_time,
                        #         writer,
                        #         t["hex_file_path"],
                        #         flash_flag,
                        #         spi_flag=t["spi"],
                        #         spi=spi,
                        #         flash_only=args.flash_only,
                        #     )
                        # elif t["external"]:
                        #     exec_test(
                        #         test,
                        #         start_time,
                        #         writer,
                        #         t["hex_file_path"],
                        #         flash_flag,
                        #         external=t["external"],
                        #         flash_only=args.flash_only,
                        #     )
                        # elif t["clock"]:
                        #     exec_test(
                        #         test,
                        #         start_time,
                        #         writer,
                        #         t["hex_file_path"],
                        #         flash_flag,
                        #         clock=t["clock"],
                        #         la_device=device3_data
                        #     )
                        else:
                            exec_test(
                                test,
                                start_time,
                                writer,
                                t["hex_file_path"],
                                flash_flag,
                                flash_only=args.flash_only,
                                uart_data=uart_data
                            )
                        counter += 1
                        test.close_devices()
                        time.sleep(5)

                        with open(os.devnull, 'a') as f:
                            sys.stdout = f
                            devices = device.open_devices()
                            sys.stdout = sys.__stdout__

            if not test_flag:
                test.console.print(f"[red]ERROR : Coun't find test {args.test}")

        test.console.print("==============================================================================")
        test.console.print("  All Tests Complete")
        test.console.print("==============================================================================")
        test.close_devices()
        # Load CSV data
        with open('results.csv') as f:
            reader = csv.reader(f)
            headers = next(reader)

            table = Table(title="Regression Results")

            for header in headers:
                table.add_column(header)

            for row in reader:
                table.add_row(*row)

            test.console.print(table)

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
