#include <common.h>


void set_registers()
{
    configure_gpio(0 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(1 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(2 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(3 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(4 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(5 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(6 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(7 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(8 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(9 , GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(10, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(11, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(12, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(13, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(14, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(15, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(16, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(17, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    configure_gpio(18, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);

}
/*
@ send on the next io (start from 0 to 18)
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
    int io_number = -1;
    int count = 0;
    int mask;
    int recieved;
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
        io_number++;
        mask = 0x1 << io_number;
        old_recieved = get_gpio_l() & mask;
        while (true)
        {
            recieved = get_gpio_l() & mask; // mask gpio bit
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
