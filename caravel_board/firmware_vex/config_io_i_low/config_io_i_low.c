#include "../defs.h"
#include "../gpio_config/gpio_config_io.c"
#include "../common/recieve_packet.c"
//#include "../local_defs.h"
//#include "../stub.c"
//#include "../config_io.h"
//#include "../defs_mpw-two-mfix.h"


void set_registers() {

    reg_mprj_io_0 = 0x1803;
    reg_mprj_io_1 = 0x1803;
    reg_mprj_io_2 = 0x1803;
    reg_mprj_io_3 = 0x1803;
    reg_mprj_io_4 = 0x1803;
    reg_mprj_io_5 = 0x1803;
    reg_mprj_io_6 = 0x1803;
    reg_mprj_io_7 = 0x1803;
    reg_mprj_io_8 = 0x1803;
    reg_mprj_io_9 = 0x1803;
    reg_mprj_io_10 = 0x1803;
    reg_mprj_io_11 = 0x1803;
    reg_mprj_io_12 = 0x1803;
    reg_mprj_io_13 = 0x1803;
    reg_mprj_io_14 = 0x1803;
    reg_mprj_io_15 = 0x1803;
    reg_mprj_io_16 = 0x1803;
    reg_mprj_io_17 = 0x1803;
    reg_mprj_io_18 = 0x1803;

    reg_mprj_io_19 = 0x1803;
    reg_mprj_io_20 = 0x1803;
    reg_mprj_io_21 = 0x1803;
    reg_mprj_io_22 = 0x1803;
    reg_mprj_io_23 = 0x1803;
    reg_mprj_io_24 = 0x1803;
    reg_mprj_io_25 = 0x1803;
    reg_mprj_io_26 = 0x1803;
    reg_mprj_io_27 = 0x1803;
    reg_mprj_io_28 = 0x1803;
    reg_mprj_io_29 = 0x1803;
    reg_mprj_io_30 = 0x1803;
    reg_mprj_io_31 = 0x1803;
    reg_mprj_io_32 = 0x1803;
    reg_mprj_io_33 = 0x1803;
    reg_mprj_io_34 = 0x1803;
//    reg_mprj_io_34 = 0x0403;
    reg_mprj_io_35 = 0x1803;
    reg_mprj_io_36 = 0x1803;
    reg_mprj_io_37 = 0x1803;
//    reg_mprj_io_37 = 0x0403;

}
/*

@ start of test  after configuration
    send packet with size = 1
@ recieving packet of size n 
    wait for 4 pulses on gpio # n-2 
@ recieved 4 pulses on gpio #
    send packet of size 3 
@timeout doesn't recieve 4 pulses on gpio # 
    send packet of size 5

*/
void main()
{
	int i,j;
    int num_pulses = 4;
    int io_number = 0;
    int count = 0;
    long int mask; 
    long int recieved; 
    int timeout = 100;
    set_registers();
    reg_mprj_datah = 0;
    reg_mprj_datal = 0;
    configure_mgmt_gpio();
    gpio_config_io();
    send_packet(1); // configuration finished start test

    while (true){
        io_number = recieve_packet()-2;
        mask = 0x1 << io_number;
        recieved = reg_mprj_datal & mask; // mask gpio bit
        for (i = 0; i < num_pulses; i++){
            count = 0;
            while (recieved == 0x0){ // wait on 0 
                recieved = reg_mprj_datal & mask; // mask gpio bit
                count++;
                if (count > timeout)
                    send_packet(5); //timeout
            }
            count = 0;
             while (recieved == mask ){  // wait on 1
                recieved = reg_mprj_datal & mask; // mask gpio bit
                count++;
                if (count > timeout)
                    send_packet(5); //timeout
            }
        }
        send_packet(3); // ack recieving packet on io
    }
}

