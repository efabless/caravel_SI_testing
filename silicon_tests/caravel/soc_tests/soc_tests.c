#include "soc_tests.h"
#include <common.h>

void main()
{
    configure_mgmt_gpio_input();
    if (reg_gpio_in == 0){
        config_uart();
        print("Start Test: cpu_stress\n");
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
        config_uart();
        print("End Test\n");
    }
    HKGpio_config();
}
