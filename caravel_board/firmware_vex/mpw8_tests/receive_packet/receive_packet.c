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
    count_down(PULSE_WIDTH * 50);
    send_packet(2);
    int recieved_size = 0;
    char recieved_char;
    configure_mgmt_gpio_input();
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    // gpio_config_io();
    gpio_config_load();
    enable_uart_TX(1);
    print("ready");
    while (true)
    {
        recieved_size = receive_packet();
        recieved_char = recieved_size + "0";
        print("number of = ");
        print(recieved_char);
    }
}
