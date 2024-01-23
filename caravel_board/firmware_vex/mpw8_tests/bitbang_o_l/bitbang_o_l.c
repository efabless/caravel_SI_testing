#include <common.h>
#include <bitbang.h>

void main()
{
    int i, j;
    int num_pulses = 4;
    int num_bits = 19;
    configure_mgmt_gpio();
    bb_configureAllGpios(GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_writeHigh(0);
    GPIOs_writeLow(0);
    send_packet(1); // configuration finished

    for (j = 0; j < 9; j++)
    {
        send_packet(j + 2); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++)
        {
            GPIOs_writeLow(0x1 << j);
            count_down(PULSE_WIDTH);
            GPIOs_writeLow(0x0);
            count_down(PULSE_WIDTH);
        }
    }

    send_packet(1); // reset counter
    for (j = 9; j < 19; j++)
    {
        send_packet(j - 9 + 2); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++)
        {
            GPIOs_writeLow(0x1 << j);
            count_down(PULSE_WIDTH);
            GPIOs_writeLow(0x0);
            count_down(PULSE_WIDTH);
        }
    }

    send_packet(1); // finish test
    send_packet(1); // finish test
    send_packet(1); // finish test
}
