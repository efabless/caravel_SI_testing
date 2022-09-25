#include "send_packet.c"

// used to detect recieving packet 
int recieve_packet(int timeout){
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
            if (count >= timeout)
            return packet_size;
        }
        else if (reg_gpio_in == 0){
            count = 0;
            is_full_pulse = !is_full_pulse;
            if (is_full_pulse)
                packet_size++; 

        }
    }
}