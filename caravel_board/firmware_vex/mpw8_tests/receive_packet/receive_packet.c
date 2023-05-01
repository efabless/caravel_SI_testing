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

void main()
{
    configure_mgmt_gpio();
    configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    send_packet(2);
    int recieved_size = 0;
    configure_mgmt_gpio_input();
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    // gpio_config_io();
    gpio_config_load();
    print("ready");
    while (true)
    {
        recieved_size = receive_packet();
        print("number of = ");
        print(recieved_size);
    }
}
