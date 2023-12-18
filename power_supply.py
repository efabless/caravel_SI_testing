from ctypes import *
from WF_SDK import *  # import instruments
from WF_SDK.dmm import *
import pyvisa
import time


class PowerSupply:
    def __init__(self, device_data):
        self.master_state = False  # master switch
        self.state = False  # digital/6V/positive supply state
        self.positive_state = False  # positive supply switch
        self.negative_state = False  # negative supply switch
        self.positive_voltage = 0  # positive supply voltage
        self.negative_voltage = 0  # negative supply voltage
        self.voltage = 0  # digital/positive supply voltage
        self.positive_current = 0  # positive supply current
        self.negative_current = 0  # negative supply current
        self.current = 0  # digital/6V supply current
        self.device_data = device_data
        self.rm = pyvisa.ResourceManager('@py')
        if self.rm.list_resources():
            self.external_power_supply = True
            self.inst = self.rm.open_resource('USB0::1155::30016::SPD3EFEX6R1193::0::INSTR')
            self.inst.query_delay = 0.1
        else:
            self.external_power_supply = False

    def switch(self):
        """
        turn the power supplies on/off
        parameters: - device data
                    - class containing supplies data:
                    - master_state
                    - state and/or positive_state and negative_state
                    - voltage and/or positive_voltage and negative_voltage
                    - current and/or positive_current and negative_current
        """
        if self.device_data.name == b"Analog Discovery 2" or self.device_data.name == b"Analog Discovery Studio":
            # switch variable supplies on AD2
            supply_state = self.state or self.positive_state
            supply_voltage = self.voltage + self.positive_voltage
            self._switch_variable_(supply_state, supply_voltage)

        elif self.device_data.name == b"Digital Discovery" or self.device_data.name == b"Analog Discovery Pro 3X50":
            # switch the digital supply on DD, or ADP3x50
            supply_state = self.master_state and (self.state
                                                  or self.positive_state)
            supply_voltage = self.voltage + self.positive_voltage
            self._switch_digital_(supply_state, supply_voltage)
        else:
            print(f"Warning: {self.device_data.name} powersupply is not handled")
        return

    def _switch_digital_(self, master_state, voltage):
        """
            turn the power supplies on/off
            parameters: - device data
                        - master switch - True = on, False = off
                        - supply voltage in Volts
        """
        # set supply voltage
        voltage = max(1.2, min(3.3, voltage))
        dwf.FDwfAnalogIOChannelNodeSet(self.device_data.handle,
                                       ctypes.c_int(0), ctypes.c_int(0),
                                       ctypes.c_double(voltage))

        # start/stop the supplies - master switch
        dwf.FDwfAnalogIOEnableSet(self.device_data.handle,
                                  ctypes.c_int(master_state))
        return

    def _switch_variable_(self, positive_state, positive_voltage):
        """
            turn the power supplies on/off
            parameters: - device data
                        - master switch - True = on, False = off
                        - positive supply switch - True = on, False = off
                        - negative supply switch - True = on, False = off
                        - positive supply voltage in Volts
                        - negative supply voltage in Volts
        """
        # set positive voltage
        positive_voltage = max(0, min(5, positive_voltage))
        dwf.FDwfAnalogIOChannelNodeSet(self.device_data.handle,
                                       ctypes.c_int(0), ctypes.c_int(1),
                                       ctypes.c_double(positive_voltage))

        # set negative voltage
        negative_voltage = max(-5, min(0, self.negative_voltage))
        dwf.FDwfAnalogIOChannelNodeSet(self.device_data.handle,
                                       ctypes.c_int(1), ctypes.c_int(1),
                                       ctypes.c_double(negative_voltage))

        # enable/disable the positive supply
        dwf.FDwfAnalogIOChannelNodeSet(self.device_data.handle,
                                       ctypes.c_int(0), ctypes.c_int(0),
                                       ctypes.c_double(positive_state))

        # enable the negative supply
        dwf.FDwfAnalogIOChannelNodeSet(self.device_data.handle,
                                       ctypes.c_int(1), ctypes.c_int(0),
                                       ctypes.c_double(self.negative_state))

        # start/stop the supplies - master switch
        dwf.FDwfAnalogIOEnableSet(self.device_data.handle,
                                  ctypes.c_int(self.master_state))
        return

    def turn_on(self):
        if self.external_power_supply:
            self.inst.write('CH1:VOLT 1.8')
            time.sleep(0.5)
            self.inst.write('OUTP CH1, ON')
            time.sleep(0.5)
            self.inst.write('CH2:VOLT 3.3')
            time.sleep(0.5)
            self.inst.write('OUTP CH2, ON')
            time.sleep(0.5)
        else:
            self.positive_voltage = 1.8
            self.negative_voltage = 0
            self.positive_state = True
            self.negative_state = True
            self.master_state = True
            self.switch()

    def turn_off(self):
        if self.external_power_supply:
            self.inst.write('OUTP CH1, OFF')
            time.sleep(0.5)
            self.inst.write('OUTP CH2, OFF')
            time.sleep(0.5)
        else:
            self.positive_voltage = 0
            self.negative_voltage = 0
            self.positive_state = False
            self.negative_state = False
            self.master_state = False
            self.switch()

    def set_voltage(self, voltage):
        if self.external_power_supply:
            self.inst.write(f'CH1:VOLT {voltage}')
            time.sleep(0.5)
            self.inst.write('OUTP CH1, ON')
            time.sleep(0.5)
            self.inst.write('CH2:VOLT 3.3')
            time.sleep(0.5)
            self.inst.write('OUTP CH2, ON')
            time.sleep(0.5)
        else:
            self.positive_voltage = voltage
            self.negative_voltage = 0
            self.positive_state = True
            self.negative_state = True
            self.master_state = True
            self.switch()
