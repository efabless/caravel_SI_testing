#include <defs.h>
//#include "../local_defs.h"
//#include "../stub.c"

//#include "../config_io.h"
//#include "../defs_mpw-two-mfix.h"
// #include "send_packet.c"

// --------------------------------------------------------
// Firmware routines
// --------------------------------------------------------


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

/* 
This test is for testing if protocol can of testing can use only mgmt gpio with the timers
the test would send 3 types of pulses each for 5 times, the purpose is to see if the observer can 
diffrentiate between the pulses of each time so we can depend on it in the testing without using timers 
if timers has a problem.
*/
void main()
{
        // configure 
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;	// Fixed for full swing operation
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // default

    // small pulses 
    for (int i = 0; i < 10; i++){
        reg_gpio_out = 1;
        count_down(2500000);
        reg_gpio_out = 0;
        count_down(2500000);   
    }

    // meduim pulses 
    for (int i = 0; i < 10; i++){
        reg_gpio_out = 1;
        count_down(1000000);
        reg_gpio_out = 0;
        count_down(1000000);   
    }

    // long  pulses 
    for (int i = 0; i < 10; i++){
        reg_gpio_out = 1;
        count_down(500000);
        reg_gpio_out = 0;
        count_down(500000);   
    }

    // longest  pulses 
    for (int i = 0; i < 10; i++){
        reg_gpio_out = 1;
        count_down(250000);
        reg_gpio_out = 0;
        count_down(250000);   
    }

}
