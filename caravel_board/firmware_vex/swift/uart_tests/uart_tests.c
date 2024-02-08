#include "uart_tests.h"
#include <common.h>

void main()
{
    configure_mgmt_gpio();
    send_packet(1); // Start uart test
    uart();
    send_packet(1); // Start uart_reception test
    uart_reception();
    send_packet(1); // Start uart_loopback test
    uart_loopback();
    send_packet(1); // Start IRQ_uart_rx test
    IRQ_uart_rx();
}