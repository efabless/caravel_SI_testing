#include <common.h>
#define PULSE_WIDTH 250000

void main()
{
    int i, j;
    int num_pulses = 4;
    int num_bits = 19;
    char *c;
    configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    set_gpio_h(0);
    set_gpio_l(0);
    gpio_config_load();
    // config_uart();
    enable_uart_TX(1);
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
                    set_gpio_h(0x1 << j - 32);
                    count_down(PULSE_WIDTH);
                    set_gpio_h(0x0);
                    count_down(PULSE_WIDTH);
                }
            }
            else
            {
                for (i = 0; i < num_pulses; i++)
                {
                    set_gpio_l(0x1 << j);
                    count_down(PULSE_WIDTH);
                    set_gpio_l(0x0);
                    count_down(PULSE_WIDTH);
                }
            }
        }
    }
    print("End Test\n");
}
