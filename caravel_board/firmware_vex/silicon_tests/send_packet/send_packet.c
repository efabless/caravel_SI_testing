#include <defs.h>
// #include "send_packet.h"

#define  PULSE_WIDTH   2500000
 

void count_down(const int d)
{
    /* Configure timer for a single-shot countdown */
	reg_timer0_config = 0;
	reg_timer0_data = d;
	reg_timer0_config = 1; /* Enabled, one-shot, down count */

    // Loop, waiting for value to reach zero
   reg_timer0_update = 1;  // latch current value
   while (reg_timer0_value > 0) {
           reg_timer0_update = 1;
   }

}

// used to make 1-> 0 pulse if is pulse = 1 if is_pulse = 0 send high signal for pulse period 
void send_pulse(int is_pulse){
    reg_gpio_out = 1;
    count_down(PULSE_WIDTH);
    reg_gpio_out = (~is_pulse) & 0x1;
    count_down(PULSE_WIDTH);  
}
void send_pulse_1(int is_pulse){
    reg_gpio_out = 0;
    count_down(PULSE_WIDTH);
    reg_gpio_out = 1;
    count_down(PULSE_WIDTH);  
}

// used to make 1-> 0 pulse if is pulse = 1 if is_pulse = 0 send high signal for pulse period 
void send_packet(int num_pulses){
    // start of packet
    reg_gpio_out = 0;
    count_down(PULSE_WIDTH);
    // send pulses
    for (int i = 0; i < num_pulses; i++){
        send_pulse(1);
    }
    // end of packet
    for (int i = 0; i < 20-num_pulses; i++){
        send_pulse(0);
    }


    // for (int i = 0; i < 20; i++){
    //     if (i==0){
    //         reg_gpio_out = 0;
    //         count_down(PULSE_WIDTH);
    //     }else if (i>1 && i<num_pulses){
    //         send_pulse(1);
    //     }else{
    //     send_pulse(0);

    //     }
    // }
}
void send_packet_1(int num_pulses){

    // send pulses
    for (int i = 0; i < num_pulses+1; i++){
        send_pulse_1(1);
    }
    // end of packet
    count_down(PULSE_WIDTH*10);
    

}
void configure_mgmt_gpio(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;	// Corrected for full swing (value should be 0)
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // default
}
/* 
This test is for send package with the software testing setup 
test will send packet with 4,10,10,1,1,5,5,9 pulses in the same order
*/
void main(){
    configure_mgmt_gpio();
    count_down(PULSE_WIDTH*50);
    // Uncomment the while() loop to make this continuous
    // while (1) {
	send_packet_1(1);
    count_down(PULSE_WIDTH*10);
	send_packet_1(2);
    count_down(PULSE_WIDTH*10);
	send_packet_1(3);
    count_down(PULSE_WIDTH*10);
	send_packet_1(4);
    count_down(PULSE_WIDTH*10);
	send_packet_1(5);
    count_down(PULSE_WIDTH*10);
	send_packet_1(6);
    count_down(PULSE_WIDTH*10);
	send_packet_1(7);
    count_down(PULSE_WIDTH*10);
	send_packet_1(8);
	
    while(1);
	// count_down(1000000);

    // }
}
