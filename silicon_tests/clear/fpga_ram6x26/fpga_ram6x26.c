#include <common.h>

void main()
{
    // HKGpio_config();
    configure_mgmt_gpio_input();
    // while (1)
    // {
    // if (reg_gpio_in == 0) {
    // FPGA IOs
    configure_gpio(1, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(11, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(23, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(29, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(34, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(35, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(37, GPIO_MODE_USER_STD_INPUT_NOPULL);

    configure_gpio(0, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(2, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(3, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(4, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(5, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(6, GPIO_MODE_USER_STD_OUTPUT);

    configure_gpio(7, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(12, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(13, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(15, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(16, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(17, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(18, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(24, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(26, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(28, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(30, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(31, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    gpio_config_load();
        
    while (reg_gpio_in == 0)
        ;
    HKGpio_config();
}