#include <common.h>
#define PULSE_WIDTH 250000

void single_block_encipher(int* key, int* text, int* expected , bool is_128key);
void main() {
    mgmt_gpio_o_enable();
    send_packet(2); // test begins
    User_enableIF();
    
    int key[] = {0x2b7e1516,0x28aed2a6,0xabf71588,0x09cf4f3c,0x0,0x0,0x0,0x0};
    int text[] = {0x6bc1bee2,0x2e409f96,0xe93d7e11,0x7393172a};
    int expected[] = {0x3ad77bb4,0x0d7a3660,0xa89ecaf3,0x2466ef97};
    single_block_encipher(key,text,expected,true);
    send_packet(4); // done first encipher

    int key2[] = {0x603deb10,0x15ca71be,0x2b73aef0,0x857d7781,0x1f352c07,0x3b6108d7,0x2d9810a3,0x0914dff4};
    int text2[] = {0xf69f2445,0xdf4f9b17,0xad2b417b,0xe66c3710};
    int expected2[] = {0x23304b7a,0x39f9f3ff,0x067d8d8f,0x9e24ecc7};
    single_block_encipher(key2,text2,expected2,false);
    send_packet(6); // done second encipher

}

void single_block_encipher(int* key, int* text, int* expected , bool is_128key) {
    // keys 
    for (int i = 0; i < 8; i++) {
        USER_writeWord(key[i],0x10 + i);
    }
    if (is_128key) {
        USER_writeWord(0x0,0x0a);// configuration 
        
    }else{
        USER_writeWord(0x2,0x0a);// configuration 
    }
    USER_writeWord(0x1,0x08); // control
    // plain text 
    for (int i = 0; i < 4; i++) {
        USER_writeWord(text[i],0x20 + i);
    }
    if (is_128key) {
        USER_writeWord(0x1,0x0a);// configuration
    }else{
        USER_writeWord(0x3,0x0a);// configuration
    }
    USER_writeWord(0x2,0x08);// control

    // reading 
    int rec;

    for (int i = 0; i < 4; i++) {
        wait_valid();
        rec = USER_readWord(0x30 + i);
        if (rec != expected[i]) {
            send_packet(10); // failed 
            break;
        }
    }   
}

void wait_valid(){
    // wait until ready == 1
    while(USER_readWord(0x9) & 0b10 == 0);
}