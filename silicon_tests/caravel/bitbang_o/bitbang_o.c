#include <common.h>
#include <bitbang.h>
#define PULSE_WIDTH 250000

void main()
{
    configure_mgmt_gpio_input();
    if (reg_gpio_in == 0){
        int i, j;
        int num_pulses = 4;
        char *c;
        bb_configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
        configure_gpio(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
        set_gpio_h(0);
        set_gpio_l(0);
        gpio_config_load();
        config_uart();
        print("Start Test: bitbang_o\n");
        while (reg_gpio_in == 0)
        {
            c = uart_get_line();
            j = get_int_from_string(c);
            if (j >= 32)
            {
                for (i = 0; i < num_pulses; i++)
                {
                    set_gpio_h(0x1 << j - 32);
                    print("u\n");
                    count_down(PULSE_WIDTH);
                    set_gpio_h(0x0);
                    print("d\n");
                    count_down(PULSE_WIDTH);
                }
            }
            else
            {
                for (i = 0; i < num_pulses; i++)
                {
                    set_gpio_l(0x1 << j);
                    print("u\n");
                    count_down(PULSE_WIDTH);
                    set_gpio_l(0x0);
                    print("d\n");
                    count_down(PULSE_WIDTH);
                }
            }
        }
    }
    HKGpio_config();
}
