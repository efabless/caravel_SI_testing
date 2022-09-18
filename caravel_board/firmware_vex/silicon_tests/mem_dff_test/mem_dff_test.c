#include <defs.h>
#include "send_packet.c"

/*
   @ start of test 
      send packet with size = 1
   @ error reading 
      send packet with size = 9
   @ pass 64 bytes 
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

   unsigned char *dff_start_address =  (unsigned char *) 0x00000000;
   unsigned int dff_size =  1024;


   for (int i = 0; i < dff_size; i++){

    unsigned char data = (i + 7)*13;
    *(dff_start_address++) = data; 

   }
   *dff_start_address =  (unsigned char *) 0x00000000;
   for (int i = 0; i < dff_size; i++){
    unsigned char data = (i + 7)*13;
    if (data != *(dff_start_address++)){
        send_packet(9);
    }
    if (i%64 == 0){
       send_packet(5);
    }
   }

   // test finish 
   send_packet(3);
   send_packet(3);
   send_packet(3);
}

