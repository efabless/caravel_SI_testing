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

bool mem_dff_test()
{
   unsigned char *dff_start_address = (unsigned char *)0x00000000;
   unsigned int dff_size = 1024;

   unsigned int loop_start = 0;
   // unsigned int loop_end =  255;

   // unsigned int loop_start =  256;
   // unsigned int loop_end =  512;

   // unsigned int loop_start =  513;
   // unsigned int loop_end =  768;

   // unsigned int loop_start =  769;
   unsigned int loop_end = dff_size;

   for (unsigned int i = loop_start; i < loop_end; i++)
   {

      unsigned char data = (i + 7) * 13;
      *(dff_start_address + i) = data;
   }
   for (unsigned int i = loop_start; i < loop_end; i++)
   {
      unsigned char data = (i + 7) * 13;
      if (data != *(dff_start_address + i))
      {
         return false;
      }
   }
   return true;
}
