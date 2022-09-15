#include <defs.h>
#include "send_packet.c"

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

   unsigned char *openram_start_address =  (unsigned char *) 0x01000000;
   unsigned int openram_size =  2*1024;


   for (int i = 0; i < openram_size; i++){

    unsigned char data = (i + 7)*13;
    *(openram_start_address++) = data; 

   }
   *openram_start_address =  (unsigned char *) 0x01000000;
   for (int i = 0; i < openram_size; i++){
    unsigned char data = (i + 7)*13;
    if (data != *(openram_start_address++)){
        send_packet(9);
    }
   }


   // test finish 
   send_packet(3);
   send_packet(3);
   send_packet(3);
}
