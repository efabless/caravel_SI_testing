#include "mem_tests_upper.h"
#include <common.h>

void main()
{

    config_uart();
    print("Start Test: mem_sram_halfW_upper\n");
    if (mem_sram_halfW_upper())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_sram_test_upper\n");
    if (mem_sram_test_upper())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_sram_W_upper\n");
    if (mem_sram_W_upper())
        print("passed\n");
    else
        print("failed\n");

    configure_gpio_default();
    gpio_config_load();

    config_uart();
    print("End Test\n");
}
