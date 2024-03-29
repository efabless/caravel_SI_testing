#include "mem_tests_dff.h"
#include <common.h>

void main()
{
    config_uart();
    print("Start Test: mem_dff_halfW\n");
    if (mem_dff_halfW())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_dff_test\n");
    if (mem_dff_test())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: mem_dff_W\n");
    if (mem_dff_W())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("End Test\n");
}
