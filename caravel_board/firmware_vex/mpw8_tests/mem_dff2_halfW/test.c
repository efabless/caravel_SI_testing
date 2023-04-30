#include <stdio.h>

void main()
{

   unsigned char *openram_start_address =  (unsigned char *) 0x01000000;
   unsigned int openram_size =  2*1024;


   for (size_t i = 0; i < openram_size; i++){

    unsigned char data = (i + 7)*13;
    *(openram_start_address+i) = data; 

   }
   for (size_t i = 0; i < openram_size; i++){
       
    unsigned char data = (i + 7)*13;
    if (data != *(openram_start_address+i){
        // error
        return;
    }
   }




}
