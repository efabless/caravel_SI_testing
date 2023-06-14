#include <common.h>

void set_registers()
{
    for (int i = 0; i < 38; i++)
    {
        if (i < 19)
        {
            GPIOs_configure(i, GPIO_MODE_MGMT_STD_INPUT_PULLUP);
        }
        else
        {
            GPIOs_configure(i, GPIO_MODE_MGMT_STD_OUTPUT);
        }
    }
}
/*
@ finish configuration
    send packet with size 1

GPIO[0:18] is configured as input pull up and mapped to GPIO[19:37]

input value send to gpio[0:18] suppose to be received as output at GPIO[19:37]
*/
void main()
{
    set_registers();
    GPIOs_writeHigh(0);
    GPIOs_writeLow(0);
    GPIOs_loadConfigs();
    int mask = 0x7FFFF;
    int mask_h = 0x7E000;
    int i_val = 0;
    int o_val_l;
    int o_val_h;
    // config_uart();
    // print("Start Test: gpio_lpu_ho\n");
    configure_mgmt_gpio();
    send_packet(2);
    while (true)
    {
        i_val = GPIOs_readLow() & mask;
        o_val_l = i_val << 19;
        o_val_h = i_val & mask_h;
        o_val_h = o_val_h >> 13;
        GPIOs_writeHigh(o_val_h);
        GPIOs_writeLow(o_val_l);
    }
}
