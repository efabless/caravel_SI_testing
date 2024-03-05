#include "soc_tests.h"
#include <common.h>

void main()
{
    // HKGpio_config();
    // while (1)
    // {
    //     HKGpio_config();
    configure_mgmt_gpio_input();
    if (reg_gpio_in == 0){
        config_uart_ios();
        config_uart();
        print("ST: cpu_stress\n");
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
        print("ST: hk_regs_wr_wb_cpu\n");
        if (hk_regs_wr_wb_cpu())
        {
            config_uart_ios();
            config_uart();
            print("passed\n");
        }
        else
        {   
            config_uart_ios();
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
        print("ST: IRQ_spi\n");
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
        print("ST: IRQ_timer\n");
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
        print("ST: IRQ_uart\n");
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
        print("ST: timer0_oneshot\n");
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
        print("ST: timer0_periodic\n");
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
        // HKGpio_config();
        config_uart();
        print("End Test\n");
    }
    // };

    HKGpio_config();
}
