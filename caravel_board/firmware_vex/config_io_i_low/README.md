# config_io_i_low senario
    @ start of test  after configuration
        send packet with size = 1
    @ recieving packet of size n 
        wait for 4 pulses on gpio # n-2 
    @ recieved 4 pulses on gpio #
        send packet of size 3 
    @timeout doesn't recieve 4 pulses on gpio # 
        send packet of size 5