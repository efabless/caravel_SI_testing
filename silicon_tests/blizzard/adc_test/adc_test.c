#include <common.h>

// --------------------------------------------------------
// Firmware routines
// --------------------------------------------------------

void delay(const int d)
{

    /* Configure timer for a single-shot countdown */
    reg_timer0_config = 0;
    reg_timer0_data = d;
    reg_timer0_config = 1;

    // Loop, waiting for value to reach zero
    reg_timer0_update = 1; // latch current value
    while (reg_timer0_value > 0)
    {
        reg_timer0_update = 1;
    }
}

#define DAC_BASE 0x30040000
#define ADC_BASE 0x30080000

#define ADC_CTRL_SOC 0x1
#define ADC_CTRL_EN 0x2

#define dac_data_reg (*(volatile uint32_t *)(DAC_BASE + 0))
#define dac_ena_reg (*(volatile uint32_t *)(DAC_BASE + 4))

#define adc_ctrl_reg (*(volatile uint32_t *)(ADC_BASE + 0))
#define adc_clkdiv_reg (*(volatile uint32_t *)(ADC_BASE + 4))
#define adc_data_reg (*(volatile uint32_t *)(ADC_BASE + 8))
#define adc_eoc_reg (*(volatile uint32_t *)(ADC_BASE + 12))

// --------------------------------------------------------
// blizzard_adc_test.c
// Blizzard ADC test
//
// Set GPIO 8 to ground
// Set GPIO 9 to 3.3V
// Input analog value on GPIO 16
// Outputs conversion value on GPIO 24-31
// Outputs end-of-conversion trigger on GPIO 32
// --------------------------------------------------------

void main()
{
    int i, j, k, v;

    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;

    reg_mprj_io_37 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_36 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_35 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_34 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_33 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_32 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_31 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_30 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_29 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_28 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_27 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_26 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_25 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_24 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_23 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_22 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_21 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_20 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_19 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_18 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_17 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;

    reg_mprj_io_16 = GPIO_MODE_MGMT_STD_ANALOG;
    reg_mprj_io_15 = GPIO_MODE_MGMT_STD_ANALOG;

    reg_mprj_io_14 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_13 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_12 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_11 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_10 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;

    // GPIO 9 is Vhigh---Set to output and drive high
    // reg_mprj_io_9  = GPIO_MODE_MGMT_STD_ANALOG;
    reg_mprj_io_9 = GPIO_MODE_MGMT_STD_OUTPUT;
    // GPIO 8 is Vlow---Set to output and drive low
    // reg_mprj_io_8  = GPIO_MODE_MGMT_STD_ANALOG;
    reg_mprj_io_8 = GPIO_MODE_MGMT_STD_OUTPUT;

    reg_mprj_io_7 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_5 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;

    /* Lowest 5 GPIOs need to be set this way in order to	*/
    /* access the housekeeping SPI at run-time.  Do not change	*/
    /* them unless absolutely necessary.			*/

    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_OUTPUT;

    /* GPIO 0 is turned off to prevent toggling the debug pin;	*/
    /* For debug, make this an output and drive it externally	*/
    /* to ground.						*/

    reg_mprj_io_0 = GPIO_MODE_MGMT_STD_ANALOG;

    // Initiate the serial transfer
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1)
        ;

    reg_uart_enable = 1;

    // print("Hello World !!");

    // Enable the wishbone bus on the user side
    reg_wb_enable = 1;

    // Bit 9 set high to drive Vhigh internally
    // Bit 8 set low to drive Vlow internally
    reg_mprj_datal = 0x00000200;

    // ADC test:  Jumper GPIO 15 and 16 together.  Use the ADC
    // to read back the value from the DAC and output on GPIO
    // 24 to 31.
    //
    // Send a pulse on GPIO 32 after each conversion and posting
    // of results that can be used as a trigger to a capture from
    // a Digilent Analog Discovery 2 module.

    // dac_ena_reg = 1;

    adc_ctrl_reg = ADC_CTRL_EN;

    // ADC frequency = core clock / (2 + 2 * divider value)
    // divider value 0 = /2 = 5MHz
    // divider value 1 = /4 = 2.5MHz
    // divider value 2 = /6 = 1.67MHz
    // and so forth.

    // adc_clkdiv_reg = 1;      /* core clock /  4 = 2.5MHz */
    // adc_clkdiv_reg = 2;      /* core clock /  6 = 1.67MHz */
    // adc_clkdiv_reg = 4;      /* core clock / 10 = 1MHz */
    // adc_clkdiv_reg = 5;      /* core clock / 12 = 813kHz */
    // adc_clkdiv_reg = 6; /* core clock / 14 = 714kHz */
    // adc_clkdiv_reg = 12;     /* core clock / 26 = 385kHz */

    int io22 = (reg_mprj_datal >> 22) & 1;
    count_down(PULSE_WIDTH * 10);
    config_uart();
    print("ST: adc_test\n");
    adc_clkdiv_reg = 6;
    while (io22 == 1)
    {
        io22 = (reg_mprj_datal >> 22) & 1;
    }
    while (io22 == 0)
    {
        delay(2500);
        adc_ctrl_reg = ADC_CTRL_EN | ADC_CTRL_SOC;
        while (adc_eoc_reg == 0)
            ;
        reg_mprj_datal = 0x200 | (adc_data_reg << 24);
        reg_mprj_datah = 0x0000001; // trigger
        delay(2500);
        reg_mprj_datah = 0x0000000;

        io22 = (reg_mprj_datal >> 22) & 1;
    }
    count_down(PULSE_WIDTH * 10);
}
