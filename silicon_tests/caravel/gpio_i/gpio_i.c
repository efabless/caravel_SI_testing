#include <common.h>
#define PULSE_WIDTH 100000

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

// void uart_puti(int c){
//     while (reg_uart_txfull == 1);
// 	reg_uart_data = c;
// }
void main()
{
        int io_number;
        int count = 0;
        int mask;
        int recieved;
        int old_recieved;
        int temp_io = 0;
        int timeout = 10000;
        long int timeout_count = 0;
        char *c;
        configure_all_gpios(GPIO_MODE_MGMT_STD_INPUT_NOPULL);
        configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
        set_gpio_h(0);
        set_gpio_l(0);
        gpio_config_load();
        config_uart();
        print("Start Test: gpio_i\n");

    while (true)
    {
        c = uart_get_line();
        io_number = get_int_from_string(c);
        if (io_number >= 32)
        {
            temp_io = io_number - 32;
            mask = 0x1 << temp_io;
            old_recieved = get_gpio_h() & mask;
        }
        else
        {
            mask = 0x1 << io_number;
            old_recieved = get_gpio_l() & mask;
        }
        while (true)
        {
            if (io_number >= 32)
            {
                recieved = get_gpio_h() & mask; // mask gpio bit
            }
            else
            {
                recieved = get_gpio_l() & mask; // mask gpio bit
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
                count_down(PULSE_WIDTH);
                print("f\n");
            }
        }
        count_down(PULSE_WIDTH);
        print("p\n");
        count = 0;
    }
}
