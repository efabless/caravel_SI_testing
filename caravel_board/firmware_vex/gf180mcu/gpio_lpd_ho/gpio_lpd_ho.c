#include <common.h>

void set_registers()
{
    for (int i = 0; i < 38; i++)
    {
        if (i < 19)
        {
            configure_gpio(i, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
        }
        else
        {
            configure_gpio(i, GPIO_MODE_MGMT_STD_OUTPUT);
        }
    }
}
/*
@ finish configuration
    send packet with size 1

GPIO[0:18] is configured as input down up and mapped to GPIO[19:37]

input value send to gpio[0:18] suppose to be received as output at GPIO[19:37]
*/
void main()
{
    configure_mgmt_gpio();
    set_registers();
    set_gpio_h(0);
    set_gpio_l(0);
    gpio_config_load();
    count_down(PULSE_WIDTH * 50);
    send_packet(1); // configuration finished start test
    int mask = 0x7FFFF;
    int mask_h = 0x7E000;
    int i_val = 0;
    int o_val_l;
    int o_val_h;
    while (true)
    {
        i_val = get_gpio_l() & mask;
        o_val_l = i_val << 19;
        o_val_h = i_val & mask_h;
        o_val_h = o_val_h >> 13;
        set_gpio_h(o_val_h);
        set_gpio_l(o_val_l);
    }
}
