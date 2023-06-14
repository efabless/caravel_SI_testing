#include <common.h>
#define PULSE_WIDTH 250000

void main()
{
    int i, j;
    int num_pulses = 4;
    int num_bits = 19;
    char *c;
    GPIOs_configureAll(GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_writeHigh(0);
    GPIOs_writeLow(0);
    GPIOs_loadConfigs();
    // config_uart();
    UART_enableTX(1);
    print("Start Test: gpio_o\n");

    for (j = 0; j < 37; j++)
    {
        if (j != 5 && j != 6)
        {
            c = j - '0';
            print("g/");
            print(c);
            print("\n");
            if (j >= 32)
            {
                for (i = 0; i < num_pulses; i++)
                {
                    GPIOs_writeHigh(0x1 << j - 32);
                    count_down(PULSE_WIDTH);
                    GPIOs_writeHigh(0x0);
                    count_down(PULSE_WIDTH);
                }
            }
            else
            {
                for (i = 0; i < num_pulses; i++)
                {
                    GPIOs_writeLow(0x1 << j);
                    count_down(PULSE_WIDTH);
                    GPIOs_writeLow(0x0);
                    count_down(PULSE_WIDTH);
                }
            }
        }
    }
    print("End Test\n");
}
