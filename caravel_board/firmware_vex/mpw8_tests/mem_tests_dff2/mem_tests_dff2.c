#include "mem_tests_dff2.h"
#include <common.h>

void main()
{
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

    config_uart();
    print("End Test\n");
    HKGpio_config();
}
