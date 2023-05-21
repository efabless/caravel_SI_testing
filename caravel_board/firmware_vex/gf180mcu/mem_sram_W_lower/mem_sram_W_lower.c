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

bool mem_sram_W_lower()
{
   //   #define dff_size  (*(volatile uint32_t*)0x0)
   volatile uint32_t* base_addr = ((volatile uint32_t*)  0x00000000 );
   int dff_size = 0x400 / 4;
//   #define iterator  (*(volatile uint32_t*)0x4)  // first address in the ram store the iterator
   int iterator = 0;
   for (iterator = 0; iterator < dff_size; iterator++ ){
      // reg_debug_2 = iterator;
      *(base_addr + iterator) = 0x55555555;
   }
   for (iterator = 0; iterator < dff_size; iterator++ ){
      // reg_debug_2 = iterator;
      if (*( base_addr + iterator) !=  0x55555555){
         return false;
      }
   }
   for (iterator = 0; iterator < dff_size; iterator++ ){
      // reg_debug_2 = iterator;
      *( base_addr + iterator) = 0xAAAAAAAA;
   }
   for (iterator = 0; iterator < dff_size; iterator++ ){
   // reg_debug_2 = iterator;
      if (*( base_addr + iterator) != 0xAAAAAAAA){
         return false;
      }
   }


   // test finish
   return true;
}
