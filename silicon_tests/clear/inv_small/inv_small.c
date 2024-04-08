#include <common.h>
#include "../bit_streams/inv_1.h"

#define clk_zero_mask 0xFFFFFF7F
#define clk_one_mask 0x00000080


void delay(int delayTime) {
    // Declare the counter as volatile to ensure the compiler does not optimize the loop away
    volatile int i;
    
    // Loop for the specified delayTime; the exact duration of delay depends on the
    // system's clock speed and the compiler's optimization settings
    for(i = 0; i < delayTime; i++) {
        // Empty loop body; the volatile keyword ensures that the loop is not optimized away
    }
}


// void process_bit_stream() {
//     for (unsigned int i = 0; i < and_3_size; ++i) {
//         // Process each bit in the byte
//         for (int j = 7; j >= 0; --j) {
//             int bit_zero_edge = (and_3[i] << (9-j) ) & 0x300 ;
//             int bit_high_edge = bit_zero_edge | 0x80;
//             // reg_mprj_datal = bit_zero_edge;
//             reg_mprj_datal = bit_high_edge;
//             // delay(1);
//             reg_mprj_datal = bit_zero_edge;
//             // delay(1);
//         }
//         // print("o");
//     }
// }

void process_bit_stream() {
    reg_mprj_datal &= 0x100;
    for (unsigned int i = 0; i < inv_1_size; i++)
    {
        int xdata = inv_1[i];
        // int xdata =0x0F;
        unsigned int io_data = 0;
        for (int j = 0; j < 8; j++) {
            io_data = (xdata & 0x1) ? 0x900 : 0x100;
            // | 0x280 : io_data & 0xFFFFFDFF;
            reg_mprj_datal = io_data;
            io_data = (xdata & 0x1) ? 0x980 : 0x180;
            reg_mprj_datal = io_data;
            // reg_mprj_datal &= clk_zero_mask;
            // reg_mprj_datal |= clk_one_mask;
            xdata = xdata >> 1;
        }
    }
    reg_mprj_datal = reg_mprj_datal | 1 << 12;
    reg_mprj_datal = reg_mprj_datal | 1 << 13;
}

void main()
{
    // HKGpio_config();
    // configure_mgmt_gpio_input();
    // while (1)
    // {
    // if (reg_gpio_in == 0) {
    // FPGA IOs
    configure_gpio(1, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(9, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(23, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(29, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(34, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(35, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(37, GPIO_MODE_USER_STD_INPUT_NOPULL);

    // ==
    configure_gpio(7, GPIO_MODE_MGMT_STD_OUTPUT); // connected to prog_clk
    configure_gpio(8, GPIO_MODE_MGMT_STD_OUTPUT); // connected to prog_rst
    configure_gpio(11, GPIO_MODE_MGMT_STD_OUTPUT); // connected to ccff_head
    configure_gpio(12, GPIO_MODE_MGMT_STD_OUTPUT); // connected to isol_n
    configure_gpio(13, GPIO_MODE_MGMT_STD_OUTPUT); // connected to op_rst

    // inv_small
    configure_gpio(21, GPIO_MODE_USER_STD_OUTPUT); // 13 a[0] -> GPIO[21]
    configure_gpio(5, GPIO_MODE_USER_STD_INPUT_PULLDOWN);  // 42 b[4] -> GPIO[5]

    // gpio_config_io();
    gpio_config_load();
    // config_uart();
    // print("ST: and_gate\n");
    process_bit_stream();

    // print("DP\n");
    configure_mgmt_gpio();
    while (1){
        send_packet(8);
    }
    // }
    // else
    // HKGpio_config();
    // };
} 
