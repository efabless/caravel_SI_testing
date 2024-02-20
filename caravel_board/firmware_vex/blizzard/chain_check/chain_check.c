#include <common.h>
void main()
{
    HKGpio_config();
    while (1){
        configure_mgmt_gpio_input();
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
            // gpio_config_io();
            gpio_config_load();
            config_uart();
            print("Start Test: chain_check\n");
        }
        HKGpio_config();
    };
}