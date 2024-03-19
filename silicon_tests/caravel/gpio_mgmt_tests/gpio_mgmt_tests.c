#include <common.h>
#include "gpio_mgmt_tests.h"
#define PULSE_WIDTH 250000

void main()
{
    HKGpio_config();
    send_packet_test();
    receive_packet_test();
    uart_io();
}