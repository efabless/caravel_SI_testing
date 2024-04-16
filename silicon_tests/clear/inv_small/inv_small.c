#include <common.h>
#include "../bit_streams/and_3.h"

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
    //Blizzard
    // reg_mprj_datal &= 0x0;
    // reg_mprj_datal = 0x100;
    // delay(2);
    // for (unsigned int i = 0; i < inv_small_size; i++)
    // {
    //     int xdata = inv_small[i];
    //     // int xdata =0x0F;
    //     unsigned int io_data = 0;
    //     for (int j = 0; j < 8; j++) {
    //         io_data = (xdata & 0x1) ? 0x2100 : 0x100;
    //         // | 0x280 : io_data & 0xFFFFFDFF;
    //         reg_mprj_datal = io_data;
    //         // toggle prog clk
    //         io_data = (xdata & 0x1) ? 0x2180 : 0x180;
    //         reg_mprj_datal = io_data;
    //         // prog clk 0
    //         io_data = (xdata & 0x1) ? 0x2100 : 0x100;
    //         reg_mprj_datal = io_data;
    //         // reg_mprj_datal &= clk_zero_mask;
    //         // reg_mprj_datal |= clk_one_mask;
    //         xdata = xdata >> 1;
    //     }
    // }
    // // prog clk 0
    // reg_mprj_datal &= 0x2100;
    // reg_mprj_datal |= 0x1100;
    // delay(2);
    // reg_mprj_datal &= 0x1100;
    // reg_mprj_datal |= 0x5100;
    // reg_mprj_datal |= 0x5300;
    // delay(2);

    //Clear
    reg_mprj_datal = 0x0;
    delay(1);
    reg_mprj_datal = 0x100;
    delay(2);
    unsigned int io_data = 0;
    for (unsigned int i = 0; i < and_3_size; i++)
    {
        int xdata = and_3[i];
        // int xdata =0x0F;
        io_data = 0;
        for (int j = 0; j < 8; j++) {
            io_data = (xdata & 0x1) ? 0x2100 : 0x100;
            // | 0x280 : io_data & 0xFFFFFDFF;
            reg_mprj_datal = io_data;
            // toggle prog clk
            io_data = (xdata & 0x1) ? 0x2180 : 0x180;
            reg_mprj_datal = io_data;
            // prog clk 0
            io_data = (xdata & 0x1) ? 0x2100 : 0x100;
            reg_mprj_datal = io_data;
            // reg_mprj_datal &= clk_zero_mask;
            // reg_mprj_datal |= clk_one_mask;
            xdata = xdata >> 1;
        }
    }
    // prog clk 0
    reg_mprj_datal = io_data & 0x2100;
    reg_mprj_datal = io_data | 0x1100;
    delay(2);
    reg_mprj_datal = io_data & 0x1100;
    reg_mprj_datal = io_data | 0x5100;
    reg_mprj_datal = io_data | 0x5980;
    delay(2);
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
    configure_gpio(29, GPIO_MODE_USER_STD_INPUT_PULLUP);
    configure_gpio(34, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(35, GPIO_MODE_USER_STD_INPUT_PULLUP);
    configure_gpio(37, GPIO_MODE_USER_STD_INPUT_NOPULL);

    // ==
    configure_gpio(7, GPIO_MODE_MGMT_STD_OUTPUT); // connected to prog_clk
    configure_gpio(8, GPIO_MODE_MGMT_STD_OUTPUT); // connected to prog_rst
    configure_gpio(11, GPIO_MODE_MGMT_STD_OUTPUT); // connected to op_rst
    configure_gpio(12, GPIO_MODE_MGMT_STD_OUTPUT); // connected to isol_n
    configure_gpio(13, GPIO_MODE_MGMT_STD_OUTPUT); // connected to ccff_head
    configure_gpio(14, GPIO_MODE_MGMT_STD_OUTPUT); // connected to clk_sel

    // and gate
    configure_gpio(21, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(20, GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    configure_gpio(19, GPIO_MODE_USER_STD_OUTPUT);

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
