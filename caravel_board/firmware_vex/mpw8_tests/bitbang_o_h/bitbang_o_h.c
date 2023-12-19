#include <common.h>
#include <bitbang.h>

/*

@ start sending on the higest gpios
    send packet with size = 1
@ send 4 pulses at gpio[37]
    send packet with size = 2
@ send 4 pulses at gpio[36]
    send packet with size = 3
@ send 4 pulses at gpio[35]
    send packet with size = 4
@ send 4 pulses at gpio[34]
    send packet with size = 5
@ send 4 pulses at gpio[33]
    send packet with size = 6
@ send 4 pulses at gpio[32]
    send packet with size = 7
@ send 4 pulses at gpio[31]
    send packet with size = 8
@ send 4 pulses at gpio[30]
    send packet with size = 9
@ send 4 pulses at gpio[29]
    send packet with size = 10

@ reset pulses
    send packet with size = 1
@ send 4 pulses at gpio[28]
    send packet with size = 2
@ send 4 pulses at gpio[27]
    send packet with size = 3
@ send 4 pulses at gpio[26]
    send packet with size = 4
@ send 4 pulses at gpio[25]
    send packet with size = 5
@ send 4 pulses at gpio[24]
    send packet with size = 6
@ send 4 pulses at gpio[23]
    send packet with size = 7
@ send 4 pulses at gpio[22]
    send packet with size = 8
@ send 4 pulses at gpio[21]
    send packet with size = 9
@ send 4 pulses at gpio[20]
    send packet with size = 10
@ send 4 pulses at gpio[19]
    send packet with size = 11

@ test finish
    send packet with size = 1
    send packet with size = 1
    send packet with size = 1


*/
void main()
{
    int i, j;
    int num_pulses = 4;
    int num_bits = 8;
    configure_mgmt_gpio();
    bb_configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    set_gpio_h(0);
    set_gpio_l(0);


    send_packet(1); // start sending on the higest gpios
    for (j = 37; j > 28; j--)
    {
        send_packet(37 - j + 2); // send 4 pulses at gpio[j]
        if (j >= 32)
        {
            for (i = 0; i < num_pulses; i++)
            {
                set_gpio_h(0x1 << j - 32);
                count_down(PULSE_WIDTH);
                set_gpio_h(0x0);
                count_down(PULSE_WIDTH);
            }
        }
        else
        {
            for (i = 0; i < num_pulses; i++)
            {
                set_gpio_l(0x1 << j);
                count_down(PULSE_WIDTH);
                set_gpio_l(0x0);
                count_down(PULSE_WIDTH);
            }
        }
    }
    send_packet(1); // reset counter
    for (j = 28; j > 18; j--)
    {
        send_packet(28 - j + 2); // send 4 pulses at gpio[j]
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
}
