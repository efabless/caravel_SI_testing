#include <common.h>

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

bool mem_dff_halfW()
{
   unsigned short *dff_start_address = (unsigned short *)0x00000000;
   unsigned int dff_size = 512;

   unsigned int loop_start = 0;
   unsigned int loop_end = dff_size;

   for (unsigned int i = loop_start; i < loop_end; i++)
   {

      unsigned short data = (i + 7) * 13;
      *(dff_start_address + i) = data;
   }
   for (unsigned int i = loop_start; i < loop_end; i++)
   {
      unsigned short data = (i + 7) * 13;
      if (data != *(dff_start_address + i))
      {
         return false;
      }
   }
   return true;
}
