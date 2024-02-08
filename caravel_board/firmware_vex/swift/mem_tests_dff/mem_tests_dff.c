#include "mem_tests_dff.h"
#include <firmware_apis.h>
void main()
{
    config_uart();
    print("Start Test: mem_dff_halfW\n");
    count_down(PULSE_WIDTH*10);
    if (mem_dff_halfW())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_dff_W\n");
    count_down(PULSE_WIDTH*10);
    if (mem_dff_W())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_dff_byte\n");
    count_down(PULSE_WIDTH*10);
    if (mem_dff_byte())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("End Test\n");
    HKGpio_config();
}
