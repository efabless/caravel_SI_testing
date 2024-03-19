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

bool mem_dff2_test()
{
   configure_mgmt_gpio();
   send_packet(1); // start of the test

   unsigned char *openram_start_address = (unsigned char *)0x00000400;
   unsigned int openram_size = 512;

   for (unsigned int i = 0; i < openram_size; i++)
   {

      unsigned char data = (i + 7) * 13;
      *(openram_start_address + i) = data;
   }
   for (unsigned int i = 0; i < openram_size; i++)
   {
      unsigned char data = (i + 7) * 13;
      if (data != *(openram_start_address + i))
      {
         return false;
      }
   }
   return true;
}
