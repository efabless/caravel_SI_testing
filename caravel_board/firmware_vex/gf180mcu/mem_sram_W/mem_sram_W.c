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

void main(){

   configure_mgmt_gpio();
   send_packet(1); // start of the test
   #define dff_size  (*(volatile uint32_t*)0x0)  
   dff_size = 0x200;
   #define iterator  (*(volatile uint32_t*)0x4)  // first address in the ram store the iterator 
   iterator = 0;
   for (iterator = 8; iterator < dff_size; iterator++ ){
      // reg_debug_2 = iterator;
      *((unsigned int *) 0x00000000 + iterator) = 0x55555555; 
   }
   for (iterator = 8; iterator < dff_size; iterator++ ){
      // reg_debug_2 = iterator;
      if (*((unsigned int *) 0x00000000 + iterator) !=  0x55555555){
         send_packet(9); // error
         return;
      }
   }
   for (iterator = 8; iterator < dff_size; iterator++ ){
      // reg_debug_2 = iterator;
      *((unsigned int *) 0x00000000 + iterator) = 0xAAAAAAAA; 
   }
   for (iterator = 8; iterator < dff_size; iterator++ ){
   // reg_debug_2 = iterator;
      if (*((unsigned int *) 0x00000000 + iterator) != 0xAAAAAAAA){
         send_packet(9); // error
         return;
      }
   }


   // test finish
   send_packet(3);
   send_packet(3);
   send_packet(3);
}
