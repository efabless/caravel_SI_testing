#include <common.h>

void main()
{
    int i, j;
    int num_pulses = 4;
    char *c;
    configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    set_gpio_h(0);
    set_gpio_l(0);
    gpio_config_load();
    config_uart();
    print("Start Test: gpio_o\n");
    // j = 0;
    while (true)
    {
        c = uart_get_line();
        j = get_int_from_string(c);
        if (j >= 32)
        {
            for (i = 0; i < num_pulses; i++)
            {
                set_gpio_h(0x1 << j - 32);
                print("u\n");
                count_down(PULSE_WIDTH);
                set_gpio_h(0x0);
                print("d\n");
                count_down(PULSE_WIDTH);
            }
        }
        else
        {
            for (i = 0; i < num_pulses; i++)
            {
                set_gpio_l(0x1 << j);
                print("u\n");
                count_down(PULSE_WIDTH);
                set_gpio_l(0x0);
                print("d\n");
                count_down(PULSE_WIDTH);
            }
        }

        // j++;
    }

    // mgmt_gpio_o_enable();
    // set_gpio_h(0xFF);
    // set_gpio_l(0xFFFFFFFF);
    // send_packet(10);

    // set_gpio_h(0);
    // set_gpio_l(0);
    // send_packet(10);

    // set_gpio_h(0x55);
    // set_gpio_l(0x55555555);
    // send_packet(10);

    // set_gpio_h(0xAA);
    // set_gpio_l(0xAAAAAAAA);
    // send_packet(10);

    // // only IO 36 = 1
    // set_gpio_h(0x10);
    // set_gpio_l(0);
    // send_packet(10);

    // // only IO 37 = 1
    // set_gpio_h(0x20);
    // set_gpio_l(0);
    // send_packet(10);

}
