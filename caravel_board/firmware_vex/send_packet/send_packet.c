#define  PULSE_WIDTH   500
 

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

// used to make 1-> 0 pulse if is pulse = 1 if is_pulse = 0 send high signal for pulse period 
void send_pulse(int is_pulse){
    reg_gpio_out = 1;
    count_down(PULSE_WIDTH);
    reg_gpio_out = (~is_pulse) & 0x1;
    count_down(PULSE_WIDTH);  
}


// used to make 1-> 0 pulse if is pulse = 1 if is_pulse = 0 send high signal for pulse period 
void send_packet(int num_pulses){
    //start of packet
    reg_gpio_out = 0;
    count_down(PULSE_WIDTH);
    // send pulses
    for (int i = 0; i < num_pulses; i++){
        send_pulse(1);
    }
    // end of packet
    for (int i = 0; i < 20-num_pulses; i++){
        send_pulse(0);
    }
}
void configure_mgmt_gpio(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;	// Fixed for full swing operation
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // default
}

