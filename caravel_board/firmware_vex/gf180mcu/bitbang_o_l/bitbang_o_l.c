#include <common.h>
#include <bitbang.h>

void main()
{
    int i, j;
    int num_pulses = 4;
    int num_bits = 19;
    configure_mgmt_gpio();
    bb_configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    set_gpio_h(0);
    set_gpio_l(0);
    send_packet(1); // configuration finished

    for (j = 0; j < 9; j++)
    {
        send_packet(j + 2); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++)
        {
            set_gpio_l(0x1 << j);
            count_down(PULSE_WIDTH);
            set_gpio_l(0x0);
            count_down(PULSE_WIDTH);
        }
    }

    send_packet(1); // reset counter
    for (j = 9; j < 19; j++)
    {
        send_packet(j - 9 + 2); // send 4 pulses at gpio[j]
        for (i = 0; i < num_pulses; i++)
        {
            set_gpio_l(0x1 << j);
            count_down(PULSE_WIDTH);
            set_gpio_l(0x0);
            count_down(PULSE_WIDTH);
        }
    }

    send_packet(1); // finish test
    send_packet(1); // finish test
    send_packet(1); // finish test

    configure_gpio_default();
    gpio_config_load();
}
