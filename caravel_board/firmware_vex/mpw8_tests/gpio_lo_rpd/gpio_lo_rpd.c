#include <common.h>


void set_registers(){
    for (int i = 0; i < 38; i++){
        if (i>=19){
            configure_gpio(i, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
        }else{
            configure_gpio(i, GPIO_MODE_MGMT_STD_OUTPUT);
        }
    }
}
/*
@ finish configuration 
    send packet with size 1

GPIO[19:37] is configured as input pull down and mapped to GPIO[0:18]

input value send to gpio[19:37] suppose to be received as output at GPIO[0:18]
*/
void main(){
    configure_mgmt_gpio();
    set_registers();
    set_gpio_h(0);
    set_gpio_l(0);
    gpio_config_load();
    send_packet(1); // configuration finished start test
    int mask = 0xFFF80000;
    int mask_h = 0x7E000;
    int i_val = 0;
    int o_val_l;
    int o_val_h;
    int o_val;
    while (true){
        i_val = get_gpio_l() & mask;
        o_val_h = get_gpio_h() >> 13;
        o_val_l = i_val << 19;
        o_val = o_val_l | o_val_h;
        set_gpio_l(o_val);
    }
}
