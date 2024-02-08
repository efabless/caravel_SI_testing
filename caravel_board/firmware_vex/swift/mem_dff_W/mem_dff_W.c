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

bool mem_dff_W()
{
    enable_debug();
volatile short *dff_start_address = (volatile short *)DFF2_START_ADDR;
    volatile int dff_size = DFF2_SIZE / 4;
    volatile short data = 0x5555;
    for (volatile int i = 0; i < dff_size; i++)
    {
        *(dff_start_address + i) = data;
    }
    for (volatile int i = 0; i < dff_size; i++)
    {
        if (data != *(dff_start_address + i))
        {
            // set_debug_reg2(dff_start_address + i);
            // set_debug_reg1(0x1E);
            return false;
        }
    }

    data = 0xAAAA;
    for (volatile int i = 0; i < dff_size; i++)
    {
        *(dff_start_address + i) = data;
    }
    for (volatile int i = 0; i < dff_size; i++)
    {
        if (data != *(dff_start_address + i))
        {
            // set_debug_reg2(dff_start_address + i);
            // set_debug_reg1(0x1E);
            return false;
        }
    }
    return true;
}
