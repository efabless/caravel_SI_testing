#include <common.h>
#define PULSE_WIDTH 250000

void main()
{ 
    configure_gpio(27,GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(28,GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(29,GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(30,GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    configure_gpio(31,GPIO_MODE_MGMT_STD_INPUT_NOPULL);


    gpio_config_load();
    while(1);

}