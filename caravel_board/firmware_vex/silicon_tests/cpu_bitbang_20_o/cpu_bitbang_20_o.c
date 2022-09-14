#include <defs.h>

// #include "../send_packet/send_packet.h"
#include "send_packet.c"
#include "bitbang.c"


/*
    configure the gpio[20] as mgmt output using bitbang then send the next pattern on them 
    generate send 10 pulses in the gpio 20 
    gpio_37 10 10 
    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ start sending 10 pulses at gpio[20] 
        send packet size = 5 
    @ stop sending pulses at gpio[20] 
        send packet size = 7
    @ finish test 
        send packet size = 3 
        send packet size = 3 
        send packet size = 3 
*/

void main(){

    unsigned int i;
    configure_mgmt_gpio();



    reg_mprj_io_20 = GPIO_MODE_MGMT_STD_OUTPUT;


    /* Enable one of the following two blocks for right or left side
     * configuration.
     */
    send_packet(1); // start of bitbang
    while (1) {
	clear_registers();		
    // clock_in_right_o_left_i_standard(0); // 18	and 19	
    clock_in_right_o_left_i_standard(0); // 17	and 20	
    clock_in_right_o_left_i_standard(0); // 16	and 21	
    clock_in_right_o_left_i_standard(0); // 15	and 22	
    clock_in_right_o_left_i_standard(0); // 14	and 23	
    clock_in_right_o_left_i_standard(0); // 13	and 24	
    clock_in_right_o_left_i_standard(0); // 12	and 25	
    clock_in_right_o_left_i_standard(0); // 11	and 26	
    clock_in_right_o_left_i_standard(0); // 10	and 27	
    clock_in_right_o_left_i_standard(0); // 9	and 28	
    clock_in_right_o_left_i_standard(0); // 8	and 29	
    clock_in_right_o_left_i_standard(0); // 7	and 30	
    clock_in_right_o_left_i_standard(0); // 6	and 31	
    clock_in_right_o_left_i_standard(0); // 5	and 32	
    clock_in_right_o_left_i_standard(0); // 4	and 33	
    clock_in_right_o_left_i_standard(0); // 3	and 34	
    clock_in_right_o_left_i_standard(0); // 2	and 35	
    clock_in_right_o_left_i_standard(0); // 1	and 36	
    clock_in_right_o_left_i_standard(0); // 0	and 37		
    load();		         // 0   and 37 and load

    send_packet(2);// end of bitbang

    reg_mprj_datal = 0x00000000;
    reg_mprj_datah = 0x00000000;
    send_packet(5);// start sending 10 pulses at gpio[20] 

    for (int i = 0; i < 10; i++){
        reg_mprj_datal = 0x100000;
        count_down(PULSE_WIDTH);
        reg_mprj_datah = 0;
        count_down(PULSE_WIDTH);
    }
    send_packet(7);// stop sending 10 pulses at gpio[20] 
	
    send_packet(3);// sending pulses on gpio
    send_packet(3);// sending pulses on gpio
    send_packet(3);// sending pulses on gpio

   }
}