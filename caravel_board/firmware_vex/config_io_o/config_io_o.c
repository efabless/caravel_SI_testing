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
@ send 4 pulses at gpio[0]  
    send packet with size = 2
@ send 4 pulses at gpio[1]  
    send packet with size = 3
@ send 4 pulses at gpio[2]  
    send packet with size = 4
@ send 4 pulses at gpio[3]  
    send packet with size = 5
@ send 4 pulses at gpio[4]  
    send packet with size = 6
@ send 4 pulses at gpio[5]  
    send packet with size = 7
@ send 4 pulses at gpio[6]  
    send packet with size = 8
@ send 4 pulses at gpio[7]  
    send packet with size = 9

@ reset pulses
    send packet with size = 1
@ send 4 pulses at gpio[9]  
    send packet with size = 2
@ send 4 pulses at gpio[10]  
    send packet with size = 3
@ send 4 pulses at gpio[11]  
    send packet with size = 4
@ send 4 pulses at gpio[12]  
    send packet with size = 5
@ send 4 pulses at gpio[13]  
    send packet with size = 6


@ start sending on the higest gpios 
    send packet with size = 1
@ send 4 pulses at gpio[37]  
    send packet with size = 2
@ send 4 pulses at gpio[36]  
    send packet with size = 3
@ send 4 pulses at gpio[35]  
    send packet with size = 4
@ send 4 pulses at gpio[34]  
    send packet with size = 5
@ send 4 pulses at gpio[33]  
    send packet with size = 6
@ send 4 pulses at gpio[32]  
    send packet with size = 7
@ send 4 pulses at gpio[31]  
    send packet with size = 8
@ send 4 pulses at gpio[30]  
    send packet with size = 9

@ reset pulses
    send packet with size = 1
@ send 4 pulses at gpio[28]  
    send packet with size = 2
@ send 4 pulses at gpio[27]  
    send packet with size = 3
@ send 4 pulses at gpio[26]  
    send packet with size = 4
@ send 4 pulses at gpio[25]  
    send packet with size = 5
@ send 4 pulses at gpio[24]  
    send packet with size = 6
@ send 4 pulses at gpio[23]  
    send packet with size = 7
@ send 4 pulses at gpio[22]  
    send packet with size = 8

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

    for (j=0;j<9;j++){
        send_packet(j+2); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++){
            reg_mprj_datal = 0x1 << j;
            count_down(PULSE_WIDTH);  
            reg_mprj_datal = 0x0;  
            count_down(PULSE_WIDTH);  
        }
    }

    send_packet(1); // reset counter
    for (j=9;j<14;j++){
        send_packet(j-9+2); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++){
            reg_mprj_datal = 0x1 << j;
            count_down(PULSE_WIDTH);  
            reg_mprj_datal = 0x0;  
            count_down(PULSE_WIDTH);  
        }
    }

    send_packet(1); //start sending on the higest gpios
    for (j=37;j > 28;j--){
        send_packet(37-j+2); // send 4 pulses at gpio[j]
        if (j>=32){
            for (i = 0; i < num_pulses; i++){
                reg_mprj_datah = 0x1 << j-32;
                count_down(PULSE_WIDTH);  
                reg_mprj_datah = 0x0;  
                count_down(PULSE_WIDTH);  
            }
        }else{
            for (i = 0; i < num_pulses; i++){
                reg_mprj_datal = 0x1 << j;
                count_down(PULSE_WIDTH);  
                reg_mprj_datal = 0x0;  
                count_down(PULSE_WIDTH);  
            }
        }
    }
    send_packet(1); // reset counter
    for (j=28;j > 21;j--){
        send_packet(28-j+2); // send 4 pulses at gpio[j]
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

