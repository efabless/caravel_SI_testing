#include <defs.h>

// #include "../send_packet/send_packet.h"
#include "send_packet.c"
#include "bitbang.c"

// --------------------------------------------------------
// GPIO configuration test
//
// Assorted attempts to understand what's going on inside
// the GPIO serial programming shift register.
//
// bitbang_flood is an update of bitbang_progression.
// The understanding is that each channel has either
// (1) a hold violation, (2) a data-dependent hold
// violation, or (3) neither ((3) has not been observed
// but is possible).
//
// bitbang_flood attempts to systematically determine
// the boundary conditions between each pair of GPIO
// control blocks.  The procedure is as follows:
//
// (1) GPIO 37 and 0 never have an error, and so they do
// not need to be checked.  GPIO 0 affects the processor
// by potentially putting it in debug mode, so keep GPIO 0
// turned off by ensuring that the low four bits are1
// (managment controlled, input and output disabled).
// GPIO 37 is free to use for input or output.  The
// management standalone GPIO is also free to use for
// input or output.
//
// (2) Analyze each side (GPIO1 to18, and GPIO19 to 36)
// independently, for simplicity.
//
// (3) At the start of each cycle, do a reset to ensure that
// the registers are all zeros.
//
// (4) Analyze each GPIO in turn, starting with the one
// closest to the processor (GPIO1 and GPIO 36).  Apply
// sequence1100000000001, adjusting for the effect of all
// GPIOs that come before it.  This sequence puts the GPIO
// in the state of managment control, output mode, with
// both output and input buffers enabled.
//
// (5) Clock this sequence in for the number of cycles
// known to be needed for all the GPIOs preceding it.
// Then clock an additional12 cycles, apply load, and
// test (apply output1 and 0 and read back each).  If
// the test is successful, then there is a simple hold
// violation at the start of the GPIO.
//
// (6) If the first test fails, then assume a data-dependent
// hold violation.  Add a1 to the run of ones in the
// sequence (e.g.,1110000000001) and repeat, but clocking
// an additional13 cycles instead of12.  Repeat the test.
// If the test is successful, then there is a data-dependent
// hold violation at the start of the GPIO.
//
// Note that if any GPIO has neither a simple hold violation
// or a data-dependent hold violation, then additional
// tests will be needed.
//
// To automate the test, use GPIO 37 as input and the
// standalone GPIO as output.  The program will run as
// follows:
//
// (1) Start with the left side (GPIO 36 to19).
// (2) Run1st test.
// (3) If and only if the test is successful, then the LED is lit,
// the GPIO test concludes with the GPIO known to have a simple
// hold violation.
// (4) If the test is unsuccessful, then the next test checks
// for a data-dependent hold violation.
// (5) If the 2nd test is successful, then the LED is lit, and
// the GPIO test conclues with the GPIO known to have a data-
// dependent hold violation.  The program waits for a pulse on
// input GPIO 37 and then proceeds to the test.
// (6) If the 2nd test is unsuccessful, then LED is off, the
// system has an unknown condition, and the program terminates
// with the LED running at a fast blink.  If this happens, the
// program must be reworked to determine the unknown condition
// and how to test for it.
// (7) The program logs the number of clocks needed to get to
// the GPIO (12 or13)
// (8) The program waits for a pulse on input GPIO 37 and then
// proceeds to the next GPIO (return to step 2).  If the left
// side is done, then the program continues with the right
// side.  When the left side analysis is complete, the LED
// runs with a slow blink.  When the analysis of either side is
// complete, the LED runs with a slow blink.
//
// The program will run a minimum of19 cycles (all channels
// have simple hold violations) or a maximum of 38 cycles
// (all channels have data-dependent hold violations) per
// side.  Note that if there are more than 9 data-dependent
// hold violations on a side, then it is not possible to
// configure a GPIO for input after the 9th one, and the
// test automatically fails.  This fact may limit the yield
// and render some chips unusable.
//
// This test can in principle be automated so that the
// intended GPIO state at run-time is set up in the program,
// the analyzing routine is called and runs without requiring
// input pulses on GPIO 37, and then the program automatically
// sets up the configuration for the intended run-time state
// and returns.  This manual analysis is only used to verify
// the assumptions under which the analysis is written.
//
// --------------------------------------------------------

// --------------------------------------------------------
// Main program entry point
// --------------------------------------------------------
/*
    configure the gpio[7:0] as mgmt output using bitbang then send the next pattern on them 
    gpio_7 10 10 10 10 10 10 10 10 
    gpio_6 00 10 10 10 10 10 10 10 
    gpio_5 00 00 10 10 10 10 10 10 
    gpio_4 00 00 00 10 10 10 10 10 
    gpio_3 00 00 00 00 10 10 10 10 
    gpio_2 00 00 00 00 00 10 10 10 
    gpio_1 00 00 00 00 00 00 10 10
    gpio_0 00 00 00 00 00 00 00 10 
    
    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ sending each pulse at gpio[7:0] 
        send packet size = 5  # betweeb each 2 3-packet size gpio[7:0] should be monitored
    @ finish test 
        send packet size = 3 
        send packet size = 3 
*/

void main()
{

    unsigned int i, j, k;
    uint32_t ddhold;
    configure_mgmt_gpio();
    reg_mprj_datal = 0;
    reg_mprj_datah = 0;

    // Set I/O to declare all I/O as output except 0 and 37.
    // 37 is an input, and 0 is turned off.  Note that
    // register 37 as input must have the high bit set, as
    // that bit slides into the next GPIO, which needs to be
    // tested under management control.  With the output
    // disabled by the input being enabled (see housekeeping.v
    // line 785), the output mode configuration is irrelevant
    // as long as it isn't zero.
    reg_mprj_io_7  = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_6  = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_5  = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_4  = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_3  = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2  = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_1  = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_0  = GPIO_MODE_MGMT_STD_OUTPUT;

    ddhold = 0;

    /* Enable one of the following two blocks for right or left side
     * configuration.
     */
    send_packet(1); // start of bitbang
    while (1) {
	clear_registers();	
    clock_in_right_i_left_o_standard(0); // 8	and 29	
    clock_in_right_i_left_o_standard(0); // 7	and 30	
    clock_in_right_i_left_o_standard(0); // 6	and 31	
    clock_in_right_i_left_o_standard(0); // 5	and 32	
    clock_in_right_i_left_o_standard(0); // 4	and 33	
    clock_in_right_i_left_o_standard(0); // 3	and 34	
    clock_in_right_i_left_o_standard(0); // 2	and 35	
    clock_in_right_i_left_o_standard(0); // 1	and 36	
    clock_in_right_i_left_o_standard(0); // 0	and 37	
    load();		                         //  load

    send_packet(2);// end of bitbang

	// Blink forever
	// Pulse N+1 times for channel N before the long pulse

        reg_mprj_datal = 0x00000000;
        reg_mprj_datah = 0x00000000;

	i = 0x80;
	for (j = 0; j < 8; j++) {
        send_packet(5);// sending pulses on gpio
        reg_mprj_datah = 0x3f;
        reg_mprj_datal = i;
        for (k = 0; k < 250; k++);
        reg_mprj_datah = 0x00;
        reg_mprj_datal = 0x00000000;
        for (k = 0; k < 250; k++);
        i >>=1;
        i |= 0x80;
	}

    for (j = 0; j < 40000; j++);

    send_packet(3);// sending pulses on gpio
    send_packet(3);// sending pulses on gpio
    send_packet(3);// sending pulses on gpio

   }
}