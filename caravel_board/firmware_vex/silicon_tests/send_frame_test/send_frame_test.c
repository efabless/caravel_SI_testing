#include <defs.h>
#include "send_frame.c"
// #include "send_packet.c"

 
/* 
This test is for sending frames with the software testing setup 
test will send frames 177,105,140,90,215,4 in the same order
*/
void main(){
    configure_mgmt_gpio();
    // Uncomment the while() loop to make this continuous
    // while (1) {
	for (int i = 0; i < 1000; i++);
	
	// send_frame(170);
	send_frame(177);
	count_down(100000);
	send_frame(105);
	count_down(100000);
	send_frame(140);
	count_down(100000);
	send_frame(90);
	count_down(100000);
	send_frame(215);
	count_down(100000);
	send_frame(4);

	
	// count_down(1000000);

    // }
}
