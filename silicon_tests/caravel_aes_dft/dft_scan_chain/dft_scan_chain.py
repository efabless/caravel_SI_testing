from machine import Pin, Timer
import time
import random

tck_period_ms = 1

TCK_PIN = 10  # GPIO pin for TCK
TMS_PIN = 11  # GPIO pin for TMS
TDI_PIN = 12  # GPIO pin for TDI
TDO_PIN = 13  # GPIO pin for TDO
TRSTn_PIN = 14

# Initialize GPIO pins
TRSTn = Pin(TRSTn_PIN, Pin.OUT)  # TCK as output
TCK = Pin(TCK_PIN, Pin.OUT)  # TCK as output
TMS = Pin(TMS_PIN, Pin.OUT)  # TMS as output
TDI = Pin(TDI_PIN, Pin.OUT)  # TDI as output
TDO = Pin(TDO_PIN, Pin.IN)   # TDO as input

done = Pin( 8, Pin.OUT) 

TRSTn.value(0)
TCK.value(0)
TMS.value(0)
TDI.value(0)
TDO.value(0)
done.value(0)

toggle = 0
fall_edge = 0
tms_pattern=0b01100110
instruction=0b0011
# vector_length = 5600
vector_length = 3099
i =0
mismatch = 0

rand_vector = [random.randint(0, 1) for _ in range(vector_length)]
#rand_vector = [0 for i in range(vector_length)]
#rand_vector = [1, 0] * (vector_length // 2) + [0] * (vector_length % 2)
out_vector = []


print(rand_vector[:10])

# Keep the program running

while True:
    TCK.value(toggle)
    if (toggle == 0): # detect falling edge 
        fall_edge = fall_edge + 1
    
    # Reset DFT
    if (fall_edge == 2):
        TRSTn.value(0)
    if (fall_edge == 3):
        TRSTn.value(1)
    
    # Shift IR
    if(toggle==0 and fall_edge >= 4 and fall_edge <= 8): # shift the first 5 bits to TMS
        bit = tms_pattern & 1
        TMS.value(bit)
        tms_pattern = tms_pattern >> 1
    
    if(toggle==0 and fall_edge >= 9 and fall_edge <= 12): # At shift-IR: shift new instruction on tdi line
        bit = instruction & 1
        TDI.value(bit)
        if(fall_edge==12):
            TMS.value(tms_pattern & 1) # exit ir
            tms_pattern = tms_pattern >> 1
        instruction = instruction >> 1
    
    if(toggle==0 and fall_edge >= 13 and fall_edge <= 14):
        bit = tms_pattern & 1
        TMS.value(bit)
        tms_pattern = tms_pattern >> 1
    
    # enter shift-DR
    if (fall_edge==15):
       TMS.value(1)
    if (fall_edge==16):
       TMS.value(0)
    
    # Drive DFT
    if(toggle==0 and fall_edge >= 18 and fall_edge < (18 + vector_length)):
        TDI.value(rand_vector[i])
        i= i+1
        
    
    if(toggle==0 and fall_edge >= (18+vector_length) and fall_edge < (18 + 2*vector_length)):
        done.value(1)
        out_vector.append(TDO.value())
        
    toggle = ~ toggle
    
    if (fall_edge == (20 + 2*vector_length)):
        break
    

for i in range(vector_length):
    if(rand_vector[i]!=out_vector[i]):
        print (f"bit {i} mismatch; out ={out_vector[i]} expected = {rand_vector[i]}")
        mismatch = mismatch + 1

if (mismatch):
    print (f"Mismatches = {mismatch}")
else:
    print(f"Vectors Match!") 

