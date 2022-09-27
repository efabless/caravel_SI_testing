#include "send_packet.c"
// used to detect recieving packet 

void configure_mgmt_gpio_input(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // Fixed for full swing operation
    reg_gpio_ien = 1;
    reg_gpio_oe = 0;
    reg_gpio_out = 0; // default
    count_down(PULSE_WIDTH*20);
}
// used to detect recieving packet 
int recieve_packet(){
    configure_mgmt_gpio_input();
    int ones = 0;
    int packet_size =1;
    while (reg_gpio_in == 0); // busy wait 0
    count_down(PULSE_WIDTH/2);
    while (true){
        if (reg_gpio_in == 1){
            ones++;
        }
        else if (reg_gpio_in == 0){
            if (ones > 0)
                packet_size++;
            ones = 0;
        }
        if (ones>3){
            configure_mgmt_gpio();
            return packet_size;
        }
        count_down(PULSE_WIDTH);
    }
}