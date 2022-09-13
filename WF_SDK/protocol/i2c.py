""" PROTOCOL: I2C CONTROL FUNCTIONS: open, read, write, exchange, spy, close """

import ctypes                     # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators

# load the dynamic library, get constants path (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif platform.startswith("darwin"):
    # on macOS
    lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
    dwf = ctypes.cdll.LoadLibrary(lib_path)
    constants_path = sep + "Applications" + sep + "WaveForms.app" + sep + "Contents" + sep + "Resources" + sep + "SDK" + sep + "samples" + sep + "py"
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"

# import constants
path.append(constants_path)
import dwfconstants as constants

"""-----------------------------------------------------------------------"""

class state:
    """ stores the state of the instrument """
    on = False
    off = True

"""-----------------------------------------------------------------------"""

def open(device_data, sda, scl, clk_rate=100e03, stretching=True):
    """
        initializes I2C communication

        parameters: - device data
                    - sda (DIO line used for data)
                    - scl (DIO line used for clock)
                    - rate (clock frequency in Hz, default is 100KHz)
                    - stretching (enables/disables clock stretching)

        returns:    - error message or empty string
    """
    # reset the interface
    dwf.FDwfDigitalI2cReset(device_data.handle)

    # clock stretching
    if stretching:
        dwf.FDwfDigitalI2cStretchSet(device_data.handle, ctypes.c_int(1))
    else:
        dwf.FDwfDigitalI2cStretchSet(device_data.handle, ctypes.c_int(0))

    # set clock frequency
    dwf.FDwfDigitalI2cRateSet(device_data.handle, ctypes.c_double(clk_rate))

    #  set communication lines
    dwf.FDwfDigitalI2cSclSet(device_data.handle, ctypes.c_int(scl))
    dwf.FDwfDigitalI2cSdaSet(device_data.handle, ctypes.c_int(sda))

    # check bus
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cClear(device_data.handle, ctypes.byref(nak))
    if nak.value == 0:
        return "Error: I2C bus lockup"

    # write 0 bytes
    dwf.FDwfDigitalI2cWrite(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), ctypes.byref(nak))
    if nak.value != 0:
        return "NAK: index " + str(nak.value)
    
    state.on = True
    state.off = False
    return ""

"""-----------------------------------------------------------------------"""

def write(device_data, data, address):
    """
        send data through I2C
        
        parameters: - device data
                    - data of type string, int, or list of characters/integers
                    - address (8-bit address of the slave device)
                    
        returns:    - error message or empty string
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = bytes(data, "utf-8")
    buffer = (ctypes.c_ubyte * len(data))()
    for index in range(0, len(buffer)):
        buffer[index] = ctypes.c_ubyte(data[index])

    # send
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cWrite(device_data.handle, ctypes.c_int(address << 1), buffer, ctypes.c_int(ctypes.sizeof(buffer)), ctypes.byref(nak))

    # check for not acknowledged
    if nak.value != 0:
        return "NAK: index " + str(nak.value)
    
    return ""

"""-----------------------------------------------------------------------"""

def read(device_data, count, address):
    """
        receives data from I2C
        
        parameters: - device data
                    - count (number of bytes to receive)
                    - address (8-bit address of the slave device)
        
        return:     - integer list containing the received bytes
                    - error message or empty string
    """
    # create buffer to store data
    buffer = (ctypes.c_ubyte * count)()

    # receive
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cRead(device_data.handle, ctypes.c_int(address << 1), buffer, ctypes.c_int(count), ctypes.byref(nak))

    # decode data
    data = [int(element) for element in buffer]

    # check for not acknowledged
    if nak.value != 0:
        return data, "NAK: index " + str(nak.value)
    
    return data, ""

"""-----------------------------------------------------------------------"""

def exchange(device_data, data, count, address):
    """
        sends and receives data using the I2C interface
        
        parameters: - device data
                    - data of type string, int, or list of characters/integers
                    - count (number of bytes to receive)
                    - address (8-bit address of the slave device)
        
        return:     - integer list containing the received bytes
                    - error message or empty string
    """
    # create buffer to store data
    buffer = (ctypes.c_ubyte * count)()

    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = bytes(data, "utf-8")
    tx_buffer = (ctypes.c_ubyte * len(data))()
    for index in range(0, len(tx_buffer)):
        tx_buffer[index] = ctypes.c_ubyte(data[index])

    # send and receive
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cWriteRead(device_data.handle, ctypes.c_int(address << 1), tx_buffer, ctypes.c_int(ctypes.sizeof(tx_buffer)), buffer, ctypes.c_int(count), ctypes.byref(nak))

    # decode data
    rec_data = [int(element) for element in buffer]

    # check for not acknowledged
    if nak.value != 0:
        return rec_data, "NAK: index " + str(nak.value)
    
    return rec_data, ""

"""-----------------------------------------------------------------------"""

def spy(device_data, count = 16):
    """
        receives data from I2C
        
        parameters: - device data
                    - count (number of bytes to receive), default is 16
        
        return:     - class containing the received data: start, address, direction, message, stop
                    - error message or empty string
    """
    # variable to store the errors
    error = ""

    # variable to store the data
    class message:
        start = ""
        address = 0
        direction = ""
        data = []
        stop = ""

    # start the interfcae
    dwf.FDwfDigitalI2cSpyStart(device_data.handle)

    # read data
    start = ctypes.c_int()
    stop = ctypes.c_int()
    data = (ctypes.c_ubyte * count)()
    count = ctypes.c_int(count)
    nak = ctypes.c_int()
    if dwf.FDwfDigitalI2cSpyStatus(device_data.handle, ctypes.byref(start), ctypes.byref(stop), ctypes.byref(data), ctypes.byref(count), ctypes.byref(nak)) == 0:
        error = "Communication with the device failed."
    
    # decode data
    if start.value != 0:

        # start condition
        if start.value == 1:
            message.start = "Start"
        elif start.value == 2:
            message.start = "Restart"

        # get address
        message.address = hex(data[0] >> 1)

        # decide message direction
        if data[0] & 1 == 0:
            message.direction = "Write"
        else:
            message.direction = "Read"
        
        # get message
        message.data = [int(element) for element in data]

        if stop.value != 0:
            message.stop = "Stop"

    # check for not acknowledged
    if nak.value != 0 and error == "":
        error = "NAK: index " + str(nak.value)
    
    return message, error

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the i2c interface
    """
    dwf.FDwfDigitalI2cReset(device_data.handle)
    state.on = False
    state.off = True
    return
