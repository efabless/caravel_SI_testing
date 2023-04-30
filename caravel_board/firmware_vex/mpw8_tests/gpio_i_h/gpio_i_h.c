#include <defs.h>
#include <stub.c>
#include "../common/send_packet.c"
#include "../../gpio_config/gpio_config_io.c"

void set_registers()
{
    reg_mprj_io_19 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_20 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_21 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_22 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_23 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_24 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_25 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_26 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_27 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_28 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_29 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_30 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_31 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_32 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_33 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_34 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    //    reg_mprj_io_34 = 0x0403;
    reg_mprj_io_35 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_36 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_37 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    //    reg_mprj_io_37 = 0x0403;
}
/*
@ send on the next io (start from 37 to 19)
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
    int i, j;
    int num_pulses = 4;
    int io_number = 38;
    int count = 0;
    int mask;
    int recieved;
    int temp_io = 0;
    int old_recieved;
    int timeout = 15000;
    long int timeout_count = 0;
    set_registers();
    reg_mprj_datah = 0;
    reg_mprj_datal = 0;
    configure_mgmt_gpio();
//    gpio_config_io();
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);
    // send_packet(1); // configuration finished start test

    while (true)
    {
        send_packet(1); // send on the next io
        io_number--;
        if (io_number >= 32)
        {
            temp_io = io_number - 32;
            mask = 0x1 << temp_io;
            old_recieved = reg_mprj_datah & mask;
        }
        else
        {
            mask = 0x1 << io_number;
            old_recieved = reg_mprj_datal & mask;
        }

        while (true)
        {
            if (io_number >= 32)
            {
                recieved = reg_mprj_datah & mask; // mask gpio bit
            }
            else
            {
                recieved = reg_mprj_datal & mask; // mask gpio bit
            }
            if (recieved != old_recieved)
            {
                count++;
                old_recieved = recieved;
                timeout_count = 0;
            }
            else
            {
                timeout_count++;
            }
            if (count == 10)
                break;
            if (timeout_count > timeout)
            {
                while (true)
                    send_packet(5); // timeout
                return;
            }
        }
        count_down(PULSE_WIDTH * 20);
        send_packet(3); // ack recieving packet on io
        count = 0;
    }
}
