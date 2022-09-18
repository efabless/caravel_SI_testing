#include <defs.h>

// #include "../send_packet/send_packet.h"
#include "send_packet.c"
#include "bitbang.c"


/*
    configure the gpio[37] as mgmt input using bitbang then wait for pattern in it 
    generate send 10 pulses in the gpio 37 
    gpio_37 10 10 
    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ wait for high input 
        send packet size = 5 
    @ wait for low input 
        send packet size = 7
    @ wait for high input 
        send packet size = 5 
    @ wait for low input 
        send packet size = 7
    @ can't find input timeout
        send packet size = 9
    @ finish test 
        send packet size = 3 
        send packet size = 3 
        send packet size = 3 
*/

void wait_for_pattern(uint32_t pattern){
    int time_out = 1000000;
    bool is_found = false;
    uint32_t mask = 0x1;
    uint32_t data ;
    // waiting for  
    for (int i = 0; i < time_out; i++){
        data = reg_mprj_datal && mask >> 0;
        if (data == pattern){
            is_found = true;
            break;
        }
    }
    if (!is_found){
        send_packet(9); // pattern not found timeout
    }
}

void main(){

    unsigned int i;
    configure_mgmt_gpio();
    reg_mprj_io_37 = 0x1803;


    /* Enable one of the following two blocks for right or left side
     * configuration.
     */
    send_packet(1); // start of bitbang
    while (1) {
	clear_registers();	
    // clock_in_right_i_left_i_standard(0); // 18	and 19	
    // clock_in_right_i_left_i_standard(0); // 17	and 20	
    // clock_in_right_i_left_i_standard(0); // 16	and 21	
    // clock_in_right_i_left_i_standard(0); // 15	and 22	
    // clock_in_right_i_left_i_standard(0); // 14	and 23	
    // clock_in_right_i_left_i_standard(0); // 13	and 24	
    // clock_in_right_i_left_i_standard(0); // 12	and 25	
    // clock_in_right_i_left_i_standard(0); // 11	and 26	
    // clock_in_right_i_left_i_standard(0); // 10	and 27	
    // clock_in_right_i_left_i_standard(0); // 9	and 28	
    // clock_in_right_i_left_i_standard(0); // 8	and 29	
    // clock_in_right_i_left_i_standard(0); // 7	and 30	
    // clock_in_right_i_left_i_standard(0); // 6	and 31	
    // clock_in_right_i_left_i_standard(0); // 5	and 32	
    // clock_in_right_i_left_i_standard(0); // 4	and 33	
    // clock_in_right_i_left_i_standard(0); // 3	and 34	
    // clock_in_right_i_left_i_standard(0); // 2	and 35	
    // clock_in_right_i_left_i_standard(0); // 1	and 36		
    clock_in_right_i_left_i_standard(0); // 0	and 37	
    load();		         // 0   and 37 and load

    send_packet(2);// end of bitbang

    send_packet(5);// wait for high input
    wait_for_pattern(1);
    send_packet(7);// wait for low input
    wait_for_pattern(0) ;   
    send_packet(5);// wait for high input
    wait_for_pattern(1);
    send_packet(7);// wait for low input
    wait_for_pattern(0);
	
    send_packet(3);// sending pulses on gpio
    send_packet(3);// sending pulses on gpio
    send_packet(3);// sending pulses on gpio

   }
}