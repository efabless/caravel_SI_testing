from caravel import *
import fileinput

class Gpio:
    def __init__(self):
        self.array = []
        self.fail_count = []
        self.failed = False
        self.init_array()
        self.init_fail_count()
    def get_fail_count(self, channel):
        return self.fail_count[channel]
    def init_fail_count(self):
        for i in range(0,19):
            self.fail_count.append(0)
    def increment_fail_count(self, channel):
        self.fail_count[channel] = self.fail_count[channel] + 1
    def init_array(self):
        for i in range(0,19):
            if i == 0:
                self.array.append("H_NONE")
            else:
                self.array.append("H_INDEPENDENT")
    def gpio_failed(self):
        self.failed = True
    def get_gpio_failed(self):
        return(self.failed)
    def set_config(self, channel, config):
        self.array[channel] = config
    def get_config(self, channel):
        return self.array[channel]

def run_builder(gpio_l, gpio_h):
    gpio_l = ','.join(gpio_l)
    gpio_h = ','.join(gpio_h)
    subprocess.call(
            f"python3 caravel_board/firmware_vex/gpio_config/gpio_config_builder.py -gpio_l {gpio_l} -gpio_h {gpio_h} -num_io 19 -config C_MGMT_OUT",
            shell=True,
        )

def modify_hex(hex_file, c_file):
    c_file = open(c_file, 'r')
    hex_data = []
    new_hex_data = ""
    first_line = 1
    flag = False
    for aline in c_file:
        aline = aline.strip()
        if aline:
            if aline.startswith('char'):
                idx = aline.find('{')
                line = aline[idx+1:-4]
                data = [item.strip() for item in line.split(',')]
            if aline.startswith('int'):
                indx = aline.find('=')
                arr_size = aline[indx+1:-1].strip()
                if int(arr_size) > 255:
                    logging.error(" Array size should be less that 255")
                    sys.exit()
    for i in data:
        hex_data.append(i[2:])

    with fileinput.input(hex_file, inplace=True, backup='.bak') as f:
        for line in f:
            line = line.strip()
            if line:
                if line.startswith('@'):
                    if first_line == 1:
                        print(line)
                        first_line = 0
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
                    print(f"{str(hex(int(arr_size)))[2:].capitalize()} 00 00 00 00 00 00 00 ")
                    break

def exec_flash(test):
    logging.info("   Flashing CPU")
    test.apply_reset()
    test.powerup_sequence()
    test.flash(f"caravel_board/firmware_vex/{test.test_name}/{test.test_name}.hex")
    test.powerup_sequence()
    test.release_reset()

def init_ios(device1_data, device2_data, device3_data):
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

def run_test(test):
    phase = 0
    io_pulse = 0
    rst = 0
    end_pulses = 0
    while end_pulses < 2:
        pulse_count = test.receive_packet()
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
            print(f"start sending pulses to gpio[{channel}]")
            if channel > 13 and channel < 22:
                io = test.deviced.dio_map[channel]
            elif channel > 21:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            state = "HI"
            timeout = time.time() + 0.5
            accurate_delay(12.5)
            while 1:
                accurate_delay(25)
                x = io.get_value()
                if state == "LOW":
                    if x == True:
                        state = "HI"
                elif state == "HI":
                    if x == False:
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

def run_test_h(test):
    phase = 0
    io_pulse = 0
    rst = 0
    end_pulses = 0
    while end_pulses < 2:
        pulse_count = test.receive_packet()
        if phase == 0 and pulse_count == 1:
            print("Start test")
            phase = phase + 1
        elif phase > 0 and pulse_count == 1:
            rst = rst + 1
            phase = phase + 1
            end_pulses = end_pulses + 1
        elif pulse_count > 1:
            end_pulses = 0
            if rst == 0:
                channel = 37 - (pulse_count - 2)
            elif rst == 1:
                channel = 28 - (pulse_count - 2)
            phase = phase + 1
            print(f"start sending pulses to gpio[{channel}]")
            if channel > 13 and channel < 22:
                io = test.deviced.dio_map[channel]
            elif channel > 21:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            state = "HI"
            timeout = time.time() + 0.5
            accurate_delay(12.5)
            while 1:
                accurate_delay(25)
                x = io.get_value()
                if state == "LOW":
                    if x == True:
                        state = "HI"
                elif state == "HI":
                    if x == False:
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

