from caravel import *


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



def process_data(test):
    phase = 0
    for passing in test.passing_criteria:
        pulse_count = test.receive_packet(250)
        if pulse_count == passing:
            print(f"pass phase {phase}")
            phase = phase + 1

        if pulse_count == 9:
            if test.sram == 1:
                print(f"{test.test_name} test failed with {test.voltage}v supply on OPENram!")
                return False
            else:
                print(f"{test.test_name} test failed with {test.voltage}v supply on DFFRAM!")
                return False
            break

    if len(test.passing_criteria) == phase:
        if test.sram == 1:
            print(f"{test.test_name} test Passed with {test.voltage}v supply on OPENram!")
            return True
        else:
            print(f"{test.test_name} test Passed with {test.voltage}v supply on DFFRAM!")
            return True

def process_mem(test):
    phase = 0
    mem_size = 0
    while True:
        pulse_count = test.receive_packet(250)
        if pulse_count == 1:
            print(f"start test")
        if pulse_count == 5:
            print(f"passed mem size {mem_size}")
            mem_size = mem_size + 1
        if pulse_count == 3:
            if phase > 1:
                print("Test finished")
                return True
            else:
                phase = phase + 1
                print(f"end test")

        if pulse_count == 9:
            if test.sram == 1:
                print(f"{test.test_name} test failed with {test.voltage}v supply on OPENram mem size {mem_size}")
                return False
            else:
                print(f"{test.test_name} test failed with {test.voltage}v supply on DFFRAM mem size {mem_size}")
                return False
            break

def process_io(test, channel):
    phase = 0
    io_pulse = 0
    timeout = time.time() + 30
    for passing in test.passing_criteria:
        pulse_count = test.receive_packet()
        if phase == 0 and pulse_count == 1:
            print("pass phase 1")
            phase = phase + 1
        if phase == 1 and pulse_count == 2:
            print("pass phase 2")
            phase = phase + 1
        if phase == 2 and pulse_count == 5:
            print(f"start sending pulses to gpio[{channel}]")
            phase = phase + 1
            if channel > 13:
                io = test.device3v3.dio_map[channel]
            else:
                io = test.device1v8.dio_map[channel]
            state = "HI"
            accurate_delay(125)
            while 1:
                accurate_delay(250)
                x = io.get_value()
                if state == "LOW":
                    if x == True:
                        state = "HI"
                elif state == "HI":
                    if x == False:
                        state = "LOW"
                        io_pulse = io_pulse + 1
                if io_pulse == 10:
                    break
                if time.time() > timeout:
                    break
        if phase == 3 and pulse_count == 7:
            print(f"end sending pulses to gpio[{channel}]")
            phase = phase + 1
        if phase == 4 and pulse_count == 3:
            print("end test")
            phase = phase + 1
        if phase == 5 and pulse_count == 3:
            print("end test")
            phase = phase + 1
        if phase == 6 and pulse_count == 3:
            print("end test")
            phase = phase + 1

        if pulse_count == 9:
            if test.sram == 1:
                print(f"{test.test_name} test failed with {test.voltage}v supply on OPENram!")
                return False
            else:
                print(f"{test.test_name} test failed with {test.voltage}v supply on DFFRAM!")
                return False
            break

    if io_pulse == 10:
        if test.sram == 1:
            print(f"{test.test_name} test Passed with {test.voltage}v supply on OPENram!")
            return True
        else:
            print(f"{test.test_name} test Passed with {test.voltage}v supply on DFFRAM!")
            return True
    else:
        print("Test Failed!")
        return False



def exec_tests(
    test, fflash, channel, io, mem
):
    test.powerup_sequence()
    logging.info(f"   changing VCORE voltage to {test.voltage}v")
    test.change_voltage()
    test.reset()
    if fflash == 1:
        test.exec_flashing()

    if io:
        return process_io(
            test, channel
        )
    elif mem:
        return process_mem(test)
    else:
        return process_data(test)


def exec_test(test, writer, io, channel, automatic_voltage, mem):
    fflash = 1
    if automatic_voltage:
        for i in range(0, 7):
            test.voltage = 1.8 - i * 0.05
            results = exec_tests(
                test,
                fflash,
                channel,
                io,
                mem,
            )
            if test.sram == 1:
                arr = [test.test_name, "OPENram", test.voltage, results]
            else:
                arr = [test.test_name, "DFFRAM", test.voltage, results]
            writer.writerow(arr)
            i = i + 1
            fflash = 0
    else:
        results = exec_tests(
            test,
            fflash,
            channel,
            io,
            mem,
        )
        if test.sram == 1:
            arr = [test.test_name, "OPENram", test.voltage, results]
        else:
            arr = [test.test_name, "DFFRAM", test.voltage, results]
        writer.writerow(arr)
        fflash = 0

