#include "uart_tests.h"
#include <common.h>

void main()
{
    configure_mgmt_gpio();
    send_packet(1); // Start uart_io test
    uart_io();
    send_packet(1); // Start uart test
    uart();
    send_packet(1); // Start uart_reception test
    uart_reception();
    send_packet(1); // Start uart_loopback test
    uart_loopback();

    configure_gpio_default();
    gpio_config_load();
}