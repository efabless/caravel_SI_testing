#include "drv.c"
#include "stdlib.c"

#define TEST_START      0xA3
#define TEST_END        0x97
#define TEST_SYNC       0xE7
#define TEST_PASSED     (TEST_END + 0x10)
#define TEST_FAILED     (TEST_END + 0x20)

void test_start(unsigned char id){
    unsigned int data = 0;
    unsigned int state = (TEST_START << 8);
    data = state | id;
    dbg_write(data);
}

void test_sync(unsigned char id){
    unsigned int data = 0;
    unsigned int state = (TEST_SYNC << 8);
    data = state | id;
    dbg_write(data);
}

void test_end(unsigned char id){
    unsigned int data = 0;
    unsigned int state = (TEST_END << 8);
    data = state | id;
    dbg_write(data);
}

void test_fail(unsigned char id){
    unsigned int data = 0;
    unsigned int state = (TEST_FAILED << 8);
    data = state | id;
    dbg_write(data);
}

void test_pass(unsigned char id){
    unsigned int data = 0;
    unsigned int state = (TEST_PASSED << 8);
    data = state | id;
    dbg_write(data);
}

// Start test time measurement
void ett_start(){
    /*
    *GPIOA_OE = 0xFF;
    *GPIOB_OE = 0xFF;
    *GPIOA_DATA = 0x85;
    *GPIOB_DATA = 0x11;
    */
}

void dummy_delay(unsigned int x){
    unsigned int volatile i;
    for(i=0; i<x; i++);
}
