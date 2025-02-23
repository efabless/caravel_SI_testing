#include <common.h>
#include "gpio_mgmt_tests.h"

void main()
{
    send_packet_test();
    receive_packet_test();
    uart_io();
}