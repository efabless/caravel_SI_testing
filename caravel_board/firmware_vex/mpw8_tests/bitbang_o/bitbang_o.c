#include <common.h>
#include <bitbang.h>
#define PULSE_WIDTH 250000

void main()
{
    int i, j;
    int num_pulses = 4;
    char *c;
    bb_configureAllGpios(GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_writeHigh(0);
    GPIOs_writeLow(0);
    GPIOs_loadConfigs();
    config_uart();
    print("Start Test: bitbang_o\n");
    while (true)
    {
        c = UART_readLine();
        j = get_int_from_string(c);
        if (j >= 32)
        {
            for (i = 0; i < num_pulses; i++)
            {
                GPIOs_writeHigh(0x1 << j - 32);
                print("u\n");
                count_down(PULSE_WIDTH);
                GPIOs_writeHigh(0x0);
                print("d\n");
                count_down(PULSE_WIDTH);
            }
        }
        else
        {
            for (i = 0; i < num_pulses; i++)
            {
                GPIOs_writeLow(0x1 << j);
                print("u\n");
                count_down(PULSE_WIDTH);
                GPIOs_writeLow(0x0);
                print("d\n");
                count_down(PULSE_WIDTH);
            }
        }
    }
}
