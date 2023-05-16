// #include "includes.h"
#include <common.h>

bool IRQ_external()
{
    uint16_t data;
    int i;

    flag = 0;
    configure_mgmt_gpio();

    // setting bit 7 as input
    reg_mprj_io_7 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    // gpio_config_io();
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1)
        ;

    irq_setmask(0);
    irq_setie(1);

    // irq_setmask(irq_getmask() | (1 << TIMER0_INTERRUPT));

    // irq_setmask(irq_getmask() | 0x3f);
    irq_setmask(irq_getmask() | (1 << USER_IRQ_4_INTERRUPT));
    // irq_setmask(irq_getmask() | ( 0x3f));
    reg_user4_irq_en = 1;
    reg_irq_source = 1;
    send_packet(1); // wait for environment to make mprj[7] high

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 10000000;
    //    int timeout = 100000000;

    for (int i = 0; i < timeout; i++)
    {
        if (flag == 1)
        {
            send_packet(5); // test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass)
    {
        return false;
    }

    return true;
}

bool IRQ_external2()
{

    uint16_t data;
    int i;

    flag = 0;
    configure_mgmt_gpio();

    // setting bit 7 as input
    reg_mprj_io_12 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    // gpio_config_io();
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1)
        ;

    irq_setmask(0);
    irq_setie(1);

    // irq_setmask(irq_getmask() | (1 << TIMER0_INTERRUPT));

    // irq_setmask(irq_getmask() | 0x3f);
    irq_setmask(irq_getmask() | (1 << USER_IRQ_5_INTERRUPT));
    // irq_setmask(irq_getmask() | ( 0x3f));
    reg_user5_irq_en = 1;
    reg_irq_source = 2;
    send_packet(1); // wait for environment to make mprj[7] high

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 10000000;
    //    int timeout = 100000000;

    for (int i = 0; i < timeout; i++)
    {
        if (flag == 1)
        {
            send_packet(5); // test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass)
    {
        return false;
    }

    return true;
}

bool IRQ_spi()
{
    clear_flag();
    configure_mgmt_gpio();
    enable_hk_spi_irq(1);
    user_irq_0_ev_pending_write(1);
    send_packet(2); //
    reg_hkspi_irq = 1;
    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 400000;

    for (int i = 0; i < timeout; i++)
    {
        if (get_flag() == 1)
        {
            send_packet(5); // test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass)
    {
        return false;
    }

    // finish test
    return true;
}

bool IRQ_timer()
{
    clear_flag();
    configure_mgmt_gpio();
    enable_timer0_irq(1);
    timer0_ev_pending_write(1);
    timer0_oneshot_configure(10000);

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 500000;
    send_packet(1);

    for (int i = 0; i < timeout; i++)
    {
        if (get_flag() == 1)
        {
            send_packet(5); // test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass)
    {
        return false;
    }

    // finish test
    return true;
}

bool IRQ_uart()
{

    clear_flag();
    configure_mgmt_gpio();
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    gpio_config_load();
    enable_uart_tx_irq(1);
    uart_ev_pending_write(1);
    send_packet(1); // sending data through the uart
    print("M");

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 400000;

    for (int i = 0; i < timeout; i++)
    {
        if (get_flag() == 1)
        {
            send_packet(5); // test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass)
    {
        return false;
    }

    return true;
}

bool IRQ_uart_rx()
{

    clear_flag();
    configure_mgmt_gpio();
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    gpio_config_load();
    uart_RX_enable(1);
    enable_uart_rx_irq(1);
    uart_ev_pending_write(1);
    send_packet(2); // sending data through the uart rx
    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 400000;

    for (int i = 0; i < timeout; i++)
    {
        if (get_flag() == 1)
        {
            send_packet(5); // test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass)
    {
        return false;
    }

    return true;
}

void main()
{
    configure_mgmt_gpio();
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    gpio_config_load();
    enable_uart_TX(1);
    bool test;
    print("Start Test: IRQ_timer\n");
    // test = IRQ_external();
    // if (test == true)
    // {
    //     send_packet(3);
    //     send_packet(3);
    //     send_packet(3);
    // }
    // else
    // {
    //     send_packet(9);
    // }

    // send_packet(10);

    // test = IRQ_external2();
    // if (test == true)
    // {
    //     send_packet(3);
    //     send_packet(3);
    //     send_packet(3);
    // }
    // else
    // {
    //     send_packet(9);
    // }

    // send_packet(10);

    test = IRQ_timer();

    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    gpio_config_load();
    enable_uart_TX(1);
    if (test == true)
    {
        print("passed");
    }
    else
    {
        send_packet("Failed");
    }

    // print("Start Test: IRQ_spi\n");

    // test = IRQ_spi();
    // if (test == true)
    // {
    //     send_packet(3);
    //     send_packet(3);
    //     send_packet(3);
    // }
    // else
    // {
    //     send_packet(9);
    // }

    // send_packet(10);

    // test = IRQ_uart();
    // if (test == true)
    // {
    //     send_packet(3);
    //     send_packet(3);
    //     send_packet(3);
    // }
    // else
    // {
    //     send_packet(9);
    // }

    // send_packet(10);

    // test = IRQ_uart_rx();
    // if (test == true)
    // {
    //     send_packet(3);
    //     send_packet(3);
    //     send_packet(3);
    // }
    // else
    // {
    //     send_packet(9);
    // }
}