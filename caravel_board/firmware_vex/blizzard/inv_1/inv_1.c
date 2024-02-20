#include <common.h>

void main()
{
    HKGpio_config();
    int count = 0;
    configure_mgmt_gpio_input();
    while (reg_gpio_in == 0)
    {
        if (count == 0) {
            count++;
            configure_gpio(21, GPIO_MODE_USER_STD_OUTPUT); // 13 a[0] -> GPIO[21]
            configure_gpio(20, GPIO_MODE_USER_STD_OUTPUT); // 14 a[1] -> GPIO[20]
            configure_gpio(19, GPIO_MODE_USER_STD_OUTPUT); // 15 a[2] -> GPIO[19]
            configure_gpio(18, GPIO_MODE_USER_STD_OUTPUT); // 16 a[3] -> GPIO[18]
            configure_gpio(17, GPIO_MODE_USER_STD_OUTPUT); // 17 a[4] -> GPIO[17]
            configure_gpio(16, GPIO_MODE_USER_STD_OUTPUT); // 18 a[5] -> GPIO[16]
            configure_gpio(15, GPIO_MODE_USER_STD_OUTPUT); // 19 a[6] -> GPIO[15]
            configure_gpio(13, GPIO_MODE_USER_STD_OUTPUT); // 36 a[7] -> GPIO[13]
            configure_gpio(12, GPIO_MODE_USER_STD_OUTPUT); // 37 a[8] -> GPIO[12]
            configure_gpio(8, GPIO_MODE_USER_STD_OUTPUT);  // 39 b[1] -> GPIO[8]
            configure_gpio(7, GPIO_MODE_USER_STD_OUTPUT);  // 40 b[2] -> GPIO[7]
            configure_gpio(6, GPIO_MODE_USER_STD_OUTPUT);  // 41 b[3] -> GPIO[6]

            configure_gpio(5, GPIO_MODE_USER_STD_INPUT_PULLDOWN);  // 42 b[4] -> GPIO[5]
            configure_gpio(4, GPIO_MODE_USER_STD_INPUT_PULLDOWN);  // 43 b[5] -> GPIO[4]
            configure_gpio(3, GPIO_MODE_USER_STD_INPUT_PULLDOWN);  // 44 b[6] -> GPIO[3]
            configure_gpio(2, GPIO_MODE_USER_STD_INPUT_PULLDOWN);  // 45 b[7] -> GPIO[2]
            configure_gpio(0, GPIO_MODE_USER_STD_INPUT_PULLDOWN);  // 46 b[8] -> GPIO[0]
            configure_gpio(33, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 119 c[0] -> GPIO[33]
            configure_gpio(32, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 120 c[1] -> GPIO[32]
            configure_gpio(31, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 121 c[2] -> GPIO[31]
            configure_gpio(30, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 122 c[3] -> GPIO[30]
            configure_gpio(28, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 123 c[4] -> GPIO[28]
            configure_gpio(26, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 125 c[6] -> GPIO[26]
            configure_gpio(24, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 127 c[8] -> GPIO[24]

            // gpio_config_io();
            gpio_config_load();
        }
    };
    HKGpio_config();
}