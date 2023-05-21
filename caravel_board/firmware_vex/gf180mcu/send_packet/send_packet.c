#include <common.h>

void send_packet_test()
{

    configure_mgmt_gpio();

    configure_gpio(1, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(2, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(3, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(4, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    gpio_config_load();

    count_down(PULSE_WIDTH*50);
    // Uncomment the while() loop to make this continuous
    // while (1) {
	send_packet(1);
    count_down(PULSE_WIDTH*10);
	send_packet(2);
    count_down(PULSE_WIDTH*10);
	send_packet(3);
    count_down(PULSE_WIDTH*10);
	send_packet(4);
    count_down(PULSE_WIDTH*10);
	send_packet(5);
    count_down(PULSE_WIDTH*10);
	send_packet(6);
    count_down(PULSE_WIDTH*10);
	send_packet(7);
    count_down(PULSE_WIDTH*10);
	send_packet(8);
	
    while(1);
	// count_down(1000000);

    // }
}
