#include <defs.h>
// #include "send_packet.c"
#include "recieve_packet.c"

/* 
test will send packet and expect to recieve the same packet size
*/
void main(){
    configure_mgmt_gpio();
    count_down(PULSE_WIDTH*50);
    // Uncomment the while() loop to make this continuous
    // while (1) {
    int recieved_size = 0;

    int packet_size = 1;
	send_packet(packet_size);
    count_down(PULSE_WIDTH*10);
    recieved_size = recieve_packet(10000);
    count_down(PULSE_WIDTH*5);
    if (recieved_size == packet_size){
        send_packet(10); // pass same packet send is recieved
    }else { 
        send_packet(9); // error not the same packet sent is recieved
    }

    packet_size = 3;
	send_packet(packet_size);
    count_down(PULSE_WIDTH*10);
    recieved_size = recieve_packet(10000);
    count_down(PULSE_WIDTH*5);
    if (recieved_size == packet_size){
        send_packet(10); // pass same packet send is recieved
    }else { 
        send_packet(9); // error not the same packet sent is recieved
    }
	
    packet_size = 5;
	send_packet(packet_size);
    count_down(PULSE_WIDTH*10);
    recieved_size = recieve_packet(10000);
    count_down(PULSE_WIDTH*5);
    if (recieved_size == packet_size){
        send_packet(10); // pass same packet send is recieved
    }else { 
        send_packet(9); // error not the same packet sent is recieved
    }
	
    while(1);
	
}
