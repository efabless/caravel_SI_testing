#include <common.h>
#define PULSE_WIDTH 250000

void main()
{
    int i, j;
    int num_pulses = 4;
    char *c;
    configure_mgmt_gpio_input();
    configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    set_gpio_h(0);
    set_gpio_l(0);
    gpio_config_load();
    config_uart();
    print("Start Test: gpio_o\n");
    while (reg_gpio_in == 1)
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
    }
    // HKGpio_config();

    configure_gpio(0, GPIO_MODE_MGMT_STD_BIDIRECTIONAL);
    configure_gpio(1, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(2, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(3, GPIO_MODE_MGMT_STD_INPUT_PULLUP);
    configure_gpio(4, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(7, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(32, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(33, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(34, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(35, GPIO_MODE_MGMT_STD_OUTPUT);
    gpio_config_load();
}
