#include <common.h>
#include "../bit_streams/and2.h"

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


void process_bit_stream() {

    reg_mprj_datal = 0x0;
    //prog_rst 1
    reg_mprj_datal = 0x80000;
    unsigned int io_data;
    for (unsigned int i = 0; i < and2_size; i++)
    {
        int xdata = and2[i];
        // int xdata =0x0F;
        io_data = 0;
        for (int j = 0; j < 8; j++) {
            //ccff_head
            io_data = (xdata & 0x1) ? 0x180000 : 0x80000;
            reg_mprj_datal = io_data;
            // toggle prog clk
            io_data = (xdata & 0x1) ? 0x1180000 : 0x1080000;
            reg_mprj_datal = io_data;
            // prog clk 0
            io_data = (xdata & 0x1) ? 0x180000 : 0x80000;
            reg_mprj_datal = io_data;
            xdata = xdata >> 1;
        }
    }
    // prog clk 0
    reg_mprj_datal = io_data & 0x180000;
    // isol_n 1 prog_rst 1 while keeping ccff_head
    reg_mprj_datal = io_data | 0xA0000;
    // ccff_head 0 isol_n 1 prog_rst 1
    reg_mprj_datal = io_data & 0xA0000;
    // clk_sel 1 head 0 isol_n 1 prog_rst 1
    reg_mprj_datal = io_data | 0x2A0000;
    // op_rst 1 clk_sel 1 head 0 isol_n 1 prog_rst 1
    reg_mprj_datal = io_data | 0x2E0000;
}

void main()
{

    // FPGA IOs
    configure_gpio(1, GPIO_MODE_USER_STD_INPUT_NOPULL);
    //Clear
    configure_gpio(9, GPIO_MODE_USER_STD_INPUT_NOPULL);

    configure_gpio(23, GPIO_MODE_USER_STD_OUTPUT);
    configure_gpio(29, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(34, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(35, GPIO_MODE_USER_STD_INPUT_NOPULL);
    configure_gpio(37, GPIO_MODE_USER_STD_INPUT_NOPULL);

    // Caravel MGMT IOs
    configure_gpio(24, GPIO_MODE_MGMT_STD_OUTPUT); // connected to prog_clk
    configure_gpio(19, GPIO_MODE_MGMT_STD_OUTPUT); // connected to prog_rst
    configure_gpio(18, GPIO_MODE_MGMT_STD_OUTPUT); // connected to op_rst
    configure_gpio(17, GPIO_MODE_MGMT_STD_OUTPUT); // connected to isol_n
    configure_gpio(20, GPIO_MODE_MGMT_STD_OUTPUT); // connected to ccff_head
    configure_gpio(21, GPIO_MODE_MGMT_STD_OUTPUT); // connected to clk_sel

    // and gate
    configure_gpio(31, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // in[121] -> GPIO[31]
    configure_gpio(32, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // in[120] -> GPIO[32]
    configure_gpio(30, GPIO_MODE_USER_STD_OUTPUT); // out[122] -> GPIO[30]

    // configure_gpio(33, GPIO_MODE_USER_STD_OUTPUT); // 13 a[0] -> GPIO[21]
    // configure_gpio(32, GPIO_MODE_USER_STD_INPUT_PULLDOWN); // 13 a[0] -> GPIO[21]
    // configure_gpio(31, GPIO_MODE_USER_STD_INPUT_PULLDOWN);  // 42 b[4] -> GPIO[5]

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
