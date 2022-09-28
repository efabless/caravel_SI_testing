#include "../defs.h"
#include "../gpio_config/gpio_config_io.c"
#include "../silicon_tests/common/recieve_packet.c"
//#include "../local_defs.h"
//#include "../stub.c"
//#include "../config_io.h"
//#include "../defs_mpw-two-mfix.h"


void set_registers() {

    reg_mprj_io_0 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_5 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_7 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_8 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_9 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_10 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_11 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_12 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_13 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_14 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_15 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_16 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_17 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_18 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;

}
/*
@ send on the next io (start from 0 to 18)
    send packet with size 1
@ recieving packet of size n 
    wait for 4 pulses on gpio
@ recieved 4 pulses on gpio #
    send packet of size 3 
@timeout doesn't recieve 4 pulses on gpio # 
    send packet of size 5

*/
void main()
{
	int i,j;
    int num_pulses = 4;
    int io_number = -1;
    int count = 0;
    int mask; 
    int recieved; 
    int old_recieved; 
    int timeout = 1000;
    long int timeout_count = 0;
    set_registers();
    reg_mprj_datah = 0;
    reg_mprj_datal = 0;
    configure_mgmt_gpio();
    gpio_config_io();
    // send_packet(1); // configuration finished start test

    while (true){
        send_packet(1); // send on the next io
        io_number++;
        mask = 0x1 << io_number;
        old_recieved = reg_mprj_datal & mask;
        while(true){
            recieved = reg_mprj_datal & mask; // mask gpio bit
           if (recieved != old_recieved){
                count++;
                old_recieved = recieved;
                timeout_count = 0;
            }else{
                timeout_count++;
            }
            if (count == 10)
                break;
            if (timeout_count > timeout){
                while (true)
                    send_packet(5); // timeout
                return;
            }
        }
        count_down(PULSE_WIDTH*20);
        send_packet(3); // ack recieving packet on io
        count=0;
    }
}

