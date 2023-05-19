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
   volatile uint16_t *base_addr = ((volatile uint16_t *)0x00000000);
   int dff_size = 0x400 / 2;
   //   #define iterator  (*(volatile uint32_t*)0x4)  // first address in the ram store the iterator
   int iterator = 0;
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      // reg_debug_2 = iterator;
      *(base_addr + iterator) = 0x5555;
   }
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      // reg_debug_2 = iterator;
      if (*(base_addr + iterator) != 0x5555)
      {
         send_packet(9); // error
         return;
      }
   }

   for (iterator = 8; iterator < dff_size; iterator++)
   {
      // reg_debug_2 = iterator;
      *(base_addr + iterator) = 0xAAAA;
   }
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      // reg_debug_2 = iterator;
      if (*((unsigned short *)0x00000000 + iterator) != 0xAAAA)
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