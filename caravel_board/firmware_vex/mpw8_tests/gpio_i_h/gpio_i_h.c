#include <common.h>


void set_registers(){
    configure_gpio(19, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(20, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(21, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(22, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(23, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(24, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(25, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(26, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(27, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(28, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(29, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(30, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(31, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(32, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(33, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(34, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(35, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(36, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(37, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
}
/*
@ send on the next io (start from 37 to 19)
    send packet with size 1
@ recieving packet of size n
    wait for 4 pulses on gpio
@ recieved 4 pulses on gpio #
    send packet of size 3
@timeout doesn't recieve 4 pulses on gpio #
    send packet of size 5

*/
void main()
{
    int i, j;
    int num_pulses = 4;
    int io_number = 38;
    int count = 0;
    int mask;
    int recieved;
    int temp_io = 0;
    int old_recieved;
    int timeout = 15000;
    long int timeout_count = 0;
    set_registers();
    set_gpio_h(0);
    set_gpio_l(0);
    configure_mgmt_gpio();
//    gpio_config_io();
    gpio_config_load();
    // send_packet(1); // configuration finished start test

    while (true)
    {
        send_packet(1); // send on the next io
        io_number--;
        if (io_number >= 32)
        {
            temp_io = io_number - 32;
            mask = 0x1 << temp_io;
            old_recieved = get_gpio_h() & mask;
        }
        else
        {
            mask = 0x1 << io_number;
            old_recieved = get_gpio_l() & mask;
        }

        while (true)
        {
            if (io_number >= 32)
            {
                recieved = get_gpio_h() & mask; // mask gpio bit
            }
            else
            {
                recieved = get_gpio_l() & mask; // mask gpio bit
            }
            if (recieved != old_recieved)
            {
                count++;
                old_recieved = recieved;
                timeout_count = 0;
            }
            else
            {
                timeout_count++;
            }
            if (count == 10)
                break;
            if (timeout_count > timeout)
            {
                while (true)
                    send_packet(5); // timeout
                return;
            }
        }
        count_down(PULSE_WIDTH * 20);
        send_packet(3); // ack recieving packet on io
        count = 0;
    }
}
