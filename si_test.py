from caravel import Dio, Test, accurate_delay
from io_config import Device, device, connect_devices, UART, SPI
import logging
import os
import csv
import sys
import time, datetime
import subprocess
import signal
from manifest import TestDict, device1_sn, device2_sn, device3_sn, device_ps_sn, voltage, analog


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
    test_names = ["send_packet", "receive_packet"]
    for name in test_names:
        test.test_name = name
        if test.test_name == "receive_packet":
            io = test.device1v8.dio_map[0]
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                print("Test started")
            for i in range(5, 8):
                while not io.get_value():
                    pass
                test.send_packet(i, 25)
                while io.get_value():
                    pass
                pulse_count = test.receive_packet(250)
                if pulse_count == i:
                    print(f"sent {i} pulses successfully")
                else:
                    print(f"{test.test_name} test failed with {test.voltage}v supply!")
                    return False
            return True
        else:
            phase = 0
            for passing in test.passing_criteria:
                pulse_count = test.receive_packet(250)
                if pulse_count == passing:
                    print(f"pass phase {phase}")
                    phase = phase + 1

                if pulse_count == 9:
                    print(f"{test.test_name} test failed with {test.voltage}v supply!")
                    return False

            if len(test.passing_criteria) == phase:
                print(f"{test.test_name} test Passed with {test.voltage}v supply!")
                return True

def process_uart(test, uart):
    """Function to test all UART functionality
    First test: IO[5] as input to caravel and IO[6] as output from caravel
    Second test: UART as output from caravel
    Third test: UART as input to caravel
    Fourth test: UART loopback (tests both input and output)
    """

    test_names = ["uart_io", "uart", "uart_reception", "uart_loopback"]
    for name in test_names:
        test.test_name = name
        pulse_count = test.receive_packet(250)
        if pulse_count == 1:
            print(f"Start test: {name}")

        if name == "uart_io":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                received = test.io_receive(4, 6)
                if received:
                    print("gpio[6] Passed")
                else:
                    print("Timeout failure on gpio[6]!")
                    return False
            pulse_count = test.receive_packet(250)
            if pulse_count == 3:
                print("Send 4 packets to IO[5]")
                test.send_pulse(4, 5, 5)
                ack_pulse = test.receive_packet(250)
                if ack_pulse == 5:
                    print("gpio[5] Failed to send pulse")
                    return False
                elif ack_pulse == 3:
                    print("gpio[5] sent pulse successfully")

        elif test.test_name == "uart":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                print("Start UART transmission")
            uart_data = uart.read_data()
            uart_data = uart_data.decode()
            if "Monitor: Test UART passed" in uart_data:
                print("UART test passed")
            else:
                print("UART test failed")
                return False
            pulse_count = test.receive_packet(250)
            if pulse_count == 5:
                print("end UART transmission")

        elif test.test_name == "uart_reception":
            pulse_count = test.receive_packet(250)
            if pulse_count == 2:
                print("Start UART transmission")
            uart.open()
            timeout = time.time() + 50
            for i in ["M", "B", "A"]:
                pulse_count = test.receive_packet(250)
                if pulse_count == 4:
                    uart.write(i)
                pulse_count = test.receive_packet(250)
                if pulse_count == 6:
                    print(f"Successfully sent {i} over UART!")
                if pulse_count == 9:
                    print(f"Couldn't send {i} over UART!")
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
                            print(f"Successfully sent {dat} over UART!")
                            break
                        if pulse_count == 9:
                            print(f"Couldn't send {dat} over UART!")
                            uart.close()
                            return False
    return True

def process_soc(test, uart):
    while True:
        uart_data = uart.read_data()
        uart_data = uart_data.decode()
        if "Start Test:" in uart_data:
            test.test_name = uart_data.split(": ")[1]
            print(f"Start Test: {test.test_name}")
        elif "End Test" in uart_data:
            print(uart_data)
            break
        uart_data = uart.read_data()
        uart_data = uart_data.decode()
        if "passed" in uart_data:
            print(f"{test.test_name} passed")
        elif "failed" in uart_data:
            print(f"{test.test_name} failed")
            return False
    return True

