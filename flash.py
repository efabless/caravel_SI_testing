#!/usr/bin/env python3

from pyftdi.ftdi import Ftdi
import time
import sys, os
from pyftdi.spi import SpiController
from array import array as Array
import binascii
from io import StringIO

# from machine import Pin, SPI, SoftSPI, sleep, I2C, SoftI2C

SR_WIP = 0b00000001  # Busy/Work-in-progress bit
SR_WEL = 0b00000010  # Write enable bit
SR_BP0 = 0b00000100  # bit protect #0
SR_BP1 = 0b00001000  # bit protect #1
SR_BP2 = 0b00010000  # bit protect #2
SR_BP3 = 0b00100000  # bit protect #3
SR_TBP = SR_BP3      # top-bottom protect bit
SR_SP = 0b01000000
SR_BPL = 0b10000000
SR_PROTECT_NONE = 0  # BP[0..2] = 0
SR_PROTECT_ALL = 0b00011100  # BP[0..2] = 1
SR_LOCK_PROTECT = SR_BPL
SR_UNLOCK_PROTECT = 0
SR_BPL_SHIFT = 2

CMD_READ_STATUS = 0x05  # Read status register
CMD_WRITE_ENABLE = 0x06  # Write enable
CMD_WRITE_DISABLE = 0x04  # Write disable
CMD_PROGRAM_PAGE = 0x02  # Write page
CMD_EWSR = 0x50  # Enable write status register
CMD_WRSR = 0x01  # Write status register
CMD_ERASE_SECTOR = 0x20
CMD_ERASE_BLOCK32 = 0x52
CMD_ERASE_BLOCK64 = 0xD8
# CMD_ERASE_CHIP = 0xC7
CMD_ERASE_CHIP = 0x60
CMD_RESET_CHIP = 0x99
CMD_JEDEC_DATA = 0x9f

CMD_READ_LO_SPEED = 0x03  # Read @ low speed
CMD_READ_HI_SPEED = 0x0B  # Read @ high speed
ADDRESS_WIDTH = 3

JEDEC_ID = 0xEF
DEVICES = {0x30: 'W25X', 0x40: 'W25Q'}
SIZES = {0x11: 1 << 17, 0x12: 1 << 18, 0x13: 1 << 19, 0x14: 1 << 20,
         0x15: 2 << 20, 0x16: 4 << 20, 0x17: 8 << 20, 0x18: 16 << 20}
SPI_FREQ_MAX = 104  # MHz
CMD_READ_UID = 0x4B
UID_LEN = 0x8  # 64 bits
READ_UID_WIDTH = 4  # 4 dummy bytes
TIMINGS = {'page': (0.0015, 0.003),  # 1.5/3 ms
           'subsector': (0.200, 0.200),  # 200/200 ms
           'sector': (1.0, 1.0),  # 1/1 s
           'bulk': (32, 64),  # seconds
           'lock': (0.05, 0.1),  # 50/100 ms
           'chip': (4, 11)}
# FEATURES = (SerialFlash.FEAT_SECTERASE |
#             SerialFlash.FEAT_SUBSECTERASE |
#             SerialFlash.FEAT_CHIPERASE)

CARAVEL_PASSTHRU = 0xC4
CARAVEL_STREAM_READ = 0x40
CARAVEL_STREAM_WRITE = 0x80
CARAVEL_REG_READ = 0x48
CARAVEL_REG_WRITE = 0x88


class Led:
    def __init__(self):
        self.led1 = Pin("B0")
        self.led2 = Pin("B7")
        self.led3 = Pin("B14")
        self.led1.on()
        self.led2.off()
        self.led3.on()

    def toggle(self):
        if self.led1.value():
            self.led1.off()
        else:
            self.led1.on()

        if self.led2.value():
            self.led2.off()
        else:
            self.led2.on()

    def off(self):
        self.led1.off()
        self.led2.off()
        self.led3.off()


