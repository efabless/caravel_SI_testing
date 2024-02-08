#include <firmware_apis.h>

/*
   @ start of test
      send packet with size = 1
   @ error reading
      send packet with size = 9
   @ pass 1 bytes
      send packet with size = 5
   @ test finish
      send packet with size = 3
      send packet with size = 3
      send packet with size = 3

*/

bool mem_sram_W()
{
    enable_debug();
volatile short *sram_start_address = (volatile short *)DFF1_START_ADDR;
    volatile int sram_size = DFF1_SIZE / 4;
    volatile short data = 0x5555;
    for (volatile int i = 0; i < sram_size; i++)
    {
        *(sram_start_address + i) = data;
    }
    for (volatile int i = 0; i < sram_size; i++)
    {
        if (data != *(sram_start_address + i))
        {
            // set_debug_reg2(sram_start_address + i);
            // set_debug_reg1(0x1E);
            return false;
        }
    }

    data = 0xAAAA;
    for (volatile int i = 0; i < sram_size; i++)
    {
        *(sram_start_address + i) = data;
    }
    for (volatile int i = 0; i < sram_size; i++)
    {
        if (data != *(sram_start_address + i))
        {
            // set_debug_reg2(sram_start_address + i);
            // set_debug_reg1(0x1E);
            return false;
        }
    }
    return true;
}
