#define  BIT_WIDTH   500

void count_down(const int d)
{
    /* Configure timer for a single-shot countdown */
    reg_timer0_config = 0;
    reg_timer0_data = d;
    reg_timer0_config = 1; /* Enabled, one-shot, down count */

    // Loop, waiting for value to reach zero
    reg_timer0_update = 1;  // latch current value
    while (reg_timer0_value > 0) {
        reg_timer0_update = 1;
    }
}


// use to send frame from 0 to 255 
void send_frame(int data){
    //start of frame
    reg_gpio_out = 0;
    count_down(BIT_WIDTH);
    int bit;
    // send bits
    for (int i = 0; i < 8; i++){
        bit = (data >> 7);
        data = (data << 1) & 255;
        reg_gpio_out = bit;
        count_down(BIT_WIDTH);
    }
    // end of frame
    reg_gpio_out = 1;
    count_down(BIT_WIDTH);
}
void configure_mgmt_gpio(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;	// Fixed for full swing operation
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // default
}