# class SPI:
#     def __init__(self, enabled=True):
#
#         if enabled:
#             # self.cs = Pin('SPI4_CS', mode=Pin.OUT, value=1)
#             # self.sck = Pin('SPI4_SCK', mode=Pin.OUT, value=0)
#             # self.mosi = Pin('SPI4_MISO', mode=Pin.OUT)  # PF9 = IO[2] = caravel input
#             self.miso = Pin('SPI4_MISO', mode=Pin.IN)  # PF8 = IO[1] = caravel output
#             self.cs = Pin('SPI5_CS', mode=Pin.OUT, value=1)
#             self.sck = Pin('SPI5_SCK', mode=Pin.OUT, value=0)
#             self.mosi = Pin('SPI5_MISO', mode=Pin.OUT)  # PF9 = IO[2] = caravel input
#             # self.miso = Pin('SPI5_MOSI', mode=Pin.IN)  # PF8 = IO[1] = caravel output
#             # self.miso = Pin('A0', mode=Pin.IN)  # PF8 = IO[1] = caravel output
#             self.spi = SoftSPI(baudrate=400000, polarity=0, phase=0, sck=self.sck, mosi=self.mosi, miso=self.miso)
#         else:
#             self.cs = Pin('SPI5_CS', mode=Pin.IN, pull=None)
#             self.sck = Pin('SPI5_SCK', mode=Pin.IN, pull=None)
#             self.mosi = Pin('SPI5_MISO', mode=Pin.IN, pull=None)  # PF9 = IO[2] = caravel input
#             self.miso = Pin('SPI5_MOSI', mode=Pin.IN, pull=None)  # PF8 = IO[1] = caravel output
#             self.spi = None
#
#     def write(self, buf):
#         txdata = bytearray(buf)
#         self.cs.value(0)
#         self.spi.write(txdata)
#         self.cs.value(1)
#
#     def exchange(self, buf, n):
#
#         txdata = bytearray(buf)
#         txdata += '\0'*(n)
#         m = len(txdata)
#         rxdata = bytearray(m)
#
#         self.cs.value(0)
#         self.spi.write_readinto(txdata, rxdata)
#         self.cs.value(1)
#         return rxdata[m-n:m]
#
#     def get_status(self):
#         return int.from_bytes(self.exchange([CARAVEL_PASSTHRU, CMD_READ_STATUS], 1), 'big')
#
#     def is_busy(self):
#         return self.get_status() & SR_WIP
#
#     def report_status(self, jedec):
#         if jedec[0] == int('bf', 16):
#             print("changing cmd values...")
#             print("status reg_1 = {}".format(hex(self.get_status())))
#         else:
#             print("status reg_1 = {}".format(hex(self.get_status())))
#             status = self.exchange([CARAVEL_PASSTHRU, 0x35], 1)
#             print("status reg_2 = {}".format(hex(int.from_bytes(status, 'big'))))
#             # print("status = {}".format(hex(from_bytes(slave.exchange([CMD_READ_STATUS], 2)[1], byteorder='big'))))
#
#     def erase_page(self, page_addr):
#         addr = page_addr
#         print("Erasing page at {:04x}...".format(addr))
#         for x in range(4):
#             # print("Erasing 64kb block at {:04x}...".format(addr))
#             self.write([CARAVEL_PASSTHRU, CMD_WRITE_ENABLE])
#             wcmd = bytearray((CARAVEL_PASSTHRU, CMD_ERASE_BLOCK64, (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff))
#             self.write(wcmd)
#             addr += 64
#             while self.is_busy():
#                 time.sleep(0.1)

def get_devices():
    # This is roundabout but works. . .
    s = StringIO()
    Ftdi.show_devices(out=s)
    devlist = s.getvalue().splitlines()[1:-1]
    devices = []
    for dev in devlist:
        url = dev.split("(")[0].strip()
        name = "(" + dev.split("(")[1]
        if name == "(Single RS232-HS)":
            devices.append(url)
    if len(devices) == 0:
        print("Error:  No matching FTDI devices on USB bus!")
        sys.exit(1)
    elif len(devices) > 1:
        print("Error:  Too many matching FTDI devices on USB bus!")
        Ftdi.show_devices()
        sys.exit(1)
    else:
        print("Success: Found one matching FTDI device at " + devices[0])

    return devices


def get_status(device):
    return int.from_bytes(
        device.exchange([CARAVEL_PASSTHRU, CMD_READ_STATUS], 1), byteorder="big"
    )


