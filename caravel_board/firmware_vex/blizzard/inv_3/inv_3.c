#include <common.h>

void main()
{
    configure_gpio(2, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(3, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(4, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(5, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(6, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(7, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(8, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(11, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(12, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(13, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(15, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(16, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(17, GPIO_MODE_USER_STD_INPUT_PULLDOWN);

    configure_gpio(18, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(19, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(20, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(21, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(24, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(25, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(26, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(27, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(28, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(30, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(31, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(32, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(33, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(0, GPIO_MODE_USER_STD_OUTPUT);

    // gpio_config_io();
    gpio_config_load();
    // config_uart();
    // print("Start Test: inv_2\n");

    HKGpio_config();
}