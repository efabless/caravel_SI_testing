#include <common.h>

void send_packet_test()
{
    configure_mgmt_gpio();
	send_packet(8);
}
