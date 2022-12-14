from caravel import *
from io_config import *
import threading


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
                print(
                    f"{test.test_name} test failed with {test.voltage}v supply on OPENram!"
                )
                return False
            else:
                print(
                    f"{test.test_name} test failed with {test.voltage}v supply on DFFRAM!"
                )
                return False
            break

    if len(test.passing_criteria) == phase:
        if test.sram == 1:
            print(
                f"{test.test_name} test Passed with {test.voltage}v supply on OPENram!"
            )
            return True
        else:
            print(
                f"{test.test_name} test Passed with {test.voltage}v supply on DFFRAM!"
            )
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
                print(
                    f"{test.test_name} test failed with {test.voltage}v supply on OPENram mem size {mem_size}"
                )
                return mem_size
            else:
                print(
                    f"{test.test_name} test failed with {test.voltage}v supply on DFFRAM mem size {mem_size}"
                )
                return mem_size
            break

def process_uart(test, uart, part, fflash, fconfig, test_name):
    start_time = time.time()
    gpio_l = Gpio()
    gpio_h = Gpio()
    if fconfig:
        choose_test(test, "config_io_o_l", gpio_l, gpio_h, start_time, part)
        if test_name != "uart":
            mgmt_cust_h = ["C_MGMT_OUT"] * 19
            mgmt_cust_l = ["C_MGMT_OUT"] * 19
            mgmt_cust_l[uart.tx] = "C_MGMT_IN"
            run_builder(gpio_l.array, gpio_h.array, False, custom=True, mgmt_cust_l=mgmt_cust_l, mgmt_cust_h=mgmt_cust_h)
    if test.sram == 1:
        modify_hex(
                f"caravel_board/firmware_vex/silicon_tests/{test_name}/{test_name}_sram.hex",
                "caravel_board/firmware_vex/gpio_config/gpio_config_data.c",
                first_line=2
            )
    else:
        modify_hex(
                f"caravel_board/firmware_vex/silicon_tests/{test_name}/{test_name}_dff.hex",
                "caravel_board/firmware_vex/gpio_config/gpio_config_data.c",
                first_line=2
            )
    uart.open()
    test.apply_reset()
    test.powerup_sequence()
    if fflash:
        test.exec_flashing()
    test.release_reset()
    timeout = time.time() + 50
    rgRX = ""
    pulse_count = test.receive_packet(25)
    if pulse_count == 2:
        print(f"start UART transmission")
    if test_name == "uart":
        while True:
            uart_data, count = uart.read_uart()
            if uart_data:
                uart_data[count.value] = 0
                rgRX = rgRX + uart_data.value.decode()
                if "Monitor: Test UART passed" in rgRX:
                    print(rgRX)
                    break
            if time.time() > timeout:
                print("UART test failed!")
                return False
        pulse_count = test.receive_packet(25)
        if pulse_count == 5:
            print(f"end UART transmission")
    elif test_name == "uart_reception":
        arr = ["M", "B", "A"]
        for i in arr:
            pulse_count = test.receive_packet(25)
            if pulse_count == 4:
                uart.write(i)
            pulse_count = test.receive_packet(25)
            if pulse_count == 6:
                print(f"Successfully sent {i} over UART!")
            if pulse_count == 9:
                print(f"Couldn't send {i} over UART!")
                return False
    elif test_name == "uart_loopback":
        for i in range(0,5):
            while time.time() < timeout:
                uart_data, count = uart.read_uart()
                if uart_data:
                    uart_data[count.value] = 0
                    dat = uart_data.value.decode()
                    uart.write(dat)
                    pulse_count = test.receive_packet(25)
                    if pulse_count == 6:
                        print(f"Successfully sent {dat} over UART!")
                        break
                    if pulse_count == 9:
                        print(f"Couldn't send {dat} over UART!")
                        return False

    for i in range(0,3):
        pulse_count = test.receive_packet(25)
        if pulse_count == 3:
            print(f"end {test_name} test")
    
    return True