def report_status(device, jedec):
    if jedec[0] == int("bf", 16):
        print("changing cmd values...")
        print("status reg_1 = {}".format(hex(get_status(device))))
    else:
        print("status reg_1 = {}".format(hex(get_status(device))))
        status = device.exchange([CARAVEL_PASSTHRU, 0x35], 1)
        print("status reg_2 = {}".format(hex(int.from_bytes(status, byteorder="big"))))
        # print("status = {}".format(hex(from_bytes(slave.exchange([CMD_READ_STATUS], 2)[1], byteorder='big'))))


def is_busy(device):
    return get_status(device) & SR_WIP


def check():
    led = Led()
    #led = Led(None)
    led.toggle()

    device_list = get_devices()
    spi = SpiController(cs_count=2)
    spi.configure(device_list[0])
    # slave = spi.get_port(cs=0, freq=12e6, mode=0)  # new caravel board
    slave = spi.get_port(cs=0, freq=1e6, mode=0)  # new caravel board

    # in some cases, you may need to comment or uncomment this line
    slave.write([CARAVEL_REG_WRITE, 0x0b, 0x01])
    # ------------

    print(" ")
    print("Caravel data:")
    mfg = slave.exchange([CARAVEL_STREAM_READ, 0x01], 2)
    # print("mfg = {}".format(binascii.hexlify(mfg)))
    print("   mfg        = {:04x}".format(int.from_bytes(mfg, 'big')))

    led.toggle()

    product = slave.exchange([CARAVEL_REG_READ, 0x03], 1)
    # print("product = {}".format(binascii.hexlify(product)))
    print("   product    = {:02x}".format(int.from_bytes(product, 'big')))

    led.toggle()

    data = slave.exchange([CARAVEL_STREAM_READ, 0x04], 4)
    # print("   project ID = {:08x}".format(int('{0:32b}'.format(int.from_bytes(data, 'big'))[::-1], 2)))
    #print("   project ID = {:08x}".format(int('{0:32b}'.format(int.from_bytes(data, 'big')), 2)))
    print("   project ID = {:08x}".format(int.from_bytes(data, 'big')))
    # if int.from_bytes(mfg, 'big') != 0x0456:
    #     exit(2)

    time.sleep(1.0)
    led.toggle()

    led.off()
    slave.__init__(enabled=False)


def erase(debug=False):
    # machine.reset()
    led = Led()
    # led = Led(None)
    led.toggle()

    device_list = get_devices()
    spi = SpiController(cs_count=2)
    spi.configure(device_list[0])
    # slave = spi.get_port(cs=0, freq=12e6, mode=0)  # new caravel board
    slave = spi.get_port(cs=0, freq=1e6, mode=0)  # new caravel board

    # in some cases, you may need to comment or uncomment this line
    slave.write([CARAVEL_REG_WRITE, 0x0b, 0x01])
    # ------------

    mfg = slave.exchange([CARAVEL_STREAM_READ, 0x01], 2)
    led.toggle()
    product = slave.exchange([CARAVEL_REG_READ, 0x03], 1)
    led.toggle()
    data = slave.exchange([CARAVEL_STREAM_READ, 0x04], 4)

    if debug:
        print(" ")
        print("Caravel data:")
        # print("mfg = {}".format(binascii.hexlify(mfg)))
        print("   mfg        = {:04x}".format(int.from_bytes(mfg,'big')))
        # print("product = {}".format(binascii.hexlify(product)))
        print("   product    = {:02x}".format(int.from_bytes(product, 'big')))
        #print("   project ID = {:08x}".format(int('{0:32b}'.format(int.from_bytes(data,'big'))[::-1], 2)))
        print("   project ID = {:08x}".format(int('{0:32b}'.format(int.from_bytes(data, 'big')), 2)))
    # if int.from_bytes(mfg, 'big') != 0x0456:
    #     exit(2)

    time.sleep(1.0)
    led.toggle()

    if debug:
        print(" ")
        print("Resetting Flash...")
    slave.write([CARAVEL_PASSTHRU, CMD_RESET_CHIP])

    if debug:
        print("status = 0x{:02x}".format(get_status(), '02x'))

    jedec = slave.exchange([CARAVEL_PASSTHRU, CMD_JEDEC_DATA], 3)
    if debug:
        print(" ")
        print("JEDEC = {}".format(binascii.hexlify(jedec)))

    if jedec[0:1] != bytes.fromhex('ef'):
    # if jedec[0:1] != bytes.fromhex('e6'):
        print("Winbond SRAM not found")
        sys.exit()

    if debug:
        print("Erasing chip...")
    slave.write([CARAVEL_PASSTHRU, CMD_WRITE_ENABLE])
    slave.write([CARAVEL_PASSTHRU, CMD_ERASE_CHIP])

    for i in range(15):
        time.sleep(0.5)
        led.toggle()

    while (is_busy()):
        time.sleep(0.5)
        led.toggle()

    if debug:
        print("done")
        print("status = {}".format(hex(get_status())))

    led.off()


