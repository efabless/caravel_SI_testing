#include "mem_tests_dff2.h"
#include <common.h>

void main()
{
    while (1)
    {
        HKGpio_config();
        configure_mgmt_gpio_input();
        if (reg_gpio_in == 0){
            config_uart();
            print("Start Test: mem_dff2_halfW\n");
            if (mem_dff2_halfW())
                print("passed\n");
            else
                print("failed\n");

            config_uart();
            print("Start Test: mem_dff2_W\n");
            if (mem_dff2_W())
                print("passed\n");
            else
                print("failed\n");

            config_uart();
            print("Start Test: mem_dff2_test\n");
            if (mem_dff2_test())
                print("passed\n");
            else
                print("failed\n");

            HKGpio_config();
            enable_uart_TX(1);
            count_down(PULSE_WIDTH * 10);
            print("End Test\n");
        }
    };
    HKGpio_config();
}
