#include "mem_tests_dff.h"
#include <common.h>

void main()
{
    // while (1) {
    // HKGpio_config();
    configure_mgmt_gpio_input();
    if (reg_gpio_in == 0){
        config_uart_ios();
        config_uart();
        print("ST: mem_dff_halfW\n");
        if (mem_dff_halfW())
            print("passed\n");
        else
            print("failed\n");

        config_uart();
        // count_down(PULSE_WIDTH);
        print("ST: mem_dff_test\n");
        if (mem_dff_test())
            print("passed\n");
        else
            print("failed\n");

        config_uart();
        print("ST: mem_dff_W\n");
        if (mem_dff_W())
            print("passed\n");
        else
            print("failed\n");

        // HKGpio_config();
        config_uart();
        print("End Test\n");
    }
    // };
    HKGpio_config();
}
