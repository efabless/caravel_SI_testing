from machine import Pin, Timer
import time
import array

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

RSTn = Pin( 8, Pin.OUT) 

TRSTn.value(0)
TCK.value(0)
TMS.value(0)
TDI.value(0)
TDO.value(0)
RSTn.value(0)

toggle = 0
fall_edge = 0
tms_pattern=0b01100110
instruction=0b0011


in_vector_size = 3066
out_vector_size = 3028
in_vector_bytes_num = 384
out_vector_bytes_num = 379
total_vectors=146
in_vec_file_path = "aes_in_vectors.bin"
golden_vec_file_path = "aes_out_vectors.bin"
    
in_vec_index = 0
out_vec_index =0
mismatch=0


in_vector = array.array('B', [0] * in_vector_size)
out_vector = array.array('B', [0] * out_vector_size)
golden_vector = array.array('B', [0] * out_vector_size)






def bytes_to_bit_array(byte_data, bit_array):
    """
    Converts bytes to bits and overwrites them in an array.array at specific indices.
    :param byte_data: Bytes to convert to bits.
    :param bit_array: array.array to store the bits.
    """
    current_index = 0  # Initialize the index to start overwriting from the beginning of the array
    for byte in byte_data:
        # Convert the byte to an 8-bit binary string and overwrite each bit in the array
        for bit in f"{byte:08b}":
            if (current_index<len(bit_array)):
                bit_array[current_index] = int(bit)  # Overwrite the bit at the current index
                current_index += 1  # Increment the index after overwriting each bit

def reverse_array(arr):
    """
    Reverses an array.array in place.
    :param arr: array.array to reverse.
    """
    left = 0
    right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr


try:
    with open(in_vec_file_path, 'rb', 0) as in_vec_file, open(golden_vec_file_path, 'rb', 0) as golden_vec_file:

        for vectors in range(total_vectors):
            # read input vector
            byte_data = in_vec_file.read(in_vector_bytes_num)
            bytes_to_bit_array(byte_data, in_vector)
            in_vector = reverse_array(in_vector)
            print(in_vector[:10])

            # read expected/golden output vector
            byte_data = golden_vec_file.read(out_vector_bytes_num)
            bytes_to_bit_array(byte_data, golden_vector)
            golden_vector = reverse_array(golden_vector)
            print(golden_vector[:10])
#             print(len(golden_vector))
            
            
            #if vectors < 70:
            #    continue
            
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
                if(toggle==0 and fall_edge >= 18 and fall_edge < (18 + in_vector_size)):
                    TDI.value(in_vector[in_vec_index])
                    if fall_edge == (17+in_vector_size):
                        TMS.value(1)
                    if fall_edge == (16+in_vector_size):
                        TMS.value(0)
                    if fall_edge == (15+in_vector_size):
                        TMS.value(1)
                    in_vec_index= in_vec_index+1
                
                # shift DR
                if(fall_edge == (18+in_vector_size)):
                    TMS.value(0)
                
                # shift out response 
                if(toggle==0 and fall_edge > (18+in_vector_size) and fall_edge <= (18 + in_vector_size + out_vector_size)):
                    out_vector[out_vec_index] = TDO.value()
                    out_vec_index = out_vec_index+1
                    
                    
                    # Exit-DR
                    if (fall_edge==(18 +  in_vector_size + out_vector_size)):
                        TMS.value(1)
                        
                if (fall_edge==(21 +  in_vector_size + out_vector_size)):
                    TMS.value(0)
                    
                toggle = ~ toggle
                
                if (fall_edge == (22 +  in_vector_size + out_vector_size)):
                    break
            
#           Check the output test vectors against the golden test vectors
            
            for i in range(out_vector_size):
                if(out_vector[i]!=golden_vector[i]):
                    mismatch = mismatch + 1
                    print (f"bit {i} mismatch; out ={out_vector[i]} expected = {golden_vector[i]}") 
            
                   
            if (mismatch):
                print (f"Vectors {vectors} Mismatches = {mismatch}")
                break
            else:
                print(f"Vectors {vectors} Match!") 
                
            # reset variables for testing new vector
            
            fall_edge = 0
            out_vec_index = 0
            in_vec_index = 0
            mismatch=0
            tms_pattern=0b01100110
            instruction=0b0011
                
                
                #if vectors==1:
                #    break
        in_vec_file.close()
        golden_vec_file.close() 
except Exception as e:
    print(f"An error occurred: {e}")