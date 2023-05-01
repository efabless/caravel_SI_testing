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

    // setting bit 7 as input
    configure_gpio(7, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    // gpio_config_io();

    // automatic bitbang approach
    gpio_config_load();

    enable_external1_irq(1);
    user_irq_1_ev_pending_write(1);
    user_irq_0_ev_pending_write(1);
    user_irq_2_ev_pending_write(1);
    user_irq_3_ev_pending_write(1);
    user_irq_4_ev_pending_write(1);
    user_irq_5_ev_pending_write(1);
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
