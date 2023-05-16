import argparse
from caravel import Dio, Test, accurate_delay
from io_config import Device, device, connect_devices, UART, SPI
import logging
import os
import csv
import sys
import time, datetime
import subprocess
import signal
from manifest import TestDict, device1_sn, device2_sn, device3_sn, voltage, analog
from rich.console import Console


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


def run_regression(test, uart, start_time, writer):
    result = False
    uart.open()
    while True:
        uart_data = uart.read_data()
        uart_data = uart_data.decode()
        if "Start Test:" in uart_data:
            print(uart_data)
            test.test_name = uart_data.split(": ")[1]
        elif "End Test" in uart_data:
            print(uart_data)
            break

        if test.test_name == "uart_reception":
            uart.write(["M", "B", "A"])
        uart_data = uart.read_data()
        uart_data = uart_data.decode()
        if test.test_name == "uart":
            if "Monitor: Test UART passed" in uart_data:
                print(uart_data)
                result = True
        else:
            if "passed" in uart_data:
                print(uart_data)
                result = True
            elif "failed" in uart_data:
                print(uart_data)
                result = False

        end_time = time.time() - start_time
        if result:
            arr = [test.test_name, test.voltage, "passed", end_time]
        else:
            arr = [test.test_name, test.voltage, "failed", end_time]
        writer.writerow(arr)

def flash_regression(test, flash_flag):
    test.reset_devices()
    if flash_flag:
        test.power_down()
        test.apply_reset()
        test.power_up_1v8()
        test.flash(f"{os.path.dirname(os.path.realpath(__file__))}/caravel_board/firmware_vex/mpw8_tests/all_test/all_test.hex")
        test.power_down()
        test.release_reset()
    else:
        test.power_down()
        time.sleep(5)
    test.power_up()
    test.device1v8.supply.set_voltage(test.voltage)
    test.reset()


if __name__ == "__main__":
    try:
        # open multiple devices
        devices = device.open_devices()
        # connect devices using hardcoded serial numbers
        d1_sn = bytes(device1_sn, "utf-8")
        d2_sn = bytes(device2_sn, "utf-8")
        d3_sn = bytes(device3_sn, "utf-8")
        device1_data, device2_data, device3_data = connect_devices(
            devices, d1_sn, d2_sn, d3_sn
        )

        logging.info("   Initializing I/Os for both devices")
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
        counter = 0
        flash_flag = True
        csv_header = ["Test_name", "Voltage (v)", "Pass/Fail", "Time (s)"]
        if os.path.exists("./results.csv"):
            os.remove("./results.csv")
        with open("results.csv", "a", encoding="UTF8") as f:
            writer = csv.writer(f)
            for v in voltage:
                start_time = time.time()
                test.voltage = v
                if counter > 0:
                    flash_flag = False
                flash_regression(test, flash_flag)
                counter = 1
                result = run_regression(test, uart_data, start_time, writer)

    except KeyboardInterrupt:
        print("Interrupted")
        try:
            test.close_devices()
            os._exit(1)
        except SystemExit:
            test.close_devices()
            os._exit(1)