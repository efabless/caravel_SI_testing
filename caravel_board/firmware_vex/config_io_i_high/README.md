# config_io_i_high senario
@ send on the next io (start from 37 to 19)
    send packet with size 1
@ recieving packet of size n 
    wait for 4 pulses on gpio
@ recieved 4 pulses on gpio #
    send packet of size 3 
@timeout doesn't recieve 4 pulses on gpio # 
    send packet of size 5