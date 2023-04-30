#include <common.h>

void main(){
    configure_mgmt_gpio();
    count_down(PULSE_WIDTH*50);
    // Uncomment the while() loop to make this continuous
    // while (1) {
	send_packet(1);
    count_down(PULSE_WIDTH*10);
	send_packet(2);
    count_down(PULSE_WIDTH*10);
	send_packet(3);
    count_down(PULSE_WIDTH*10);
	send_packet(4);
    count_down(PULSE_WIDTH*10);
	send_packet(5);
    count_down(PULSE_WIDTH*10);
	send_packet(6);
    count_down(PULSE_WIDTH*10);
	send_packet(7);
    count_down(PULSE_WIDTH*10);
	send_packet(8);
	
    while(1);
	// count_down(1000000);

    // }
}
