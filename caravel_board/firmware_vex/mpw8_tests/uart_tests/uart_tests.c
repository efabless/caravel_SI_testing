#include "uart_tests.h"
#include <common.h>

void main()
{
    configure_mgmt_gpio();
    send_packet(1); // Start uart test
    uart();
    enable_uart_TX(0);
    empty_buffer();
    send_packet(1); // Start uart_io test
    uart_io();
    enable_uart_TX(0);
    empty_buffer();
    send_packet(1); // Start uart_reception test
    uart_reception();
    enable_uart_TX(0);
    empty_buffer();
    send_packet(1); // Start uart_loopback test
    uart_loopback();
}