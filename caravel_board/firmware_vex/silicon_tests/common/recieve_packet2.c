#include "send_packet.c"


// used to detect recieving packet 
int recieve_packet2(){
    reg_gpio_oe = 0; // disable the output
    reg_gpio_out = 0; 
    int ones = 0;
    int packet_size =0;
    while (reg_gpio_in == 1); // busy wait 0
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
            reg_gpio_oe = 1; // disable the output
            reg_gpio_out = 1; 
            return packet_size;
        }
        count_down(PULSE_WIDTH);
    }
}

