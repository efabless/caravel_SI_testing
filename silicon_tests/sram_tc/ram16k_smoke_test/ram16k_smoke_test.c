// SPDX-FileCopyrightText: 2023 Efabless Corporation

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//      http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


#include <common.h>

#define USER_ADDR_SPACE_C_HEADER_FILE  // TODO disable using the other file until tag is updated and https://github.com/efabless/caravel_mgmt_soc_litex/pull/137 is merged

#define MEM_SIZE 1*1024     // Note: The only functional part of the 4K word memory (16KB) is first quarter (due to a bug in the wrapper) word addresses: 0 to 1023
#define ADDR_MASK 0x3FF

#define ADDR_STEP_1 395
#define ADDR_STEP_2 73
#define ADDR_STEP_3 521

#define SEED_1 0x11434fab
#define SEED_2 0xab23cf67
#define SEED_3 0x9f4578eb
#define SEED_4 0x729fda64




unsigned int seed; // random seed (global variable to be able to regenerate the values)


void main(){
    // Enable managment gpio as output to use as indicator for finishing configuration  
    enable_user_interface(1);
    mgmt_gpio_o_enable();
    send_packet(2);

    if (!test_mem_word()){  // writes words to all locations in the memory (non-consecutive addresses and random data)
        return;
    }

    if (!test_mem_word_inv()){  // invert the random data written to make sure that there is no stuck at 0 or stuck at 1
        return;
    }

    if (!test_mem_halfword()){  // writes half words to all locations in the memory (non-consecutive addresses and random data)
        return;
    }

    if (!test_mem_byte()){  // writes bytes to all locations in the memory (non-consecutive addresses and random data)
        return;
    }

    if (!test_mem_consec()){  // writes words to random address and read it right after writing 
        return;
    }
    

    send_packet(16);

}

int test_mem_word(){

    seed = SEED_1;
    unsigned int x =0;
    int addr, data;

    // writing 
    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_1;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        data = rand_num_gen(&seed);
        USER_writeWord(data, addr);
    }

    seed = SEED_1; // re-write seed to be same value to generate the same values 
    x = 0;
    // reading 
    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_1;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        if (USER_readWord(addr) != rand_num_gen(&seed)){
            send_packet(4);
            mgmt_gpio_wr(0); // finish test (failure)
            return 0;
        }
    }
}

int test_mem_word_inv(){

    seed = SEED_1;
    unsigned int x =0;
    int addr, data;

    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_1;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        data = ~rand_num_gen(&seed);
        // USER_writeWord(data, (i|0x4000));
        USER_writeWord(data, addr);
    }

    seed = SEED_1; // re-write seed to be same value to generate the same values 

    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_1;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        // if (USER_readWord((i|0x4000)) != rand_num_gen(&seed, 32)){
        if (USER_readWord(addr) != ~rand_num_gen(&seed)){
            send_packet(4);
            mgmt_gpio_wr(0); // finish test (failure)
            return 0;
        }
    }
}

int test_mem_halfword(){

    seed = SEED_2;
    unsigned int x =0;
    int addr;
    short data;
    char first_or_second_half;

    // writing to first half 
    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_2;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        data = rand_num_gen(&seed)&0xFF;
        first_or_second_half = rand_num_gen(&seed)&1;
        USER_writeHalfWord(data, addr, first_or_second_half);
    }

    seed = SEED_2; // re-write seed to be same value to generate the same values 
    // read first half 
    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_2;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        data = rand_num_gen(&seed)&0xFF;
        first_or_second_half = rand_num_gen(&seed)&1;
        if (USER_readHalfWord(addr, first_or_second_half) != data){
            send_packet(6);
            mgmt_gpio_wr(0); // finish test (failure)
            return 0;
        }
    }

}

int test_mem_byte(){

    seed = SEED_3;
    unsigned int x =0;
    int addr;
    short data;
    char byte_num;

    // writing to first half 
    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_3;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        data = rand_num_gen(&seed)&0xFF;
        byte_num = rand_num_gen(&seed)&0b11;
        USER_writeByte(data, addr, byte_num);
    }

    seed = SEED_3; // re-write seed to be same value to generate the same values 
    // read first half 
    for (int i=0; i<MEM_SIZE; i++){
        x = x + ADDR_STEP_3;
        addr = x & ADDR_MASK;
        addr = addr | 0x4000;
        data = rand_num_gen(&seed)&0xFF;
        byte_num = rand_num_gen(&seed)&0b11;
        if (USER_readByte(addr, byte_num) != data){
            send_packet(8);
            mgmt_gpio_wr(0); // finish test (failure)
            return 0;
        }
    }

}
// change to consec addresses 
int test_mem_consec(){

    seed = SEED_4;
    int addr, data;

    // writing 
    for (int i=0; i<MEM_SIZE; i++){
        addr = i | 0x4000;
        data = rand_num_gen(&seed);
        USER_writeWord(data, addr);
        if (USER_readWord(addr) != data){
            send_packet(10);
            mgmt_gpio_wr(0); // finish test (failure)
            return 0;
        }
    }
}
