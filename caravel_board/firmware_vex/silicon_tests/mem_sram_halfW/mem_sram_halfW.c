#include <defs.h>
#include "send_packet.c"

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

   unsigned short *openram_start_address =  (unsigned short *) 0x01000000;
   unsigned int openram_size =  1024;


   for (unsigned int i = 0; i < openram_size; i++){

    unsigned short data = (i + 7)*13;
    *(openram_start_address+i) = data; 

   }
   for (unsigned int i = 0; i < openram_size; i++){
    unsigned short data = (i + 7)*13;
    if (data != *(openram_start_address+i)){
        send_packet(9); //error
    }
    send_packet(5); // pass 1 byte
   }


   // test finish 
   send_packet(3);
   send_packet(3);
   send_packet(3);
}
