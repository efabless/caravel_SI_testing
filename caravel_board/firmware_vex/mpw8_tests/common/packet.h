#ifndef PACKET_C_HEADER_FILE
#define PACKET_C_HEADER_FILE

#include <timer0.h>
#include <mgmt_gpio.h>
#define  PULSE_WIDTH   2500000
 
/**
 * Performs a countdown using timer0.
 * 
 * @param d The duration of the countdown in timer ticks.
 * @return None.
 */
void count_down(const int d)
{
    /* Configure timer for a single-shot countdown */
    timer0_oneshot_configure(d);
    
    // Loop, waiting for value to reach zero
    update_timer0_val(); // latch current value
    int old_val = get_timer0_val();
    while (old_val > 0) {
        update_timer0_val();
        old_val = get_timer0_val();
    }
}

void send_pulse(){
    mgmt_gpio_wr(0);
    count_down(PULSE_WIDTH);
    mgmt_gpio_wr(1);
    count_down(PULSE_WIDTH);  
}

/**
 * Sends a packet by emitting a series of pulses, where the number of pulses is
 * determined by the num_pulses parameter. After sending the pulses, the
 * function waits for a duration of PULSE_WIDTH*10 before ending the packet.
 *
 * @param num_pulses The number of pulses to send in the packet.
 */
void send_packet(int num_pulses){
    // send pulses
    for (int i = 0; i < num_pulses+1; i++){
        send_pulse();
    }
    // end of packet
    count_down(PULSE_WIDTH*10);
}


/**
 * Configures management GPIO.
 *
 * This function sets the necessary register values for full swing operation, 
 * enables management gpio and configures as output, sets the default output value to 1, and waits 
 * for a certain amount of time.
 *
 * @param None
 *
 * @return None
 */

void configure_mgmt_gpio(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;	// Fixed for full swing operation
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // default
    count_down(PULSE_WIDTH*20);
}

#endif // PACKET_C_HEADER_FILE
