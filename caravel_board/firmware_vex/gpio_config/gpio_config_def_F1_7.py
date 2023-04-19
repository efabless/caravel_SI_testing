#!/bin/env python3
#
# gpio_config_def.py ---  Provides definition of hold violations between blocks for MPW-2
#
# Input:   Hold violations between each GPIO and desired
# Output:  Configuration bitstreams for upper and lower gpio chains
#

from bitstring import Bits, BitArray, BitStream
from enum import Enum

#############
##  Configuration file for MPW-2 part F1-7
#############

# number of IO in the configuration stream for each chain
NUM_IO = 19

# defines these cases of hold violations
H_NONE = 0
H_DEPENDENT = 1
H_INDEPENDENT = 2
H_SPECIAL = 3

# gpio names and incoming hold violation types

gpio_h = [
    ['IO[37]', H_NONE],    # <<<< this must be set to NONE
    ['IO[36]', H_INDEPENDENT],
    ['IO[35]', H_INDEPENDENT],
    ['IO[34]', H_INDEPENDENT],
    ['IO[33]', H_INDEPENDENT],
    ['IO[32]', H_INDEPENDENT],
    ['IO[31]', H_INDEPENDENT],
    ['IO[30]', H_INDEPENDENT],
    ['IO[29]', H_DEPENDENT],
    ['IO[28]', H_INDEPENDENT],
    ['IO[27]', H_DEPENDENT],
    ['IO[26]', H_DEPENDENT],
    ['IO[25]', H_INDEPENDENT],
    ['IO[24]', H_INDEPENDENT],
    ['IO[23]', H_INDEPENDENT],
    ['IO[22]', H_INDEPENDENT],
    ['IO[21]', H_INDEPENDENT],
    ['IO[20]', H_INDEPENDENT],
    ['IO[19]', H_INDEPENDENT],
]

del gpio_h[NUM_IO:]

gpio_l = [
    ['IO[00]', H_NONE],    # <<<< this must be set to NONE
    ['IO[01]', H_DEPENDENT],
    ['IO[02]', H_DEPENDENT],
    ['IO[03]', H_INDEPENDENT],
    ['IO[04]', H_INDEPENDENT],
    ['IO[05]', H_DEPENDENT],
    ['IO[06]', H_DEPENDENT],
    ['IO[07]', H_INDEPENDENT],
    ['IO[08]', H_DEPENDENT],
    ['IO[09]', H_DEPENDENT],
    ['IO[10]', H_INDEPENDENT],
    ['IO[11]', H_DEPENDENT],
    ['IO[12]', H_DEPENDENT],
    ['IO[13]', H_INDEPENDENT],
    ['IO[14]', H_INDEPENDENT],
    ['IO[15]', H_INDEPENDENT],
    ['IO[16]', H_INDEPENDENT],
    ['IO[17]', H_INDEPENDENT],
    ['IO[18]', H_INDEPENDENT],
]

del gpio_l[NUM_IO:]

# defines these values for IO configurations
C_MGMT_OUT = 0
C_MGMT_IN = 1
C_USER_BIDIR = 2
C_DISABLE = 3
C_ALL_ONES = 4

config_h = [
    C_MGMT_OUT,  #37
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,  #30
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,  #27
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
]

del config_h[NUM_IO:]

config_l = [
    C_DISABLE,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
    C_MGMT_OUT,
]

del config_l[NUM_IO:]