def change_config(channel, gpio_l, gpio_h, part, voltage, start_time):
    end_time = (time.time() - start_time) / 60.
    if channel > 18:
        if gpio_h.get_config(37 - channel) == "H_INDEPENDENT":
            gpio_h.set_config(37 - channel, "H_DEPENDENT")
            gpio_h.increment_fail_count(37 - channel)
        elif gpio_h.get_config(37 - channel) == "H_DEPENDENT":
            gpio_h.set_config(37 - channel, "H_INDEPENDENT")
            gpio_h.increment_fail_count(37 - channel)
        if gpio_h.get_fail_count(37 - channel) > 1:
            gpio_h.gpio_failed()
            print(f"gpio[{channel}] not working")
            print("Final configuration for gpio_l: ", gpio_l.array)
            print("Final configuration for gpio_h: ", gpio_h.array)
            print("Configuring the ios took: ", (time.time() - start_time) / 60., "minutes")
            f = open(f"{part}.txt", 'a')
            f.write(f"\n\nPart: {part}\n")
            f.write(f"voltage: {voltage}\n")
            f.write("Final configuration: \n")
            f.write(f"configuration failed in gpio[{channel}], anything after is invalid\n")
            f.write(f"gpio from 37 to 19: {gpio_h.array}\n")
            f.write(f"Execution time: {end_time} minutes\n")
            f.close()
            test.turn_off_devices()
        
    else:
        if gpio_l.get_config(channel) == "H_INDEPENDENT":
            gpio_l.set_config(channel, "H_DEPENDENT")
            gpio_l.increment_fail_count(channel)
        elif gpio_l.get_config(channel) == "H_DEPENDENT":
            gpio_l.set_config(channel, "H_INDEPENDENT")
            gpio_l.increment_fail_count(channel)
        if gpio_l.get_fail_count(channel) > 1:
            gpio_l.gpio_failed()
            print(f"gpio[{channel}] not working")
            print("Final configuration for gpio_l: ", gpio_l.array)
            print("Final configuration for gpio_h: ", gpio_h.array)
            print("Configuring the ios took: ", (time.time() - start_time) / 60., "minutes")
            f = open(f"{part}.txt", 'a')
            f.write(f"\n\nPart: {part}\n")
            f.write(f"voltage: {voltage}\n")
            f.write("Final configuration: \n")
            f.write(f"configuration failed in gpio[{channel}], anything after is invalid\n")
            f.write(f"gpio from 0 to 18: {gpio_l.array}\n")
            f.write(f"Execution time: {end_time} minutes\n")
            f.close()
            test.turn_off_devices()
    return gpio_l, gpio_h

def choose_test(test, test_name, gpio_l, gpio_h, start_time, part, chain="low", high=False):
    test_result = False
    while not test_result:
        test.test_name = test_name
        run_builder(gpio_l.array, gpio_h.array)
        modify_hex(f"caravel_board/firmware_vex/{test_name}/{test_name}.hex","gpio_config_data.c")
        exec_flash(test)
        if not high:
            test_result, channel_failed = run_test(test)
        else:
            test_result, channel_failed = run_test_h(test)
        if test_result:
            print("Test Passed!")
            print("Final configuration for gpio_l: ", gpio_l.array)
            print("Final configuration for gpio_h: ", gpio_h.array)
            test_passed(test, start_time, part, gpio_l, gpio_h, chain)
        else:
            if gpio_h.get_gpio_failed() is False and gpio_l.get_gpio_failed() is False:
                gpio_l, gpio_h = change_config(channel_failed, gpio_l, gpio_h, part, test.voltage, start_time)
            else:
                break


