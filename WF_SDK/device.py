""" DEVICE CONTROL FUNCTIONS: open, check_error, close, temperature """

"""
import ctypes                            # import the C compatible data types
import WF_SDK.dwfconstants as constants  # import every constant
from sys import platform                 # this is needed to check the OS type

# load the dynamic library (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
elif platform.startswith("darwin"):
    # on macOS
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

"""

"""-----------------------------------------------------------------------"""

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

"""
def open():
    '''
        open the first available device
    '''
    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int()

    # connect to the first available device
    dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(device_handle))
    data.handle = device_handle
    data.name = device_name
    return data
"""

"""-----------------------------------------------------------------------"""

class data:
    """ stores the device handle and the device name """
    handle = ctypes.c_int(0)
    name = ""
    serial_number = ""
    version = ""
    class analog:
        class input:
            channel_count = 0
            max_buffer_size = 0
            max_resolution = 0
            min_range = 0
            max_range = 0
            steps_range = 0
            min_offset = 0
            max_offset = 0
            steps_offset = 0
        class output:
            channel_count = 0
            node_count = []
            node_type = []
            max_buffer_size = []
            min_amplitude = []
            max_amplitude = []
            min_offset = []
            max_offset = []
            min_frequency = []
            max_frequency = []
        class IO:
            channel_count = 0
            node_count = []
            channel_name = []
            channel_label = []
            node_name = []
            node_unit = []
            min_set_range = []
            max_set_range = []
            min_read_range = []
            max_read_range = []
            set_steps = []
            read_steps = []
    class digital:
        class input:
            channel_count = 0
            max_buffer_size = 0
        class output:
            channel_count = 0
            max_buffer_size = 0

class state:
    """ stores the state of the device """
    connected = False
    disconnected = True
    error = ""

"""-----------------------------------------------------------------------"""

def open_devices(config=0, debug=False):
    # declare string variables
    devicename = ctypes.create_string_buffer(64)
    serialnum = ctypes.create_string_buffer(16)
    cDevice = ctypes.c_int()
    hdwf = ctypes.c_int()
    # enumerate connected devices
    dwf.FDwfEnum(ctypes.c_int(0), ctypes.byref(cDevice))
    if debug:
        print("Number of Devices: "+str(cDevice.value))
    # open devices
    datas = []
    for iDevice in range(0, cDevice.value):
        dwf.FDwfEnumDeviceName(ctypes.c_int(iDevice), devicename)
        dwf.FDwfEnumSN(ctypes.c_int(iDevice), serialnum)
        if debug:
            print("------------------------------")
            print("Device "+str(iDevice+1)+" : ")
            print("\t" + str(devicename.value))
            print("\t" + str(serialnum.value))
        dwf.FDwfDeviceConfigOpen(ctypes.c_int(iDevice), ctypes.c_int(config), ctypes.byref(hdwf))
        device_data = data()
        device_data.handle = hdwf.value
        device_data.name = devicename.value
        device_data.serial_number = serialnum.value
        device_data = __get_info__(device_data)
        state.connected = True
        state.disconnected = False
        datas.append(device_data)
    return datas

def open(device=None, config=0):
    """
        open a specific device

        parameters: - device type: None (first device), "Analog Discovery", "Analog Discovery 2", "Analog Discovery Studio", "Digital Discovery"
                                   "Analog Discovery Pro 3X50" and "Analog Discovery Pro 5250"
                    - configuration
    
        returns:    - device data
    """
    device_names = [("Analog Discovery", constants.devidDiscovery), ("Analog Discovery 2", constants.devidDiscovery2),
                    ("Analog Discovery Studio", constants.devidDiscovery2), ("Digital Discovery", constants.devidDDiscovery),
                    ("Analog Discovery Pro 3X50", constants.devidADP3X50), ("Analog Discovery Pro 5250", constants.devidADP5250)]
    
    # decode device names
    device_type = constants.enumfilterAll
    for pair in device_names:
        if pair[0] == device:
            device_type = pair[1]
            break

    # count devices
    device_count = ctypes.c_int()
    dwf.FDwfEnum(device_type, ctypes.byref(device_count))

    # check for connected devices
    if device_count.value <= 0:
        if device_type.value == 0:
            state.error = "Error: There are no connected devices"
        else:
            state.error = "Error: There is no " + device + " connected"
        print(state.error)
        quit()

    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int(0)

    # connect to the first available device
    index = 0
    while device_handle.value == 0 and index < device_count.value:
        dwf.FDwfDeviceConfigOpen(ctypes.c_int(index), ctypes.c_int(config), ctypes.byref(device_handle))
        index += 1  # increment the index and try again if the device is busy

    # check connected device type
    device_name = ""
    if device_handle.value != 0:
        device_id = ctypes.c_int()
        device_rev = ctypes.c_int()
        dwf.FDwfEnumDeviceType(ctypes.c_int(index - 1), ctypes.byref(device_id), ctypes.byref(device_rev))

        # decode device id
        for pair in device_names:
            if pair[1].value == device_id.value:
                device_name = pair[0]
                break
    
    global data
    data.handle = device_handle
    data.name = device_name
    data = __get_info__(data)
    state.connected = True
    state.disconnected = False
    return data

