#include "send_packet.c"


void configure_mgmt_gpio_i(char en){
    reg_gpio_ien = en;
    reg_gpio_oe = en;
    reg_gpio_out = 0; 
}

// used to detect recieving packet 
int recieve_packet(int timeout){
    reg_gpio_oe = 0; // disable the output
    reg_gpio_out = 0; 
    int packet_size = 0;
    bool is_full_pulse = false; // indecator for full pulse if half pulse is just sent it will be false
    while (reg_gpio_in == 1);
    while (reg_gpio_in == 0);
    while (reg_gpio_in == 1);
    while (reg_gpio_in == 0);
    packet_size++; // First packet not expected to get end of transmission 
    is_full_pulse == true;
    int count = 0;
    while (true){
        if (reg_gpio_in == 1){
            count++;
            if (count >= timeout){
                reg_gpio_oe = 1;// enable the output
                reg_gpio_out = 1;
                return packet_size;
            }
        }
        else if (reg_gpio_in == 0){
            if (count > 0){ // indicate goes to 1 then 0 
                is_full_pulse = !is_full_pulse;
                if (is_full_pulse)
                    packet_size++; 
            }
            count = 0;
        }
    }
}

