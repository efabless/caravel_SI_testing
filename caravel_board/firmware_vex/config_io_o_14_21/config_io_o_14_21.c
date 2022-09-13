#include "../defs.h"
#include "../gpio_config/gpio_config_io.c"
#include "../common/send_packet.c"
//#include "../local_defs.h"
//#include "../stub.c"

//#include "../config_io.h"
//#include "../defs_mpw-two-mfix.h"


void set_registers() {

    reg_mprj_io_0 = GPIO_MODE_MGMT_STD_ANALOG;
    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_5 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_7 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_8 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_9 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_10 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_11 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_12 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_13 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_14 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_15 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_16 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_17 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_18 = GPIO_MODE_MGMT_STD_OUTPUT;

    reg_mprj_io_19 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_20 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_21 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_22 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_23 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_24 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_25 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_26 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_27 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_28 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_29 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_30 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_31 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_32 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_33 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_34 = GPIO_MODE_MGMT_STD_OUTPUT;
//    reg_mprj_io_34 = 0x0403;
    reg_mprj_io_35 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_36 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_37 = GPIO_MODE_MGMT_STD_OUTPUT;
//    reg_mprj_io_37 = 0x0403;

}
/*

@ start of test  after configuration
    send packet with size = 1

@ send 4 pulses at gpio[14]  
    send packet with size = 2
@ send 4 pulses at gpio[15] 
    send packet with size = 3
@ send 4 pulses at gpio[16]  
    send packet with size = 4
@ send 4 pulses at gpio[17]  
    send packet with size = 5
@ send 4 pulses at gpio[18]  
    send packet with size = 6

@ send 4 pulses at gpio[22]  
    send packet with size = 7
@ send 4 pulses at gpio[21]  
    send packet with size = 8
@ send 4 pulses at gpio[20]  
    send packet with size = 9
@ send 4 pulses at gpio[19]  
    send packet with size = 10

@ test finish 
    send packet with size = 1
    send packet with size = 1
    send packet with size = 1

*/
void main()
{
	int i,j;
    int num_pulses = 4;
    int num_bits = 19;
    configure_mgmt_gpio();
    set_registers();
    reg_mprj_datah = 0;
    reg_mprj_datal = 0;
    gpio_config_io();
    send_packet(1); // configuration finished
    int counter = 1;
    for (j=14;j<19;j++){
        counter++;
        send_packet(counter); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++){
            reg_mprj_datal = 0x1 << j;
            count_down(PULSE_WIDTH);  
            reg_mprj_datal = 0x0;  
            count_down(PULSE_WIDTH);  
        }
    }

    for (j=22;j > 18;j--){
        counter++;
        send_packet(counter); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++){
            reg_mprj_datal = 0x1 << j;
            count_down(PULSE_WIDTH);  
            reg_mprj_datal = 0x0;  
            count_down(PULSE_WIDTH);  
        }

    }

    send_packet(1); // finish test
    send_packet(1); // finish test
    send_packet(1); // finish test

}