def process_spi(test, spi, part, fflash, fconfig):
    start_time = time.time()
    gpio_l = Gpio()
    gpio_h = Gpio()
    if fconfig:
        choose_test(test, "config_io_o_h", gpio_l, gpio_h, start_time, part)
    if test.sram == 1:
        modify_hex(
                f"caravel_board/firmware_vex/silicon_tests/uart/uart_sram.hex",
                "gpio_config_data.c",
                first_line=2
            )
    else:
        modify_hex(
                f"caravel_board/firmware_vex/silicon_tests/uart/uart_dff.hex",
                "gpio_config_data.c",
                first_line=2
            )
    test.apply_reset()
    test.powerup_sequence()
    test.test_name = "spi_master"
    if fflash:
        test.exec_flashing()
    test.release_reset()
    csb = spi.device_data.dio_map[spi.cs]
        
    while csb.get_value() != True:
        pass

    print("CSB is low")

    th1 = threading.Thread(target=spi.enabled())
    spi.rw_mode = "r"
    th2 = threading.Thread(target=spi.clk_trig())
    bit = 0
    th1.start()
    while(bit < 24 and th2.join()):
        th2.start()
        bit = bit + 1
        if bit == 17:
            spi.rw_mode = "w"



def process_input_io(test):
    count = 0
    for i in range(0,10):
        pulse_count = test.receive_packet(250)
        test_count = pulse_count
        if pulse_count != 10 or pulse_count != 9:
            if test.sram:
                time.sleep(1.2)
            else:
                time.sleep(1)
            test.send_packet(pulse_count, 250)
            print(f"recieved {pulse_count} pulses and sent them")
        pulse_count = test.receive_packet(250)
        if pulse_count == 10:
            print(f"test for {test_count} pulses passed!")
            count = count + 1
        elif pulse_count == 9:
            print(f"Test for {test_count} pulses failed!")
            pulse_count = test.receive_packet(250)
            print(f"The CPU received {pulse_count}")
            count = count - 1
    if count > 10:
        return True
    return False


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
                print(
                    f"{test.test_name} test failed with {test.voltage}v supply on OPENram!"
                )
                return False
            else:
                print(
                    f"{test.test_name} test failed with {test.voltage}v supply on DFFRAM!"
                )
                return False
            break

    if io_pulse == 10:
        if test.sram == 1:
            print(
                f"{test.test_name} test Passed with {test.voltage}v supply on OPENram!"
            )
            return True
        else:
            print(
                f"{test.test_name} test Passed with {test.voltage}v supply on DFFRAM!"
            )
            return True
    else:
        print("Test Failed!")
        return False


def exec_tests(test, fflash, fconfig, channel, io, mem, uart, io_input, uart_data, part):
    test.powerup_sequence()
    logging.info(f"   changing VCORE voltage to {test.voltage}v")
    test.change_voltage()
    test.reset()
    if fflash == 1 and not uart:
        test.exec_flashing()

    if io:
        return process_io(test, channel)
    elif mem:
        return process_mem(test)
    elif uart:
        return process_uart(test, uart_data, part, fflash, fconfig, test_name=test.test_name)
    elif io_input:
        return process_input_io(test)
    else:
        return process_data(test)


def exec_test(test, writer, io, channel, automatic_voltage, mem, uart, io_input, uart_data, part, fconfig):
    fflash = 1
    if automatic_voltage:
        for i in range(0, 7):
            test.voltage = 1.8 - i * 0.05
            results = exec_tests(
                test,
                fflash,
                fconfig,
                channel,
                io,
                mem,
                uart,
                io_input,
                uart_data, 
                part,
            )
            if test.sram == 1:
                arr = [test.test_name, "OPENram", test.voltage, results]
            else:
                arr = [test.test_name, "DFFRAM", test.voltage, results]
            writer.writerow(arr)
            i = i + 1
            fflash = 0
            fconfig = 0
    else:
        results = exec_tests(
            test,
            fflash,
            fconfig,
            channel,
            io,
            mem,
            uart,
            io_input,
            uart_data, 
            part,
        )
        if test.sram == 1:
            arr = [test.test_name, "OPENram", test.voltage, results]
        else:
            arr = [test.test_name, "DFFRAM", test.voltage, results]
        writer.writerow(arr)
        fflash = 0
        fconfig = 0


