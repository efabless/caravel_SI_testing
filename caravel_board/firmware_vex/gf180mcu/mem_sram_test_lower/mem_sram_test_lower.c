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

bool mem_sram_test_lower()
{
   //   #define dff_size  (*(volatile uint32_t*)0x0)
   volatile uint8_t *base_addr = ((volatile uint8_t *) 0x00000000);
   int dff_size = 0x400;
   //   #define iterator  (*(volatile uint32_t*)0x4)  // first address in the ram store the iterator
   int iterator = 0;
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      *(base_addr + iterator) = 0x55;
   }
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      if (*(base_addr + iterator) != 0x55)
      {
         return false;
      }
   }

   for (iterator = 8; iterator < dff_size; iterator++)
   {
      *(base_addr + iterator) = 0xAA;
   }
   for (iterator = 8; iterator < dff_size; iterator++)
   {
      if (*(base_addr + iterator) != 0xAA)
      {
         return false;
      }
   }

   // test finish
   return true;
}