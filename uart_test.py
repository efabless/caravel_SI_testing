from caravel import *

def init_ios(device1_data, device2_data, device3_data):
    device1_dio_map = {
        "rstb": Dio(14, device1_data, True),
        "gpio_mgmt": Dio(15, device1_data),
        0: Dio(0, device1_data),
        1: Dio(1, device1_data),
        2: Dio(2, device1_data),
        3: Dio(3, device1_data),
        4: Dio(4, device1_data),
        5: Dio(5, device1_data),
        6: Dio(6, device1_data),
        7: Dio(7, device1_data),
        8: Dio(8, device1_data),
        9: Dio(9, device1_data),
        10: Dio(10, device1_data),
        11: Dio(11, device1_data),
        12: Dio(12, device1_data),
        13: Dio(13, device1_data),
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process LVS check.")
    parser.add_argument(
        "-uart", "--uart", help="uart transmission test", action="store_true"
    )
    parser.add_argument(
        "-va", "--voltage_all", help="automatically change test voltage", action="store_true"
    )
    parser.add_argument(
        "-v", "--voltage", help="change test voltage"
    )
    parser.add_argument("-a", "--all", help="run all tests", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info("  Running:  caravel.py")
    # open multiple devices
    devices = device.open_devices()
    # connect devices using hardcoded serial numbers
    device1_data, device2_data, device3_data = connect_devices(devices)

    logging.info("   Initializing I/Os for both devices")
    # Initializing I/Os
    device1_dio_map, device2_dio_map, device3_dio_map = init_ios(device1_data, device2_data, device3_data)
    # Initilizing devices
    device1 = Device(device1_data, 0, device1_dio_map)
    device2 = Device(device2_data, 1, device2_dio_map)
    device3 = Device(device3_data, 2, device3_dio_map)

    test = Test(device1, device2, device3)

    uart = UART(device1_data)
    uart.open()
    test.apply_reset()
    test.powerup_sequence()
    logging.info(f"   changing VCORE voltage to {test.voltage}v")
    test.change_voltage()
    test.test_name = "uart"
    test.exec_flashing()
    test.release_reset()
    phase = 0
    io_pulse = 0
    rgRX = ""
    try:
        while 1:
            uart_data, count = uart.read_uart()
            if uart_data:
                uart_data[count.value] = 0
                rgRX = rgRX + uart_data.value.decode()
    except KeyboardInterrupt:
        pass
    print(rgRX)
    # timeout = time.time() + 30
    # test.passing_criteria = [2,5,3,3,3]
    # for passing in test.passing_criteria:
    #     pulse_count = test.receive_packet(250)
    #     if phase == 0 and pulse_count == 2:
    #         print("Start transmission on gpio[6]")
    #         phase = phase + 1
    #         while time.time() < timeout:
    #             uart_data = uart.read_uart()
    #         print(uart_data)
    #     if phase == 1 and pulse_count == 5:
    #         print("End transmission on gpio[6]")
    #         phase = phase + 1
    #     if phase == 2 and pulse_count == 3:
    #         print("end test")
    #         phase = phase + 1
    #     if phase == 3 and pulse_count == 3:
    #         print("end test")
    #         phase = phase + 1
    #     if phase == 4 and pulse_count == 3:
    #         print("end test")
    #         phase = phase + 1

        # if pulse_count == 9:
        #     if test.sram == 1:
        #         print(f"{test.test_name} test failed with {test.voltage}v supply on OPENram!")
        #     else:
        #         print(f"{test.test_name} test failed with {test.voltage}v supply on DFFRAM!")
        #     break


    test.close_devices()