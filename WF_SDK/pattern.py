""" PATTERN GENERATOR CONTROL FUNCTIONS: generate, close, enable, disable """

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
    channel = [False for _ in range(16)]

"""-----------------------------------------------------------------------"""

class function:
    """ function names """
    pulse = constants.DwfDigitalOutTypePulse
    custom = constants.DwfDigitalOutTypeCustom
    random = constants.DwfDigitalOutTypeRandom

"""-----------------------------------------------------------------------"""

class trigger_source:
    """ trigger source names """
    none = constants.trigsrcNone
    analog = constants.trigsrcDetectorAnalogIn
    digital = constants.trigsrcDetectorDigitalIn
    external = [None, constants.trigsrcExternal1, constants.trigsrcExternal2, constants.trigsrcExternal3, constants.trigsrcExternal4]

"""-----------------------------------------------------------------------"""

class idle_state:
    """ channel idle states """
    initial = constants.DwfDigitalOutIdleInit
    high = constants.DwfDigitalOutIdleHigh
    low = constants.DwfDigitalOutIdleLow
    high_impedance = constants.DwfDigitalOutIdleZet

"""-----------------------------------------------------------------------"""

def generate(device_data, channel, function, frequency, duty_cycle=50, data=[], wait=0, repeat=0, run_time=0, idle=idle_state.initial, trigger_enabled=False, trigger_source=trigger_source.none, trigger_edge_rising=True):
    """
        generate a logic signal
        
        parameters: - channel - the selected DIO line number
                    - function - possible: pulse, custom, random
                    - frequency in Hz
                    - duty cycle in percentage, used only if function = pulse, default is 50%
                    - data list, used only if function = custom, default is empty
                    - wait time in seconds, default is 0 seconds
                    - repeat count, default is infinite (0)
                    - run_time: in seconds, 0=infinite, "auto"=auto
                    - idle - possible: initial, high, low, high_impedance, default = initial
                    - trigger_enabled - include/exclude trigger from repeat cycle
                    - trigger_source - possible: none, analog, digital, external[1-4]
                    - trigger_edge_rising - True means rising, False means falling, None means either, default is rising
    """
    # get internal clock frequency
    internal_frequency = ctypes.c_double()
    dwf.FDwfDigitalOutInternalClockInfo(device_data.handle, ctypes.byref(internal_frequency))
    
    # get counter value range
    counter_limit = ctypes.c_uint()
    dwf.FDwfDigitalOutCounterInfo(device_data.handle, ctypes.c_int(channel), ctypes.c_int(0), ctypes.byref(counter_limit))
    
    # calculate the divider for the given signal frequency
    if function == constants.DwfDigitalOutTypePulse:
        divider = int(-(-(internal_frequency.value / frequency) // counter_limit.value))
    else:
        divider = int(internal_frequency.value / frequency)
    
    # enable the respective channel
    dwf.FDwfDigitalOutEnableSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(1))
    
    # set output type
    dwf.FDwfDigitalOutTypeSet(device_data.handle, ctypes.c_int(channel), function)
    
    # set frequency
    dwf.FDwfDigitalOutDividerSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(divider))

    # set idle state
    dwf.FDwfDigitalOutIdleSet(device_data.handle, ctypes.c_int(channel), idle)

    # set PWM signal duty cycle
    if function == constants.DwfDigitalOutTypePulse:
        # calculate counter steps to get the required frequency
        steps = int(round(internal_frequency.value / frequency / divider))
        # calculate steps for low and high parts of the period
        high_steps = int(steps * duty_cycle / 100)
        low_steps = int(steps - high_steps)
        dwf.FDwfDigitalOutCounterSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(low_steps), ctypes.c_int(high_steps))
    
    # load custom signal data
    elif function == constants.DwfDigitalOutTypeCustom:
        # format data
        buffer = (ctypes.c_ubyte * ((len(data) + 7) >> 3))(0)
        for index in range(len(data)):
            if data[index] != 0:
                buffer[index >> 3] |= 1 << (index & 7)
    
        # load data
        dwf.FDwfDigitalOutDataSet(device_data.handle, ctypes.c_int(channel), ctypes.byref(buffer), ctypes.c_int(len(data)))
    
    # calculate run length
    if run_time == "auto":
        run_time = len(data) / frequency
    
    # set wait time
    dwf.FDwfDigitalOutWaitSet(device_data.handle, ctypes.c_double(wait))
    
    # set repeat count
    dwf.FDwfDigitalOutRepeatSet(device_data.handle, ctypes.c_int(repeat))
    
    # set run length
    dwf.FDwfDigitalOutRunSet(device_data.handle, ctypes.c_double(run_time))

    # enable triggering
    dwf.FDwfDigitalOutRepeatTriggerSet(device_data.handle, ctypes.c_int(trigger_enabled))
    
    if trigger_enabled:
        # set trigger source
        dwf.FDwfDigitalOutTriggerSourceSet(device_data.handle, trigger_source)
    
        # set trigger slope
        if trigger_edge_rising == True:
            # rising edge
            dwf.FDwfDigitalOutTriggerSlopeSet(device_data.handle, constants.DwfTriggerSlopeRise)
        elif trigger_edge_rising == False:
            # falling edge
            dwf.FDwfDigitalOutTriggerSlopeSet(device_data.handle, constants.DwfTriggerSlopeFall)
        elif trigger_edge_rising == None:
            # either edge
            dwf.FDwfDigitalOutTriggerSlopeSet(device_data.handle, constants.DwfTriggerSlopeEither)

    # start generating the signal
    dwf.FDwfDigitalOutConfigure(device_data.handle, ctypes.c_int(True))
    state.on = True
    state.off = False
    state.channel[channel] = True
    return

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the instrument
    """
    dwf.FDwfDigitalOutReset(device_data.handle)
    state.on = False
    state.off = True
    state.channel = [False for _ in range(16)]
    return

"""-----------------------------------------------------------------------"""

def enable(device_data, channel):
    """ enables a digital output channel """
    dwf.FDwfDigitalOutEnableSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(1))
    dwf.FDwfDigitalOutConfigure(device_data.handle, ctypes.c_int(True))
    state.on = True
    state.off = False
    state.channel[channel] = True
    return

"""-----------------------------------------------------------------------"""

def disable(device_data, channel):
    """ disables a digital output channel """
    dwf.FDwfDigitalOutEnableSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(0))
    dwf.FDwfDigitalOutConfigure(device_data.handle, ctypes.c_int(True))
    state.channel[channel] = False
    return
