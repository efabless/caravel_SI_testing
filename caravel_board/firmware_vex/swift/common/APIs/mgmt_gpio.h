/**
 \file
*/
#ifndef MGMT_GPIO_C_HEADER_FILE
#define MGMT_GPIO_C_HEADER_FILE
#define PULSE_WIDTH 2500000
#include <timer0.h>

/**
 * Performs a countdown using timer0.
 *
 * @param d The duration of the countdown in timer ticks.
 * @return None.
 */
void count_down(const int d)
{
    /* Configure timer for a single-shot countdown */
    timer0_configureOneShot(d);

    // Loop, waiting for value to reach zero
    timer0_updateValue(); // latch current value
    int old_val = timer0_readValue();
    while (old_val > 0)
    {
        timer0_updateValue();
        old_val = timer0_readValue();
    }
}

void send_pulse()
{
    ManagmentGpio_write(0);
    count_down(PULSE_WIDTH);
    ManagmentGpio_write(1);
    count_down(PULSE_WIDTH);
}

/**
 * Sends a packet by emitting a series of pulses, where the number of pulses is
 * determined by the num_pulses parameter. After sending the pulses, the
 * function waits for a duration of PULSE_WIDTH*10 before ending the packet.
 *
 * @param num_pulses The number of pulses to send in the packet.
 */
void send_packet(int num_pulses)
{
    // send pulses
    for (int i = 0; i < num_pulses + 1; i++)
    {
        send_pulse();
    }
    // end of packet
    count_down(PULSE_WIDTH * 10);
}

// management GPIO
/**
 * Configure management GPIO as input
 *
 */
void ManagmentGpio_inputEnable()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
#ifndef REG_GPIO_INVERTED
    reg_gpio_ien = 1;
    reg_gpio_oe = 0;
#else
    reg_gpio_ien = 0; // because in gf the GPIO  enable regs are inverted
    reg_gpio_oe = 1;
#endif
    dummyDelay(1);
}
/**
 * Configure management GPIO as output
 *
 */
void ManagmentGpio_outputEnable()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
#ifndef REG_GPIO_INVERTED
    reg_gpio_ien = 0;
    reg_gpio_oe = 1;
#else
    reg_gpio_ien = 1; // because in gf the GPIO  enable regs are inverted
    reg_gpio_oe = 0;
#endif
    dummyDelay(1);
}
/**
 * Configure management GPIO as bi-direction
 *
 */
void ManagmentGpio_ioEnable()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
#ifndef REG_GPIO_INVERTED
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
#else
    reg_gpio_ien = 0; // because in gf the GPIO  enable regs are inverted
    reg_gpio_oe = 0;
#endif
}
/**
 * Configure management GPIO as floating
 * It's not connected as input or output
 *
 */
void ManagmentGpio_disable()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
#ifndef REG_GPIO_INVERTED
    reg_gpio_ien = 0;
    reg_gpio_oe = 0;
#else
    reg_gpio_ien = 1; // because in gf the GPIO  enable regs are inverted
    reg_gpio_oe = 1;
#endif
}
/**
 * Write data in management GPIO
 *
 * @param data data to write at management GPIO possible values are 0 and 1
 *
 * \note
 * This function works when management GPIO  configured as output
 *
 */
void ManagmentGpio_write(int data) { reg_gpio_out = data; }
/**
 * Read data in management GPIO
 *
 * \note
 * This function works correctly when management GPIO  configured as input
 * If management doesn't connect to anything the firmware would read "0"
 *
 */
int ManagmentGpio_read() { return reg_gpio_in; }
/**
 * Wait over management GPIO to equal data
 *
 * \note
 * This function works correctly when management GPIO  configured as input
 *
 * @param data data to wait over
 *
 */
void ManagmentGpio_wait(int data)
{
    while (reg_gpio_in == data)
        ;
}

void HKGpio_config()
{

    ManagmentGpio_inputEnable();
    ManagmentGpio_wait(0);

    GPIOs_configure(0, GPIO_MODE_MGMT_STD_BIDIRECTIONAL);
    GPIOs_configure(1, GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(2, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(3, GPIO_MODE_MGMT_STD_INPUT_PULLUP);
    GPIOs_configure(4, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(6, GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(7, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(32, GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(33, GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(34, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_configure(35, GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_loadConfigs();
}

#endif // MGMT_GPIO_C_HEADER_FILE
