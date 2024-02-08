#include "soc_tests.h"
#include <firmware_apis.h>

void main()
{
    config_uart();
    print("Start Test: cpu_stress\n");
    count_down(PULSE_WIDTH*10);
    if (cpu_stress())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    config_uart();
    print("Start Test: hk_regs_wr_wb_cpu\n");
    // count_down(PULSE_WIDTH*10);
    if (hk_regs_wr_wb_cpu())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    if (IRQ_external())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    if (IRQ_external2())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    config_uart();
    print("Start Test: IRQ_spi\n");
    // count_down(PULSE_WIDTH*10);
    if (IRQ_spi())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    config_uart();
    print("Start Test: IRQ_timer\n");
    // count_down(PULSE_WIDTH*10);
    if (IRQ_timer())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    config_uart();
    print("Start Test: IRQ_uart\n");
    // count_down(PULSE_WIDTH*10);
    if (IRQ_uart())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    config_uart();
    print("Start Test: timer0_oneshot\n");
    // count_down(PULSE_WIDTH*10);
    if (timer0_oneshot())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    config_uart();
    print("Start Test: timer0_periodic\n");
    // count_down(PULSE_WIDTH*10);
    if (timer0_periodic())
    {
        config_uart();
        print("passed\n");
    }
    else
    {
        config_uart();
        print("failed\n");
    }

    // if (IRQ_uart_rx())
    // {
    //     config_uart();
    //     print("passed\n");
    // }
    // else
    // {
    //     config_uart();
    //     print("failed\n");
    // }
    config_uart();
    print("End Test\n");
    HKGpio_config();
}