def test_passed(test, start_time, part, gpio_l, gpio_h, chain):
    end_time = (time.time() - start_time) / 60.
    
    print("Configuring the ios took: ", end_time, "minutes")

    f = open(f"{part}.txt", 'a')
    f.write(f"\n\nPart: {part}\n")
    f.write(f"voltage: {test.voltage}\n")
    f.write(f"configuration of {chain} chain was successful\n")
    f.write(f"Final configuration of {chain} chain: \n")
    if chain == "low":
        f.write(f"gpio from 0 to 18: {gpio_l.array}\n")
    elif chain == "high":
        f.write(f"gpio from 37 to 19: {gpio_h.array}\n")
    f.write(f"Execution time: {end_time} minutes\n")
    f.close() 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Caravel silicon io configuration.")
    parser.add_argument(
        "-o", "--gpio_output", help="run gpio output configuration test", action="store_true"
    )
    parser.add_argument(
        "-oh", "--gpio_output_h", help="run gpio output high configuration test", action="store_true"
    )
    parser.add_argument(
        "-oa", "--gpio_output_all", help="run gpio output all configuration test", action="store_true"
    )
    parser.add_argument(
        "-c", "--chain", help="run gpio chain configuration test", action="store_true"
    )
    parser.add_argument(
        "-v", "--voltage", help="change test voltage"
    )
    parser.add_argument(
        "-va", "--voltage_all", help="automatically change test voltage", action="store_true"
    )
    parser.add_argument(
        "-p", "--part", help="part name", required=True
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    
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
    gpio_l = Gpio()
    gpio_h = Gpio()

    start_time = time.time()
    start_program = time.time()
    part = args.part

    if os.path.exists(f"./{part}.txt"):
        os.remove(f"./{part}.txt")

    if args.voltage:
        test.voltage = float(args.voltage)

    if args.gpio_output:
        if args.voltage_all:
            for i in range(0, 7):
                start_time = time.time()
                gpio_l = Gpio()
                gpio_h = Gpio()
                test.voltage = 1.8 - i * 0.05
                choose_test(test, "config_io_o", gpio_l, gpio_h, start_time, part=part)
        else:
            choose_test(test, "config_io_o", gpio_l, gpio_h, start_time, part=part)

    if args.gpio_output_all:
        if args.voltage_all:
            for i in range(0, 7):
                start_time = time.time()
                gpio_l = Gpio()
                gpio_h = Gpio()
                test.voltage = 1.8 - i * 0.05
                choose_test(test, "config_io_o_all", gpio_l, gpio_h, start_time, part)
        else:
            choose_test(test, "config_io_o_all", gpio_l, gpio_h, start_time, part)

    if args.gpio_output_h:
        if args.voltage_all:
            for i in range(0, 7):
                gpio_l = Gpio()
                gpio_h = Gpio()
                test.voltage = 1.8 - i * 0.05
                choose_test(test, "config_io_o_h", gpio_l, gpio_h, start_time, part, "high", True)
        else:
            choose_test(test, "config_io_o_h", gpio_l, gpio_h, start_time, part, "high", True)

    
    if args.chain:
        if args.voltage_all:
            for i in range(0, 7):
                start_time = time.time()
                gpio_l = Gpio()
                gpio_h = Gpio()
                test.voltage = 1.8 - i * 0.05
                choose_test(test, "config_io_o_l", gpio_l, gpio_h, start_time, part)
        else:
            choose_test(test, "config_io_o_l", gpio_l, gpio_h, start_time, part)
        
        gpio_l = Gpio()
        gpio_h = Gpio()
        start_time = time.time()

        if args.voltage_all:
            for i in range(0, 7):
                start_time = time.time()
                gpio_l = Gpio()
                gpio_h = Gpio()
                test.voltage = 1.8 - i * 0.05
                choose_test(test, "config_io_o_h", gpio_l, gpio_h, start_time, part, "high", True)
        else:
            choose_test(test, "config_io_o_h", gpio_l, gpio_h, start_time, part, "high", True)

    end_time = (time.time() - start_program) / 60.
    f = open(f"{part}.txt", 'a')
    f.write(f"\n\nTotal Execution time: {end_time} minutes")
    f.close() 
    test.close_devices()
    exit(0)