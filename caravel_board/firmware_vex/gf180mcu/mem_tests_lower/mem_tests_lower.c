#include "mem_tests_lower.h"
#include <common.h>

void main()
{
    config_uart();
    print("Start Test: mem_sram_halfW_lower");
    if (mem_sram_halfW_lower())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_sram_W_lower");
    if (mem_sram_W_lower())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_sram_test_lower");
    if (mem_sram_test_lower())
        print("passed\n");
    else
        print("failed\n");

    configure_gpio_default();
    gpio_config_load();

    config_uart();
    print("End Test\n");
}
