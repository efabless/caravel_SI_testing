#include <common.h>
#include "../bit_streams/and_la.h"

#define PULSE_WIDTH 2500000


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
    reg_mprj_datal = 0x100;
    unsigned int io_data;
    for (unsigned int i = 0; i < and_la_size; i++)
    {
        int xdata = and_la[i];
        // int xdata =0x0F;
        io_data = 0;
        for (int j = 0; j < 8; j++) {
            io_data = (xdata & 0x1) ? 0x2100 : 0x100;
            // | 0x280 : io_data & 0xFFFFFDFF;
            reg_mprj_datal = io_data;
            // delay(10);
            // toggle prog clk
            io_data = (xdata & 0x1) ? 0x2180 : 0x180;
            reg_mprj_datal = io_data;
            // delay(10);
            // prog clk 0
            io_data = (xdata & 0x1) ? 0x2100 : 0x100;
            reg_mprj_datal = io_data;
            // delay(10);
            // reg_mprj_datal &= clk_zero_mask;
            // reg_mprj_datal |= clk_one_mask;
            xdata = xdata >> 1;
            // delay(10);
        }
    }
    // prog clk 0
    reg_mprj_datal = io_data & 0x2100;
    reg_mprj_datal = io_data | 0x1100;
    // delay(10);
    reg_mprj_datal = io_data & 0x1100;
    // delay(10);
    reg_mprj_datal = io_data | 0x5100;
    // delay(10);
    //Blizzard
    reg_mprj_datal = io_data | 0x5300;
    //Clear
    // reg_mprj_datal = io_data | 0x5900;
}

void main()
{
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

    // gpio_config_io();
    gpio_config_load();
    process_bit_stream();
    configure_mgmt_gpio();
    mgmt_gpio_wr(1);
    bool pass1 = false;
    bool pass2 = false;
    bool pass3 = false;
    bool pass4 = false;

    // a = la[126] b = la[125] c=la[124]
    // configure la_reg3 as input expect la[124] = reg3[28]
    set_la_ien(LA_REG_3,0xEFFFFFFF);
    set_la_oen(LA_REG_3,0x10000000);

    // a =1 b = 1 
    set_la_reg(LA_REG_3,0xFFFFFFFF);
    if (get_c() == 1)
    {
        send_packet(2);
        pass1 = true;
    }
    else{
        send_packet(9);
        pass1 = false;
    }
    
    // a =1 b = 0 
    set_la_reg(LA_REG_3,0x40000000);
    if (get_c() == 0)
    {
        send_packet(2);
        pass2 = true;
    }
    else{
        send_packet(9);
        pass2 = false;
    }

    // a =0 b = 1 
    set_la_reg(LA_REG_3,0x20000000);
    if (get_c() == 0)
    {
        send_packet(2);
        pass3 = true;
    }
    else{
        send_packet(9);
        pass3 = false;
    }

    // a =0 b = 0 
    set_la_reg(LA_REG_3,0x0);
    if (get_c() == 0)
    {
        send_packet(2);
        pass4 = true;
    }
    else{
        send_packet(9);
        pass4 = false;
    }

    if (pass1 == true && pass2 == true && pass3 == true && pass4 == true)
    {
        mgmt_gpio_wr(0);
    }
    else{
        mgmt_gpio_wr(1);
    }
}

int get_c(){
    int c = get_la_reg(LA_REG_3);
    // mask C value
    c = c >> 28;
    c = c & 1;
    return c; 
}
