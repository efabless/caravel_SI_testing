#include <defs.h>
#include <stub.c>
#include "../common/send_packet.c"

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

void main()
{
   configure_mgmt_gpio();
   send_packet(1); // start of the test

   unsigned int *dff_start_address = (unsigned int *)0x00000000;
   unsigned int dff_size = 256;

   for (unsigned int i = 0; i < dff_size; i++)
   {

      unsigned int data = (i + 7) * 13;
      *(dff_start_address + i) = data;
   }
   for (unsigned int i = 0; i < dff_size; i++)
   {
      unsigned int data = (i + 7) * 13;
      if (data != *(dff_start_address + i))
      {
         send_packet(9); // error
      }
   }

   // test finish
   send_packet(3);
   send_packet(3);
   send_packet(3);
}
