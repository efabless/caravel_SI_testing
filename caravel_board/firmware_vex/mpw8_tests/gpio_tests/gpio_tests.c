#include <common.h>
#include "gpio_tests.h"

void main()
{
    gpio_o();
    gpio_i();
    bitbang_o();
    bitbang_i();
    config_uart();
    print("End Test\n");
}