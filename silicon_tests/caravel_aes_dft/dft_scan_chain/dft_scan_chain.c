#include <common.h>
#define PULSE_WIDTH 250000

void main()
{ 
    configure_gpio(27,GPIO_MODE_USER_STD_OUTPUT);
    gpio_config_load();
    while(1);

}