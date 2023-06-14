#include <common.h>
// #define PULSE_WIDTH 2500000

void uart_io()
{
    int i, j;
    int num_pulses = 4;
    int num_bits = 19;
    int count = 0;
    int mask;
    int recieved;
    int old_recieved;
    int timeout = 15000;
    long int timeout_count = 0;
    configure_mgmt_gpio();
    GPIOs_configure(6, GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_writeHigh(0);
    GPIOs_writeLow(0);
    GPIOs_loadConfigs();
    // gpio_config_io();
    mask = 0x1 << 5;
    // count_down(PULSE_WIDTH * 100);
    send_packet(2); // configuration finished
    count_down(PULSE_WIDTH * 4);
    for (i = 0; i < num_pulses; i++)
    {
        GPIOs_writeLow(0x1 << 6);
        count_down(PULSE_WIDTH);
        GPIOs_writeLow(0x0);
        count_down(PULSE_WIDTH);
    }

    send_packet(3);

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
                send_packet(9); // timeout
            return;
        }
    }

    send_packet(4); // finish test
}