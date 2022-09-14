#include <defs.h>
//#include "../local_defs.h"
//#include "../stub.c"

//#include "../config_io.h"
//#include "../defs_mpw-two-mfix.h"

// --------------------------------------------------------
// Firmware routines
// --------------------------------------------------------

/* 
This test is for testing if protocol can of testing can use only mgmt gpio without the timers
the test would send 3 types of pulses each for 5 times, the purpose is to see if the observer can 
diffrentiate between the pulses of each time so we can depend on it in the testing without using timers 
if timers has a problem.
*/
void main()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;

    // longest pulses 
    for (int i = 0; i < 5; i++){
        reg_gpio_out = 1;
        for (int j = 0; j < 1000; j++);
        reg_gpio_out = 0;
        for (int j = 0; j < 1000; j++);   
    }

    // reset for long time
    reg_gpio_out = 0;
    for (int i = 0; i < 2000; i++);   

    // meduim pulses 
    for (int i = 0; i < 5; i++){
        reg_gpio_out = 1;
        for (int j = 0; j < 500; j++);
        reg_gpio_out = 0;
        for (int j = 0; j < 500; j++);   
    }

    // reset for long time
    reg_gpio_out = 0;
    for (int i = 0; i < 2000; i++); 

    // small  pulses 
    for (int i = 0; i < 5; i++){
        reg_gpio_out = 1;
        for (int j = 0; j < 100; j++);
        reg_gpio_out = 0;
        for (int j = 0; j < 100; j++);   
    }

}
