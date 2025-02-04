#include <common.h>
#define PULSE_WIDTH 250000

void single_block_decipher(int* key, int* text, int* expected , bool is_128key);
void main() {

    mgmt_gpio_o_enable();

    send_packet(2); // test begins 
    User_enableIF();
    
    int key[] = {0x2b7e1516,0x28aed2a6,0xabf71588,0x09cf4f3c,0x0,0x0,0x0,0x0};
    int text[] = {0xf5d3d585,0x03b9699d,0xe785895a,0x96fdbaaf};
    int expected[] = {0xae2d8a57, 0x1e03ac9c, 0x9eb76fac, 0x45af8e51};
    single_block_decipher(key,text,expected,true);
    send_packet(4); // done first decipher

    int key2[] = {0x00010203,0x04050607,0x08090a0b,0x0c0d0e0f,0x10111213,0x14151617,0x18191a1b,0x1c1d1e1f};
    int text2[] = {0x8ea2b7ca, 0x516745bf, 0xeafc4990, 0x4b496089};
    int expected2[] = {0x00112233, 0x44556677, 0x8899aabb, 0xccddeeff};
    single_block_decipher(key2,text2,expected2,false);
    send_packet(6); // done second decipher

}

void single_block_decipher(int* key, int* text, int* expected , bool is_128key) {
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
        USER_writeWord(0x0,0x0a);// configuration
    }else{
        USER_writeWord(0x2,0x0a);// configuration
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