"""-----------------------------------------------------------------------"""

def check_error(device_data):
    """
        check for connection errors
    """
    # if the device handle is empty after a connection attempt
    if device_data.handle.value == constants.hdwfNone.value:
        # check for errors
        err_nr = ctypes.c_int()            # variable for error number
        dwf.FDwfGetLastError(ctypes.byref(err_nr))  # get error number
    
        # if there is an error
        if err_nr != constants.dwfercNoErc:
            # display it and quit
            err_msg = ctypes.create_string_buffer(512)        # variable for the error message
            dwf.FDwfGetLastErrorMsg(err_msg)                  # get the error message
            err_msg = err_msg.value.decode("ascii")           # format the message
            print("Error: " + err_msg)                        # display error message
            state.error = err_msg
            state.connected = False
            state.disconnected = True
            quit()                                            # exit the program
    return

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        close a specific device
    """
    dwf.FDwfDeviceClose(device_data.handle)
    data.handle = ctypes.c_int(0)
    data.name = ""
    state.connected = False
    state.disconnected = True
    return

"""-----------------------------------------------------------------------"""

def temperature(device_data):
    """
        return the board temperature
    """
    channel = -1
    node = -1
    # find the system monitor
    for channel_index in range(device_data.analog.IO.channel_count):
        if device_data.analog.IO.channel_label[channel_index] == "System":
            channel = channel_index
            break
    if channel < 0:
        return 0
    
    # find the temperature node
    for node_index in range(device_data.analog.IO.node_count[channel]):
        if device_data.analog.IO.node_name[channel][node_index] == "Temp":
            node = node_index
            break
    if node < 0:
        return 0
    
    # read the temperature
    dwf.FDwfAnalogIOStatus(device_data.handle)
    temperature = ctypes.c_double()
    dwf.FDwfAnalogIOChannelNodeStatus(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), ctypes.byref(temperature))
    return temperature.value

"""-----------------------------------------------------------------------"""

def __get_info__(device_data):
    """
        get and return device information
    """
    # check WaveForms version
    version = ctypes.create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    device_data.version = str(version.value)[2:-1]

    # define temporal variables
    temp1 = ctypes.c_int()
    temp2 = ctypes.c_int()
    temp3 = ctypes.c_int()

    # analog input information
    # channel count
    dwf.FDwfAnalogInChannelCount(device_data.handle, ctypes.byref(temp1))
    device_data.analog.input.channel_count = temp1.value
    # buffer size
    dwf.FDwfAnalogInBufferSizeInfo(device_data.handle, 0, ctypes.byref(temp1))
    device_data.analog.input.max_buffer_size = temp1.value
    # ADC resolution
    dwf.FDwfAnalogInBitsInfo(device_data.handle, ctypes.byref(temp1))
    device_data.analog.input.max_resolution = temp1.value
    # range information
    temp1 = ctypes.c_double()
    temp2 = ctypes.c_double()
    temp3 = ctypes.c_double()
    dwf.FDwfAnalogInChannelRangeInfo(device_data.handle, ctypes.byref(temp1), ctypes.byref(temp2), ctypes.byref(temp3))
    device_data.analog.input.min_range = temp1.value
    device_data.analog.input.max_range = temp2.value
    device_data.analog.input.steps_range = int(temp3.value)
    # offset information
    dwf.FDwfAnalogInChannelOffsetInfo(device_data.handle, ctypes.byref(temp1), ctypes.byref(temp2), ctypes.byref(temp3))
    device_data.analog.input.min_offset = temp1.value
    device_data.analog.input.max_offset = temp2.value
    device_data.analog.input.steps_offset = int(temp3.value)

    # analog output information
    temp1 = ctypes.c_int()
    dwf.FDwfAnalogOutCount(device_data.handle, ctypes.byref(temp1))
    device_data.analog.output.channel_count = temp1.value
    for channel_index in range(device_data.analog.output.channel_count):
        # check node types and node count
        temp1 = ctypes.c_int()
        dwf.FDwfAnalogOutNodeInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.byref(temp1))
        templist = []
        for node_index in range(3):
            if ((1 << node_index) & int(temp1.value)) == 0:
                continue
            elif node_index == constants.AnalogOutNodeCarrier.value:
                templist.append("carrier")
            elif node_index == constants.AnalogOutNodeFM.value:
                templist.append("FM")
            elif node_index == constants.AnalogOutNodeAM.value:
                templist.append("AM")
        device_data.analog.output.node_type.append(templist)
        device_data.analog.output.node_count.append(len(templist))
        # buffer size
        templist = []
        for node_index in range(device_data.analog.output.node_count[channel_index]):
            dwf.FDwfAnalogOutNodeDataInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.c_int(node_index), 0, ctypes.byref(temp1))
            templist.append(temp1.value)
        device_data.analog.output.max_buffer_size.append(templist)
        # amplitude information
        templist1 = []
        templist2 = []
        temp1 = ctypes.c_double()
        temp2 = ctypes.c_double()
        for node_index in range(device_data.analog.output.node_count[channel_index]):
            dwf.FDwfAnalogOutNodeAmplitudeInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(temp1), ctypes.byref(temp2))
            templist1.append(temp1.value)
            templist2.append(temp2.value)
        device_data.analog.output.min_amplitude.append(templist1)
        device_data.analog.output.max_amplitude.append(templist2)
        # offset information
        templist1 = []
        templist2 = []
        for node_index in range(device_data.analog.output.node_count[channel_index]):
            dwf.FDwfAnalogOutNodeOffsetInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(temp1), ctypes.byref(temp2))
            templist1.append(temp1.value)
            templist2.append(temp2.value)
        device_data.analog.output.min_offset.append(templist1)
        device_data.analog.output.max_offset.append(templist2)
        # frequency information
        templist1 = []
        templist2 = []
        for node_index in range(device_data.analog.output.node_count[channel_index]):
            dwf.FDwfAnalogOutNodeFrequencyInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(temp1), ctypes.byref(temp2))
            templist1.append(temp1.value)
            templist2.append(temp2.value)
        device_data.analog.output.min_frequency.append(templist1)
        device_data.analog.output.max_frequency.append(templist2)

    # analog IO information
    # channel count
    temp1 = ctypes.c_int()
    dwf.FDwfAnalogIOChannelCount(device_data.handle, ctypes.byref(temp1))
    device_data.analog.IO.channel_count = temp1.value
    for channel_index in range(device_data.analog.IO.channel_count):
        # channel names and labels
        temp1 = ctypes.create_string_buffer(256)
        temp2 = ctypes.create_string_buffer(256)
        dwf.FDwfAnalogIOChannelName(device_data.handle, ctypes.c_int(channel_index), temp1, temp2)
        device_data.analog.IO.channel_name.append(str(temp1.value)[2:-1])
        device_data.analog.IO.channel_label.append(str(temp2.value)[2:-1])
        # check node count
        temp1 = ctypes.c_int()
        dwf.FDwfAnalogIOChannelInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.byref(temp1))
        device_data.analog.IO.node_count.append(temp1.value)
        # node names and units
        templist1 = []
        templist2 = []
        for node_index in range(device_data.analog.IO.node_count[channel_index]):
            temp1 = ctypes.create_string_buffer(256)
            temp2 = ctypes.create_string_buffer(256)
            dwf.FDwfAnalogIOChannelNodeName(device_data.handle, ctypes.c_int(channel_index), ctypes.c_int(node_index), temp1, temp2)
            templist1.append(str(temp1.value)[2:-1])
            templist2.append(str(temp2.value)[2:-1])
        device_data.analog.IO.node_name.append(templist1)
        device_data.analog.IO.node_unit.append(templist2)
        # node write info
        templist1 = []
        templist2 = []
        templist3 = []
        temp1 = ctypes.c_double()
        temp2 = ctypes.c_double()
        temp3 = ctypes.c_int()
        for node_index in range(device_data.analog.IO.node_count[channel_index]):
            dwf.FDwfAnalogIOChannelNodeSetInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(temp1), ctypes.byref(temp2), ctypes.byref(temp3))
            templist1.append(temp1.value)
            templist2.append(temp2.value)
            templist3.append(temp3.value)
        device_data.analog.IO.min_set_range.append(templist1)
        device_data.analog.IO.max_set_range.append(templist2)
        device_data.analog.IO.set_steps.append(templist3)
        # node read info
        templist1 = []
        templist2 = []
        templist3 = []
        for node_index in range(device_data.analog.IO.node_count[channel_index]):
            dwf.FDwfAnalogIOChannelNodeStatusInfo(device_data.handle, ctypes.c_int(channel_index), ctypes.c_int(node_index), ctypes.byref(temp1), ctypes.byref(temp2), ctypes.byref(temp3))
            templist1.append(temp1.value)
            templist2.append(temp2.value)
            templist3.append(temp3.value)
        device_data.analog.IO.min_read_range.append(templist1)
        device_data.analog.IO.max_read_range.append(templist2)
        device_data.analog.IO.read_steps.append(templist3)

    # digital input information
    # channel count
    temp1 = ctypes.c_int()
    dwf.FDwfDigitalInBitsInfo(device_data.handle, ctypes.byref(temp1))
    device_data.digital.input.channel_count = temp1.value
    # buffer size
    dwf.FDwfDigitalInBufferSizeInfo(device_data.handle, ctypes.byref(temp1))
    device_data.digital.input.max_buffer_size = temp1.value

    # digital output information
    # channel count
    dwf.FDwfDigitalOutCount(device_data.handle, ctypes.byref(temp1))
    device_data.digital.output.channel_count = temp1.value
    # buffer size
    dwf.FDwfDigitalOutDataInfo(device_data.handle, ctypes.c_int(0), ctypes.byref(temp1))
    device_data.digital.output.max_buffer_size = temp1.value

    return device_data