def run_test(
    test, writer, automatic_voltage, io=False, channel="gpio_mgmt", sram=None, mem=False, uart=False, io_input=False, uart_data=None, part=None
):
    logging.info(f"  Running {test.test_name} test")
    fconfig = 1
    if sram == None:
        test.sram = 1
        exec_test(test, writer, io, channel, automatic_voltage, mem, uart, io_input, uart_data, part, fconfig)
        fconfig = 0
        test.sram = 0
    elif sram == "sram":
        test.sram = 1
    elif sram == "dff":
        test.sram = 0
    exec_test(test, writer, io, channel, automatic_voltage, mem, uart, io_input, uart_data, part, fconfig)


if __name__ == "__main__":
    try:
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
            "-mtd", "--mem_test_dffram", help="mem DFFRAM test", action="store_true"
        )
        parser.add_argument(
            "-mts", "--mem_test_sram", help="mem OPENram test", action="store_true"
        )
        parser.add_argument(
            "-mtdhw", "--mem_test_dffram_half_word", help="mem DFFRAM half word test", action="store_true"
        )
        parser.add_argument(
            "-mtshw", "--mem_test_sram_half_word", help="cpu stress half word test", action="store_true"
        )
        parser.add_argument(
            "-mtdw", "--mem_test_dffram_word", help="mem DFFRAM word test", action="store_true"
        )
        parser.add_argument(
            "-mtsw", "--mem_test_sram_word", help="cpu stress word test", action="store_true"
        )
        parser.add_argument(
            "-it", "--irq_timer", help="IRQ timer test", action="store_true"
        )
        parser.add_argument(
            "-to", "--timer0_oneshot", help="timer0 oneshot test", action="store_true"
        )
        parser.add_argument(
            "-iu", "--irq_uart", help="irq uart test", action="store_true"
        )
        parser.add_argument(
            "-u", "--uart_test", help="uart test", action="store_true"
        )
        parser.add_argument(
            "-ur", "--uart_reception_test", help="uart test", action="store_true"
        )
        parser.add_argument(
            "-ul", "--uart_loopback_test", help="uart test", action="store_true"
        )
        parser.add_argument(
            "-tp", "--timer0_periodic", help="timer0 periodic test", action="store_true"
        )
        parser.add_argument(
            "-rp", "--receive_packet", help="receive packet test", action="store_true"
        )
        parser.add_argument(
            "-bb37",
            "--cpu_bitbang_37_o",
            help="cpu_bitbang_37_o test",
            action="store_true",
        )
        parser.add_argument(
            "-bb36",
            "--cpu_bitbang_36_o",
            help="cpu_bitbang_36_o test",
            action="store_true",
        )
        parser.add_argument(
            "-va",
            "--voltage_all",
            help="automatically change test voltage",
            action="store_true",
        )
        parser.add_argument("-v", "--voltage", help="change test voltage")
        parser.add_argument("-a", "--all", help="run all tests", action="store_true")
        parser.add_argument("-am", "--all_mem", help="run all tests", action="store_true")
        parser.add_argument("-p", "--part", help="part name", required=True)
        args = parser.parse_args()

        logging.basicConfig(level=logging.INFO)
        logging.info("  Running:  caravel.py")
        # open multiple devices
        devices = device.open_devices()
        # connect devices using hardcoded serial numbers
        device1_data, device2_data, device3_data = connect_devices(devices)

        logging.info("   Initializing I/Os for both devices")
        # Initializing I/Os
        device1_dio_map, device2_dio_map, device3_dio_map = init_ios(
            device1_data, device2_data, device3_data
        )
        # Initilizing devices
        device1 = Device(device1_data, 0, device1_dio_map)
        device2 = Device(device2_data, 1, device2_dio_map)
        device3 = Device(device3_data, 2, device3_dio_map)

        test = Test(device1, device2, device3)
        uart_data = UART(device1_data)
        spi = SPI(device1_data)
        part = args.part

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
            if args.receive_packet:
                test.test_name = "receive_packet"
                if args.voltage_all:
                    run_test(test, writer, True, io_input=True)
                else:
                    run_test(test, writer, False, io_input=True)
            if args.uart_test:
                test.test_name = "uart"
                if args.voltage_all:
                    run_test(test, writer, True, uart=True, uart_data=uart_data, part=part)
                else:
                    run_test(test, writer, False, uart=True, uart_data=uart_data, part=part)
            if args.uart_reception_test:
                test.test_name = "uart_reception"
                if args.voltage_all:
                    run_test(test, writer, True, uart=True, uart_data=uart_data, part=part)
                else:
                    run_test(test, writer, False, uart=True, uart_data=uart_data, part=part)
            if args.uart_loopback_test:
                test.test_name = "uart_loopback"
                if args.voltage_all:
                    run_test(test, writer, True, uart=True, uart_data=uart_data, part=part)
                else:
                    run_test(test, writer, False, uart=True, uart_data=uart_data, part=part)
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
            if args.mem_test_dffram_half_word:
                test.passing_criteria = [1, 3, 3, 3]
                test.test_name = f"mem_dff_halfW"
                if args.voltage_all:
                    run_test(test, writer, True, sram="dff", mem=True)
                else:
                    run_test(test, writer, False, sram="dff", mem=True)
            if args.mem_test_sram_half_word:
                test.passing_criteria = [1, 3, 3, 3]
                test.test_name = f"mem_sram_halfW"
                if args.voltage_all:
                    run_test(test, writer, True, sram="sram", mem=True)
                else:
                    run_test(test, writer, False, sram="sram", mem=True)
            if args.mem_test_dffram_word:
                test.passing_criteria = [1, 3, 3, 3]
                test.test_name = f"mem_dff_W"
                if args.voltage_all:
                    run_test(test, writer, True, sram="dff", mem=True)
                else:
                    run_test(test, writer, False, sram="dff", mem=True)
            if args.mem_test_sram_word:
                test.passing_criteria = [1, 3, 3, 3]
                test.test_name = f"mem_sram_W"
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
                    run_test(test, writer, False, True, 37)
            if args.cpu_bitbang_36_o:
                test.passing_criteria = [1, 2, 5, 7, 3, 3, 3]
                test.test_name = "cpu_bitbang_36_o"
                if args.voltage_all:
                    run_test(test, writer, True, True, 36)
                else:
                    run_test(test, writer, False, True, 36)

            if args.all_mem:
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
                test.test_name = f"mem_dff_halfW"
                if args.voltage_all:
                    run_test(test, writer, True, sram="dff", mem=True)
                else:
                    run_test(test, writer, False, sram="dff", mem=True)
                test.test_name = f"mem_sram_halfW"
                if args.voltage_all:
                    run_test(test, writer, True, sram="sram", mem=True)
                else:
                    run_test(test, writer, False, sram="sram", mem=True)
                test.test_name = f"mem_dff_W"
                if args.voltage_all:
                    run_test(test, writer, True, sram="dff", mem=True)
                else:
                    run_test(test, writer, False, sram="dff", mem=True)
                test.test_name = f"mem_sram_W"
                if args.voltage_all:
                    run_test(test, writer, True, sram="sram", mem=True)
                else:
                    run_test(test, writer, False, sram="sram", mem=True)


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
                test.test_name = f"mem_dff_halfW"
                if args.voltage_all:
                    run_test(test, writer, True, sram="dff", mem=True)
                else:
                    run_test(test, writer, False, sram="dff", mem=True)
                test.test_name = f"mem_sram_halfW"
                if args.voltage_all:
                    run_test(test, writer, True, sram="sram", mem=True)
                else:
                    run_test(test, writer, False, sram="sram", mem=True)
                test.test_name = f"mem_dff_W"
                if args.voltage_all:
                    run_test(test, writer, True, sram="dff", mem=True)
                else:
                    run_test(test, writer, False, sram="dff", mem=True)
                test.test_name = f"mem_sram_W"
                if args.voltage_all:
                    run_test(test, writer, True, sram="sram", mem=True)
                else:
                    run_test(test, writer, False, sram="sram", mem=True)

        test.close_devices()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            test.close_devices()
            sys.exit(0)
        except SystemExit:
            test.close_devices()
            os._exit(0)
