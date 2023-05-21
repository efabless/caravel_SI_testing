#include "soc_tests.h"
#include <common.h>

void main()
{
    config_uart();
    print("Start Test: cpu_stress\n");
    if (cpu_stress())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: hk_regs_wr_wb_cpu\n");
    if (hk_regs_wr_wb_cpu())
        print("passed\n");
    else
        print("failed\n");

    if (IRQ_external())
        print("passed\n");
    else
        print("failed\n");

    if (IRQ_external2())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: IRQ_spi\n");
    if (IRQ_spi())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: IRQ_timer\n");
    if (IRQ_timer())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: IRQ_uart\n");
    if (IRQ_uart())
        print("passed\n");
    else
        print("failed\n");

    if (IRQ_uart_rx())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: timer0_oneshot\n");
    if (timer0_oneshot())
        print("passed\n");
    else
        print("failed\n");

    config_uart();
    print("Start Test: timer0_periodic\n");
    if (timer0_periodic())
        print("passed\n");
    else
        print("failed\n");
}
