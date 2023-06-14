#include <common.h>

void set_registers()
{
    GPIOs_configure(0, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(1, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(2, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(3, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(4, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(6, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(7, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(8, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(9, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(10, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(11, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(12, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(13, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(14, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(15, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(16, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(17, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(18, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
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
    GPIOs_writeHigh(0);
    GPIOs_writeLow(0);
    configure_mgmt_gpio();
    //    gpio_config_io();
    GPIOs_loadConfigs();
    count_down(PULSE_WIDTH * 20);

    // send_packet(2); // configuration finished start test

    while (true)
    {
        send_packet(1); // send on the next io
        io_number++;
        mask = 0x1 << io_number;
        old_recieved = GPIOs_readLow() & mask;
        while (true)
        {
            recieved = GPIOs_readLow() & mask; // mask gpio bit
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
