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

bool mem_sram_halfW_lower()
{
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
         return false;
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
         return false;
      }
   }

   // test finish
   return true;
}