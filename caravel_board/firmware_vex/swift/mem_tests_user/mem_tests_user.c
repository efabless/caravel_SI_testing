#include "mem_tests_user.h"
#include <firmware_apis.h>
void main()
{
    config_uart();
    print("Start Test: mem_user_halfW\n");
    count_down(PULSE_WIDTH*10);
    if (mem_user_halfW())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_user_W\n");
    count_down(PULSE_WIDTH*10);
    if (mem_user_W())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_user_byte\n");
    count_down(PULSE_WIDTH*10);
    if (mem_user_byte())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("End Test\n");
    HKGpio_config();
}
