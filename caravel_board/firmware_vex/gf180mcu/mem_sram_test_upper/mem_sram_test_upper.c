#include <common.h>

/*
   @ start of test
      send packet with size = 1
   @ error reading
      send packet with size = 9
   @ test finish
      send packet with size = 3
      send packet with size = 3
      send packet with size = 3

*/

void main()
{

   configure_mgmt_gpio();
   send_packet(1); // start of the test
                   //   #define dff_size  (*(volatile uint32_t*)0x0)
   volatile uint32_t *base_addr = ((volatile uint32_t *)0x00000400);
   int dff_size = 0x400;
   //   #define iterator  (*(volatile uint32_t*)0x4)  // first address in the ram store the iterator
   int iterator = 0;
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      *((unsigned char *)0x00000000 + iterator) = 0x55;
   }
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      if (*((unsigned char *)0x00000000 + iterator) != 0x55)
      {
         send_packet(9); // error
         return;
      }
   }

   for (iterator = 8; iterator < dff_size; iterator++)
   {
      *((unsigned char *)0x00000000 + iterator) = 0xAA;
   }
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      if (*((unsigned char *)0x00000000 + iterator) != 0xAA)
      {
         send_packet(9); // error
         return;
      }
   }

   // test finish
   count_down(PULSE_WIDTH * 10);
   send_packet(3);
   count_down(PULSE_WIDTH * 10);
   send_packet(4);
   count_down(PULSE_WIDTH * 10);
   send_packet(5);
}