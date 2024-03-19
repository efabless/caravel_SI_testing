#include <common.h>
/*
test is using uart as a comunication channel

/*
@ send "ready" through uart
    send packets of n through mgmt_gpio

loop
    @ send "number of = n" through uart
        send packets of n through mgmt_gpio


*/

void receive_packet_test()
{
    configure_mgmt_gpio();
    send_packet(2);
    bool is_recieved;
    configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    set_gpio_h(0);
    set_gpio_l(0);
    gpio_config_load();
    for (int i = 5; i < 8; i++)
    {
        configure_mgmt_gpio_input();
        set_gpio_l(0x1 << 0);
        is_recieved = recieved_pulse_num(i);
        set_gpio_l(0x0);
        configure_mgmt_gpio();
        if (is_recieved)
        {
            send_packet(i);
        }
        else
        {
            send_packet(9);
        }
    }
}
