from caravel import Dio, Test, accurate_delay
from io_config import Device, device, connect_devices, UART, SPI
import logging
import os
import csv
import sys
import time
import subprocess
import signal
from manifest import TestDict, device1_sn, device2_sn, device3_sn, voltage


def init_ad_ios(device1_data, device2_data, device3_data):
    device1_dio_map = {
        "rstb": Dio(0, device1_data, True),
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


def process_data(test):
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
    uart.open()
    if test.test_name == "uart":
        rgRX = ""
        timeout = time.time() + 50
        pulse_count = test.receive_packet(250)
        if pulse_count == 2:
            print("start UART transmission")
        while True:
            uart_data, count = uart.read_uart()
            if uart_data:
                uart_data[count.value] = 0
                rgRX = rgRX + uart_data.value.decode()
                if test.passing_criteria[0] in rgRX:
                    print(rgRX)
                    break
            if time.time() > timeout:
                print(f"{test.test_name} test failed with {test.voltage}v supply")
                return False
        pulse_count = test.receive_packet(250)
        if pulse_count == 5:
            print("end UART transmission")
    elif test.test_name == "uart_reception":
        for i in test.passing_criteria:
            pulse_count = test.receive_packet(250)
            if pulse_count == 4:
                uart.write(i)
            pulse_count = test.receive_packet(250)
            if pulse_count == 6:
                print(f"Successfully sent {i} over UART!")
            if pulse_count == 9:
                print(f"Couldn't send {i} over UART!")
                return False
    elif test.test_name == "uart_loopback":
        for i in range(0, 5):
            while time.time() < timeout:
                uart_data, count = uart.read_uart()
                if uart_data:
                    uart_data[count.value] = 0
                    dat = uart_data.value.decode()
                    uart.write(dat)
                    pulse_count = test.receive_packet(250)
                    if pulse_count == 6:
                        print(f"Successfully sent {dat} over UART!")
                        break
                    if pulse_count == 9:
                        print(f"Couldn't send {dat} over UART!")
                        return False
    for i in range(0, 3):
        pulse_count = test.receive_packet(250)
        if pulse_count == 3:
            print("end UART test")
    return True


def process_mem(test):
    phase = 0
    mem_size = 0
    while True:
        pulse_count = test.receive_packet(250)
        if pulse_count == 1:
            print("start test")
        if pulse_count == 5:
            print(f"passed mem size {mem_size}")
            mem_size = mem_size + 1
        if pulse_count == 3:
            if phase > 1:
                print("Test finished")
                return True
            else:
                phase = phase + 1
                print("end test")

        if pulse_count == 9:
            print(
                f"{test.test_name} test failed with {test.voltage}v supply, mem size {mem_size}"
            )
            return mem_size


def hk_stop(close):
    global pid
    if not close:
        print("running caravel_hkstop.py...")
        p = subprocess.Popen(
            ["python3", "caravel_board/firmware_vex/util/caravel_hkstop.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        pid = p.pid
        print("subprocess pid:", pid)
    elif pid:
        print("stopping caravel_hkstop.py...")
        os.kill(pid, signal.SIGTERM)
        pid = None


def process_io(test, io):
    phase = 0
    io_pulse = 0
    if io == "low":
        rst = 0
    if io == "high":
        rst = 2
    end_pulses = 0
    while end_pulses < 2:
        pulse_count = test.receive_packet(250)
        if phase == 0 and pulse_count == 1:
            print("Start test")
            phase = phase + 1
        elif phase > 0 and pulse_count == 1:
            rst = rst + 1
            end_pulses = end_pulses + 1
        elif pulse_count > 1:
            end_pulses = 0
            if rst < 2:
                channel = (pulse_count - 2) + (9 * rst)
            elif rst == 2:
                channel = 37 - (pulse_count - 2)
            elif rst == 3:
                channel = 28 - (pulse_count - 2)
            phase = phase + 1
            if channel == 5:
                hk_stop(True)
            print(f"start sending pulses to gpio[{channel}]")
            if channel > 13 and channel < 22:
                io = test.deviced.dio_map[channel]
            if channel > 21:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            state = "HI"
            timeout = time.time() + 20
            accurate_delay(125)
            while 1:
                accurate_delay(250)
                x = io.get_value()
                if state == "LOW":
                    if x:
                        state = "HI"
                elif state == "HI":
                    if not x:
                        state = "LOW"
                        io_pulse = io_pulse + 1
                if io_pulse == 4:
                    io_pulse = 0
                    print(f"gpio[{channel}] Passed")
                    break
                if time.time() > timeout:
                    print(f"Timeout failure on gpio[{channel}]!")
                    return False, channel
    return True, None


def process_spi(test, spi):
    csb = spi.device_data.dio_map[spi.cs]

    while not csb.get_value():
        pass

    print("CSB is high")

    spi.enabled()
    spi.rw_mode = "r"
    data1 = ""
    data2 = ""
    for i in range(0, 8):
        spi.clk_trig()
        data1 = data1 + str(spi.data[i])
    spi.data = []
    for i in range(0, 8):
        spi.clk_trig()
        data2 = data2 + str(spi.data[i])
    print(int(data1, 2))
    print(int(data2, 2))


def process_input_io(test, io):
    count = 0
    if io == "low":
        channel = 0
    else:
        channel = 37
    while count < 19:
        if channel == 5:
            hk_stop(True)
        pulse_count = test.receive_packet(250)
        if pulse_count == 1:
            print(f"Sending 4 pulses on gpio[{channel}]")
            test.send_pulse(4, channel, 50)
            ack_pulse = test.receive_packet(250)
            if ack_pulse == 5:
                print(f"gpio[{channel}] Failed to send pulse")
                return False, channel
            elif ack_pulse == 3:
                print(f"gpio[{channel}] sent pulse successfully")
            if io == "low":
                channel = channel + 1
            else:
                channel = channel - 1
            count = count + 1
    return True, None


def flash_test(test, hex_file, uart, uart_data, mem, io, mode, spi_flag, spi):
    test.apply_reset()
    test.powerup_sequence()
    test.flash(hex_file)
    test.release_reset()
    test.powerup_sequence()
    logging.info(f"   changing VCORE voltage to {test.voltage}v")
    test.device1v8.supply.set_voltage(test.voltage)
    test.reset()
    if uart:
        return process_uart(test, uart_data)
    elif mem:
        return process_mem(test)
    elif io:
        hk_stop(False)
        if mode == "output":
            return process_io(test, io)
        elif mode == "input":
            return process_input_io(test, io)
        else:
            print(f"ERROR : No {mode} mode")
            exit(1)
    elif spi_flag:
        return process_spi(test, spi)
    else:
        return process_data(test)


def exec_test(
    test,
    start_time,
    writer,
    hex_file,
    uart=False,
    uart_data=None,
    mem=False,
    io=False,
    mode="low",
    spi_flag=False,
    spi=None,
):
    results = flash_test(test, hex_file, uart, uart_data, mem, io, mode, spi_flag, spi)
    end_time = time.time() - start_time
    arr = [test.test_name, test.voltage, results, end_time]
    writer.writerow(arr)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info("  Running:  caravel.py")
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
        device3 = Device(device3_data, 1, device3_dio_map)

        test = Test(device1, device2)
        uart_data = UART(device1_data)
        spi = SPI(device1_data)

        csv_header = ["test_name", "voltage (v)", "Pass/Fail", "Time"]
        if os.path.exists("./results.csv"):
            os.remove("./results.csv")

        with open("results.csv", "a", encoding="UTF8") as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(csv_header)
            for t in TestDict:
                start_time = time.time()
                test.test_name = t["test_name"]
                test.passing_criteria = t["passing_criteria"]
                for v in voltage:
                    test.voltage = v
                    logging.info(f"  Running:  {test.test_name}")
                    if t["uart"]:
                        exec_test(
                            test,
                            start_time,
                            writer,
                            t["hex_file_path"],
                            True,
                            uart_data,
                        )
                    elif t["mem"]:
                        exec_test(
                            test, start_time, writer, t["hex_file_path"], mem=True
                        )
                    elif t["io"]:
                        exec_test(
                            test,
                            start_time,
                            writer,
                            t["hex_file_path"],
                            io=t["io"],
                            mode=t["mode"],
                        )
                    elif t["spi"]:
                        exec_test(
                            test,
                            start_time,
                            writer,
                            t["hex_file_path"],
                            spi_flag=t["spi"],
                            spi=spi,
                        )
                    else:
                        exec_test(test, start_time, writer, t["hex_file_path"])
        test.close_devices()
        sys.exit(0)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            test.close_devices()
            sys.exit(1)
        except SystemExit:
            test.close_devices()
            os._exit(1)