def flash_test(
    test, hex_file, flash_flag, uart, uart_data, mem, io, mode, spi_flag, spi, external
):
    test.reset_devices()
    if flash_flag:
        logging.info(f"==============================================================================")
        logging.info(f"  Flashing :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
        logging.info(f"==============================================================================")
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
    logging.info(f"   changing VCORE voltage to {test.voltage}v")
    # test.device1v8.supply.set_voltage(test.voltage)
    test.device_power.supply.set_voltage(test.voltage)
    test.reset()

    logging.info(f"==============================================================================")
    logging.info(f"  Running  :  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
    logging.info(f"==============================================================================")

    results = None

    if uart:
        results = process_uart(test, uart_data)
    elif mem:
        results = process_soc(test, uart_data)
    # elif io:
    #     if mode == "output":
    #         results = process_io(test, io)
    #     elif mode == "input":
    #         results = process_input_io(test, io)
    #     elif mode == "plud":
    #         results = process_io_plud(test)
    #     else:
    #         print(f"ERROR : No {mode} mode")
    #         exit(1)
    # elif spi_flag:
    #     results = process_spi(test, spi)
    # elif external:
    #     results = process_external(test)
    else:
        results = process_mgmt_gpio(test)

    logging.info(f"==============================================================================")
    logging.info(f"  Completed:  {test.test_name} : {datetime.datetime.now()} | Analog : {analog}")
    logging.info(f"==============================================================================")

    return results


def exec_test(
    test,
    start_time,
    hex_file,
    flash_flag=True,
    uart=False,
    uart_data=None,
    mem=False,
    io=False,
    mode="low",
    spi_flag=False,
    spi=None,
    external=False,
):
    results = flash_test(
        test,
        hex_file,
        flash_flag,
        uart,
        uart_data,
        mem,
        io,
        mode,
        spi_flag,
        spi,
        external,
    )
    end_time = time.time() - start_time
    arr = [test.test_name, test.voltage, results, end_time]
    with open("results.csv", "a", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(arr)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info(f"=============================================================")
        if analog:
            logging.info(f"  Beginning Tests for analog project")
        else:
            logging.info(f"  Beginning Tests for digital project")
        logging.info(f"=============================================================")
        # open multiple devices
        devices = device.open_devices()
        # connect devices using hardcoded serial numbers
        d1_sn = bytes(device1_sn, "utf-8")
        d2_sn = bytes(device2_sn, "utf-8")
        d3_sn = bytes(device3_sn, "utf-8")
        dps_sn = bytes(device_ps_sn, "utf-8")
        device1_data, device2_data, device3_data, device_ps_data = connect_devices(
            devices, d1_sn, d2_sn, d3_sn, dps_sn
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
        device_ps = Device(device_ps_data, 3, None)

        test = Test(device1, device2, device3, device_power=device_ps)
        uart_data = UART(device1_data)
        spi = SPI(device1_data)

        csv_header = ["Test_name", "Voltage (v)", "Pass/Fail", "Time (s)"]
        if os.path.exists("./results.csv"):
            os.remove("./results.csv")

        with open("results.csv", "a", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)

        for t in TestDict:
            start_time = time.time()
            test.test_name = t["test_name"]
            test.passing_criteria = t["passing_criteria"]
            flash_flag = True
            counter = 0
            for v in voltage:
                test.voltage = v
                time.sleep(5)
                if counter > 0:
                    flash_flag = False
                if t["uart"]:
                    exec_test(
                        test,
                        start_time,
                        t["hex_file_path"],
                        flash_flag,
                        True,
                        uart_data,
                    )
                elif t["mem"]:
                    exec_test(
                        test,
                        start_time,
                        t["hex_file_path"],
                        flash_flag,
                        mem=True,
                    )
                elif t["io"]:
                    exec_test(
                        test,
                        start_time,
                        t["hex_file_path"],
                        flash_flag,
                        io=t["io"],
                        mode=t["mode"],
                    )
                elif t["spi"]:
                    exec_test(
                        test,
                        start_time,
                        t["hex_file_path"],
                        flash_flag,
                        spi_flag=t["spi"],
                        spi=spi,
                    )
                elif t["external"]:
                    exec_test(
                        test,
                        start_time,
                        t["hex_file_path"],
                        flash_flag,
                        external=t["external"],
                    )
                else:
                    exec_test(
                        test, start_time, t["hex_file_path"], flash_flag
                    )
                counter += 1
                test.close_devices()
                time.sleep(5)
                devices = device.open_devices()
        logging.info(f"=============================================================")
        logging.info(f"  All Tests Complete")
        logging.info(f"=============================================================")
        test.close_devices()
        os._exit(0)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            test.close_devices()
            os._exit(1)
        except SystemExit:
            test.close_devices()
            os._exit(1)
