#include <common.h>
void main()
{
    // HKGpio_config();
    configure_mgmt_gpio_input();
    // while (reg_gpio_in == 0)
    // {
    if (reg_gpio_in == 0) {
        configure_gpio(1, GPIO_MODE_USER_STD_INPUT_NOPULL);
        configure_gpio(23, GPIO_MODE_USER_STD_OUTPUT);
        configure_gpio(29, GPIO_MODE_USER_STD_INPUT_NOPULL);
        configure_gpio(34, GPIO_MODE_USER_STD_INPUT_NOPULL);
        configure_gpio(37, GPIO_MODE_USER_STD_INPUT_NOPULL);
        configure_gpio(10, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
        configure_gpio(11, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
        configure_gpio(35, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
        configure_gpio(36, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
        configure_gpio(21, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
        configure_gpio(20, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
        configure_gpio(19, GPIO_MODE_USER_STD_OUTPUT);

        // gpio_config_io();
        gpio_config_load();
        config_uart();
        print("ST: and_gate\n");
    }
    // };
    HKGpio_config();
}