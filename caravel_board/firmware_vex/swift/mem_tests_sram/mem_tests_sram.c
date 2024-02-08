#include "mem_tests_sram.h"
#include <firmware_apis.h>

void main()
{
    config_uart();
    print("Start Test: mem_sram_halfW\n");
    count_down(PULSE_WIDTH*10);
    if (mem_sram_halfW())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_sram_byte\n");
    count_down(PULSE_WIDTH*10);
    if (mem_sram_byte())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_sram_W\n");
    count_down(PULSE_WIDTH*10);
    if (mem_sram_W())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("End Test\n");
    HKGpio_config();
}