def run_test(test, writer, automatic_voltage, io=False, channel="gpio_mgmt", sram=None, mem=False):
    logging.info(f"  Running {test.test_name} test")
    if sram == None:
        test.sram = 1
        exec_test(test, writer, io, channel, automatic_voltage, mem)
        test.sram = 0
    elif sram == "sram":
        test.sram = 1
    elif sram == "dff":
        test.sram = 0
    exec_test(test, writer, io, channel, automatic_voltage, mem)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process LVS check.")
    parser.add_argument(
        "-sp", "--send_packet", help="send packet test", action="store_true"
    )
    parser.add_argument("-b", "--blink", help="blink test", action="store_true")
    parser.add_argument(
        "-cs", "--cpu_stress", help="cpu stress test", action="store_true"
    )
    parser.add_argument(
        "-ms", "--mem_stress", help="cpu stress test", action="store_true"
    )
    parser.add_argument(
        "-mtd", "--mem_test_dffram", help="cpu stress test", action="store_true"
    )
    parser.add_argument(
        "-mts", "--mem_test_sram", help="cpu stress test", action="store_true"
    )
    parser.add_argument(
        "-it", "--irq_timer", help="IRQ timer test", action="store_true"
    )
    parser.add_argument(
        "-to", "--timer0_oneshot", help="timer0 oneshot test", action="store_true"
    )
    parser.add_argument("-iu", "--irq_uart", help="irq uart test", action="store_true")
    parser.add_argument(
        "-tp", "--timer0_periodic", help="timer0 periodic test", action="store_true"
    )
    parser.add_argument(
        "-bb37", "--cpu_bitbang_37_o", help="cpu_bitbang_37_o test", action="store_true"
    )
    parser.add_argument(
        "-bb36", "--cpu_bitbang_36_o", help="cpu_bitbang_36_o test", action="store_true"
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

    csv_header = ["test_name", "ram", "voltage (v)", "Pass/Fail"]
    if os.path.exists("./results.csv"):
        os.remove("./results.csv")

    with open("results.csv", "a", encoding="UTF8") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(csv_header)
        if args.voltage:
            test.voltage = float(args.voltage)

        if args.send_packet:
            test.test_name = "send_packet"
            test.passing_criteria = [1, 2, 3, 4, 5, 6, 7, 8]
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
        if args.cpu_stress:
            test.test_name = "cpu_stress"
            test.passing_criteria = [1, 2, 3, 4, 5, 1, 1, 1]
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
        if args.blink:
            test.test_name = "blink"
            test.passing_criteria = [1, 1, 1, 1]
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
        if args.mem_test_dffram:
            test.passing_criteria = [1, 3, 3, 3]
            test.test_name = f"mem_dff_test"
            if args.voltage_all:
                run_test(test, writer, True, sram="dff", mem=True)
            else:
                run_test(test, writer, False, sram="dff", mem=True)
        if args.mem_test_sram:
            test.passing_criteria = [1, 3, 3, 3]
            test.test_name = f"mem_sram_test"
            if args.voltage_all:
                run_test(test, writer, True, sram="sram", mem=True)
            else:
                run_test(test, writer, False, sram="sram", mem=True)
        if args.mem_stress:
            test.passing_criteria = [1, 2, 3, 4, 7, 7, 7]
            arr = [100, 200, 400, 600, 1200, 1600]
            for i in arr:
                test.sram = 1
                test.test_name = f"mem_stress_{i}"
                run_test(test, writer)
        if args.irq_timer:
            test.test_name = "IRQ_timer"
            test.passing_criteria = [1, 5, 3, 3, 3]
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
        if args.timer0_oneshot:
            test.passing_criteria = [1, 5, 3, 3, 3]
            test.test_name = "timer0_oneshot"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
        if args.irq_uart:
            test.passing_criteria = [1, 5, 3, 3, 3]
            test.test_name = "IRQ_uart"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
        if args.timer0_periodic:
            test.passing_criteria = [1, 5, 3, 3, 3]
            test.test_name = "timer0_periodic"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
        if args.cpu_bitbang_37_o:
            test.passing_criteria = [1, 2, 5, 7, 3, 3, 3]
            test.test_name = "cpu_bitbang_37_o"
            if args.voltage_all:
                run_test(test, writer, True, True, 37)
            else:
                run_test(test, writer, False, True,  37)
        if args.cpu_bitbang_36_o:
            test.passing_criteria = [1, 2, 5, 7, 3, 3, 3]
            test.test_name = "cpu_bitbang_36_o"
            if args.voltage_all:
                run_test(test, writer, True, True, 36)
            else:
                run_test(test, writer, False, True,  36)

        if args.all:
            test.passing_criteria = [1, 2, 3, 4, 5, 1, 1, 1]
            test.test_name = "cpu_stress"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
            test.passing_criteria = [1, 5, 3, 3, 3]
            test.test_name = "IRQ_timer"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
            test.test_name = "timer0_oneshot"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
            test.test_name = "IRQ_uart"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
            test.test_name = "timer0_periodic"
            if args.voltage_all:
                run_test(test, writer, True)
            else:
                run_test(test, writer, False)
            test.passing_criteria = [1, 3, 3, 3]
            test.test_name = f"mem_dff_test"
            if args.voltage_all:
                run_test(test, writer, True, sram="dff", mem=True)
            else:
                run_test(test, writer, False, sram="dff", mem=True)
            test.test_name = f"mem_sram_test"
            if args.voltage_all:
                run_test(test, writer, True, sram="sram", mem=True)
            else:
                run_test(test, writer, False, sram="sram", mem=True)
            test.passing_criteria = [1, 2, 3, 4, 7, 7, 7]
            arr = [100, 200, 400, 600, 1200, 1600]
            for i in arr:
                test.sram = 1
                test.test_name = f"mem_stress_{i}"
                run_test(test, writer)

    test.close_devices()