def flash(file_path, debug=False):
    # machine.reset()

    led = Led()
    # led = Led(None)
    led.toggle()

    status_good = True

    device_list = get_devices()
    spi = SpiController(cs_count=2)
    spi.configure(device_list[0])
    # slave = spi.get_port(cs=0, freq=12e6, mode=0)  # new caravel board
    slave = spi.get_port(cs=0, freq=1e6, mode=0)  # new caravel board

    # in some cases, you may need to comment or uncomment this line
    slave.write([CARAVEL_REG_WRITE, 0x0b, 0x01])
    # ------------

    mfg = slave.exchange([CARAVEL_STREAM_READ, 0x01], 2)
    led.toggle()
    product = slave.exchange([CARAVEL_REG_READ, 0x03], 1)
    led.toggle()

    data = slave.exchange([CARAVEL_STREAM_READ, 0x04], 4)

    if debug:
        print(" ")
        print("Caravel data:")
        # print("mfg = {}".format(binascii.hexlify(mfg)))
        print("   mfg        = {:04x}".format(int.from_bytes(mfg,'big')))
        # print("product = {}".format(binascii.hexlify(product)))
        print("   product    = {:02x}".format(int.from_bytes(product, 'big')))
        #print("   project ID = {:08x}".format(int('{0:32b}'.format(int.from_bytes(data,'big'))[::-1], 2)))
        print("   project ID = {:08x}".format(int('{0:32b}'.format(int.from_bytes(data, 'big')), 2)))

    # if int.from_bytes(mfg, 'big') != 0x0456:
    #     exit(2)

    time.sleep(1.0)
    led.toggle()

    if debug:
        print(" ")
        print("Resetting Flash...")
    slave.write([CARAVEL_PASSTHRU, CMD_RESET_CHIP])

    # print("status = 0x{:02x}".format(slave.get_status(), '02x'))

    jedec = slave.exchange([CARAVEL_PASSTHRU, CMD_JEDEC_DATA], 3)
    if debug:
        print(" ")
        print("JEDEC = {}".format(binascii.hexlify(jedec)))

    if jedec[0:1] != bytes.fromhex('ef'):
    # if jedec[0:1] != bytes.fromhex('e6'):
        print("Winbond SRAM not found")
        sys.exit()

    buf = bytearray()
    addr = 0
    nbytes = 0
    total_bytes = 0

    with open(file_path, mode='r') as f:
        x = f.readline()
        while x != '':
            if x[0] == '@':
                addr = int(x[1:],16)
                if debug:
                    print('setting address to {:08x}'.format(addr))
            else:
                x = "".join(x.split())
                # print(x)
                #values = bytearray.fromhex(x[0:len(x)-1])
                values = bytearray.fromhex(x)
                buf[nbytes:nbytes] = values
                nbytes += len(values)
                # print(binascii.hexlify(values))

            x = f.readline()

            if nbytes >= 256 or (x != '' and x[0] == '@' and nbytes > 0):
                total_bytes += nbytes
                # print('\n----------------------\n')
                # print(binascii.hexlify(buf))
                # print("\ntotal_bytes = {}".format(total_bytes))

                slave.write([CARAVEL_PASSTHRU, CMD_WRITE_ENABLE])
                wcmd = bytearray((CARAVEL_PASSTHRU, CMD_PROGRAM_PAGE,(addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff))
                # wcmd = bytearray((CARAVEL_PASSTHRU, CMD_WRITE_ENABLE, CMD_PROGRAM_PAGE,(addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff))
                # print(binascii.hexlify(wcmd))
                # wcmd.extend(buf[0:255])
                wcmd.extend(buf)
                slave.write(wcmd)
                while (is_busy()):
                    time.sleep(0.1)

                if debug:
                    print("addr {}: flash page write successful (1)".format(hex(addr)))

                if nbytes > 256:
                    buf = buf[255:]
                    addr += 256
                    nbytes -= 256
                    if debug:
                        print("*** over 256 hit")
                else:
                    buf = bytearray()
                    addr += 256
                    nbytes =0

        if nbytes > 0:
            total_bytes += nbytes
            # print('\n----------------------\n')
            # print(binascii.hexlify(buf))
            # print("\nnbytes = {}".format(nbytes))

            slave.write([CARAVEL_PASSTHRU, CMD_WRITE_ENABLE])
            wcmd = bytearray((CARAVEL_PASSTHRU, CMD_PROGRAM_PAGE, (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff))
            # wcmd = bytearray((CARAVEL_PASSTHRU, CMD_WRITE_ENABLE, CMD_PROGRAM_PAGE, (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff))
            wcmd.extend(buf)
            slave.write(wcmd)
            while (is_busy()):
                time.sleep(0.1)

            if debug:
                print("addr {}: flash page write successful (2)".format(hex(addr)))

    if debug:
        print("\ntotal_bytes = {}".format(total_bytes))

    # slave.report_status(slave, jedec)

    # print("************************************")
    if debug:
        print("^^^^^^^^ verifying  ^^^^^^^^")
    # print("************************************")

    buf = bytearray()
    addr = 0
    nbytes = 0
    total_bytes = 0

    while (is_busy()):
        time.sleep(0.5)

    # slave.write([CARAVEL_REG_WRITE, 0x0b, 0x01])
    # slave.write([CARAVEL_REG_WRITE, 0x0b, 0x00])

    # slave.report_status(slave, jedec)

    with open(file_path, mode='r') as f:
        x = f.readline()
        while x != '':
            if x[0] == '@':
                addr = int(x[1:],16)
                if debug:
                    print('setting address to {:08x}'.format(addr))
            else:
                x = "".join(x.split())
                # print(x)
                # values = bytearray.fromhex(x[0:len(x)-1])
                values = bytearray.fromhex(x)
                buf[nbytes:nbytes] = values
                nbytes += len(values)
                # print(binascii.hexlify(values))

            x = f.readline()

            if nbytes >= 256 or (x != '' and x[0] == '@' and nbytes > 0):

                total_bytes += nbytes
                # print('\n----------------------\n')
                # print(binascii.hexlify(buf))
                # print("\ntotal_bytes = {}".format(total_bytes))

                read_cmd = bytearray((CARAVEL_PASSTHRU, CMD_READ_LO_SPEED,(addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff))
                # print(binascii.hexlify(read_cmd))
                buf2 = slave.exchange(read_cmd, nbytes)
                if buf == buf2:
                    if debug:
                        print("addr {}: read compare successful".format(hex(addr)))
                else:
                    status_good = False
                    if debug:
                        print("addr {}: *** read compare FAILED ***".format(hex(addr)))
                        print(binascii.hexlify(buf))
                        print("<----->")
                        print(binascii.hexlify(buf2))

                if nbytes > 256:
                    buf = buf[255:]
                    addr += 256
                    nbytes -= 256
                    if debug:
                        print("*** over 256 hit")
                else:
                    buf = bytearray()
                    addr += 256
                    nbytes =0

        if nbytes > 0:
            total_bytes += nbytes
            # print('\n----------------------\n')
            # print(binascii.hexlify(buf))
            # print("\nnbytes = {}".format(nbytes))

            read_cmd = bytearray((CARAVEL_PASSTHRU, CMD_READ_LO_SPEED, (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff))
            # print(binascii.hexlify(read_cmd))
            buf2 = slave.exchange(read_cmd, nbytes)
            if buf == buf2:
                if debug:
                    print("addr {}: read compare successful".format(hex(addr)))
            else:
                status_good = False
                if debug:
                    print("addr {}: *** read compare FAILED ***".format(hex(addr)))
                    print(binascii.hexlify(buf))
                    print("<----->")
                    print(binascii.hexlify(buf2))

    if debug:
        print("\ntotal_bytes = {}".format(total_bytes))

    slave.write([CARAVEL_REG_WRITE, 0x0b, 0x00])

    led.toggle()
    time.sleep(0.3)
    led.toggle()

    led.off()

    return status_good

