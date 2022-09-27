#include "send_packet.c"


void configure_mgmt_gpio_i(char en){
    reg_gpio_ien = en;
    reg_gpio_oe = en;
}

// used to detect recieving packet 
int recieve_packet(int timeout){
    configure_mgmt_gpio_i(0);
    configure_mgmt_gpio_i(1);
    int packet_size = 0;
    bool is_full_pulse = false; // indecator for full pulse if half pulse is just sent it will be false
    reg_mprj_datal = 0x0;
    while (reg_gpio_in == 0);
    reg_mprj_datal = 0x4000;
    while (reg_gpio_in == 1);
    reg_mprj_datal = 0x0;
    while (reg_gpio_in == 0);
    reg_mprj_datal = 0x4000;
    while (reg_gpio_in == 1);
    packet_size++; // First packet not expected to get end of transmission 
    is_full_pulse == true;
    int count = 0;
    while (true){
        if (reg_gpio_in == 0){
            reg_mprj_datal = 0x0;
            count++;
            if (count >= timeout)
            return packet_size;
        }
        else if (reg_gpio_in == 1){
            reg_mprj_datal = 0x4000;
            count = 0;
            is_full_pulse = !is_full_pulse;
            if (is_full_pulse)
                packet_size++; 

        }
    }
}

