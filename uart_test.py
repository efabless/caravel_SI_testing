import fileinput
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

def modify_hex(hex_file, c_file):
    c_file = open(c_file, "r")
    hex_data = []
    new_hex_data = ""
    first_line = 2
    flag = False
    for aline in c_file:
        aline = aline.strip()
        if aline:
            if aline.startswith("char"):
                idx = aline.find("{")
                line = aline[idx + 1 : -4]
                data = [item.strip() for item in line.split(",")]
            if aline.startswith("int"):
                indx = aline.find("=")
                arr_size = aline[indx + 1 : -1].strip()
                if int(arr_size) > 255:
                    logging.error(" Array size should be less that 255")
                    sys.exit()
    for i in data:
        hex_data.append(i[2:])

    with fileinput.input(hex_file, inplace=True, backup=".bak") as f:
        for line in f:
            line = line.strip()
            if line:
                if line.startswith("@"):
                    if first_line > 0:
                        print(line)
                        first_line = first_line - 1
                    else:
                        print(line)
                        flag = True
                elif flag == False:
                    print(line)
                elif flag == True:
                    count = 0
                    for d in hex_data:
                        if count < 16:
                            new_hex_data = new_hex_data + " " + d
                            count = count + 1
                        else:
                            print(new_hex_data[1:])
                            new_hex_data = ""
                            count = 1
                            new_hex_data = new_hex_data + " " + d
                    while len(new_hex_data[1:].split()) < 16:
                        new_hex_data = new_hex_data + " " + "00"
                    print(new_hex_data[1:])
                    print(
                        f"{str(hex(int(arr_size)))[2:].capitalize()} 00 00 00 00 00 00 00 "
                    )
                    break


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
    parser.add_argument("-p", "--part", help="part name", required=True)
    args = parser.parse_args()

    run_cmd = ['python3', 'io_config.py', '-ol6', '-v', f'{args.voltage}', '-p', f'{args.part}']
    subprocess.run(run_cmd)
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
    test.voltage = float(args.voltage)
    uart = UART(device1_data)
    if test.sram == 1:
        modify_hex(
                f"caravel_board/firmware_vex/silicon_tests/uart/uart_sram.hex",
                "gpio_config_data.c",
            )
    else:
        modify_hex(
                f"caravel_board/firmware_vex/silicon_tests/uart/uart_dff.hex",
                "gpio_config_data.c",
            )
    uart.open()
    test.apply_reset()
    test.powerup_sequence()
    logging.info(f"   changing VCORE voltage to {test.voltage}v")
    test.test_name = "uart"
    test.exec_flashing()
    test.release_reset()
    timeout = time.time() + 50
    rgRX = ""
    pulse_count = test.receive_packet(250)
    if pulse_count == 2:
        print(f"start UART transmission")
    while time.time() < timeout:
        uart_data, count = uart.read_uart()
        if uart_data:
            uart_data[count.value] = 0
            rgRX = rgRX + uart_data.value.decode()
            if "Monitor: Test UART passed" in rgRX:
                print(rgRX)
                break
    pulse_count = test.receive_packet(250)
    if pulse_count == 5:
        print(f"end UART transmission")
    for i in range(0,3):
        pulse_count = test.receive_packet(250)
        if pulse_count == 3:
            print(f"end UART test")


    test.close_devices()