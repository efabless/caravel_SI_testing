#include <defs.h>
#include "send_packet.c"

/*
   @ start of test 
      send packet with size = 1
   @ pass bytes  
      send packet with size = 2
   @ pass int  
      send packet with size = 3
   @ pass short  
      send packet with size = 4
   @ error reading 
      send packet with size = 9
   @ test finish 
      send packet with size = 7
      send packet with size = 7
      send packet with size = 7
   
*/
#define BYTE_SIZE 600
#define SHORT_SIZE BYTE_SIZE/2
#define INT_SIZE BYTE_SIZE/4
void main()
{
   
   configure_mgmt_gpio();
   send_packet(1); // start of the test

   // to take 700 bytes of dff

   // unsigned int dff_ints[750]; // 240byte
   // unsigned short dff_shorts[115]; // 230byte 
   unsigned char dff_bytes[BYTE_SIZE]; // 800byte
   unsigned short *dff_shorts=(unsigned short *) dff_bytes;
   unsigned int *dff_ints=(unsigned int *) dff_bytes;
   unsigned char magic = 0x79;
   unsigned int magic_int = 0x79797979;
   unsigned short magic_short = 0x7979;
   unsigned char magic1;
   unsigned int magic1_int;
   unsigned short magic1_short;
   int i;
   magic1 = magic;
   for ( i=0; i<BYTE_SIZE; i++){
      dff_bytes[i] = (magic1*3+5)|magic;
      magic1 += 11;
   }
   magic1 = magic;

   for ( i=0; i<BYTE_SIZE; i++){
       unsigned char t = (magic1*3+5)|magic;
      if (t != dff_bytes[i]){
         send_packet(9); //error
         return;
      }
      magic1 += 11;
   }  
   send_packet(2); // byte pass
   // int
   magic1_int = magic_int;
   for ( i=0; i<INT_SIZE; i++){
      dff_ints[i] = (magic1_int*3+5)|magic_int;
      magic1_int += 11;
   }
   magic1_int = magic_int;

   for ( i=0; i<INT_SIZE; i++){
       unsigned int t = (magic1_int*3+5)|magic_int;
      if (t != dff_ints[i]){
         send_packet(9); //error
         return;
      }
      magic1_int += 11;
   }   
   send_packet(3); // int pass

   // short
   magic1_short = magic_short;
   for ( i=0; i<SHORT_SIZE; i++){
      dff_shorts[i] = (magic1_short*3+5)|magic_short;
      magic1_short += 11;
   }
   magic1_short = magic_short;

   for ( i=0; i<SHORT_SIZE; i++){
      unsigned short t = (magic1_short*3+5)|magic_short;
      if (t != dff_shorts[i]){
         send_packet(9); //error
         return;
      }
      magic1_short += 11;
   }
   send_packet(4); // short pass

   // test finish 
   send_packet(7);
   send_packet(7);
   send_packet(7);
}


// // random dff locations dff ram from 0x00000000 to 0x00000400
// #define dff_loc0 (*(volatile uint32_t*) 0x00000000)
// #define dff_loc1 (*(volatile uint32_t*) 0x00000008)
// #define dff_loc2 (*(volatile uint32_t*) 0x0000002C)
// #define dff_loc3 (*(volatile uint32_t*) 0x00000050)
// #define dff_loc4 (*(volatile uint32_t*) 0x00000084)
// #define dff_loc5 (*(volatile uint32_t*) 0x00000100)
// #define dff_loc6 (*(volatile uint32_t*) 0x0000013c)
// #define dff_loc7 (*(volatile uint32_t*) 0x0000020c)
// #define dff_loc8 (*(volatile uint32_t*) 0x00000270)
// #define dff_loc9 (*(volatile uint32_t*) 0x00000368)
// #define dff_loc10 (*(volatile uint32_t*) 0x00000400)

// // random sram locations sram ram from 0x01000000 to 0x01000800
// #define sram_loc0 (*(volatile uint32_t*) 0x01000000)
// #define sram_loc1 (*(volatile uint32_t*) 0x01000008)
// #define sram_loc2 (*(volatile uint32_t*) 0x0100012C)
// #define sram_loc3 (*(volatile uint32_t*) 0x01000250)
// #define sram_loc4 (*(volatile uint32_t*) 0x01000384)
// #define sram_loc5 (*(volatile uint32_t*) 0x01000400)
// #define sram_loc6 (*(volatile uint32_t*) 0x0100053c)
// #define sram_loc7 (*(volatile uint32_t*) 0x0100060c)
// #define sram_loc8 (*(volatile uint32_t*) 0x01000770)
// #define sram_loc9 (*(volatile uint32_t*) 0x01000768)
// #define sram_loc10 (*(volatile uint32_t*) 0x01000800)


   // // writing 1's to the dff random mem
   // dff_loc0  = 0xFFFFFFFF; dff_loc1  = 0xFFFFFFFF; dff_loc2  = 0xFFFFFFFF; dff_loc3  = 0xFFFFFFFF;
   // dff_loc4  = 0xFFFFFFFF; dff_loc5  = 0xFFFFFFFF; dff_loc6  = 0xFFFFFFFF; dff_loc7  = 0xFFFFFFFF;
   // dff_loc8  = 0xFFFFFFFF; dff_loc9  = 0xFFFFFFFF;  dff_loc10 = 0xFFFFFFFF;

   // // read dff 
   // cond1 = dff_loc0 == 0xFFFFFFFF && dff_loc1 == 0xFFFFFFFF && dff_loc2 == 0xFFFFFFFF && dff_loc3 == 0xFFFFFFFF ;
   // cond2 = dff_loc4 == 0xFFFFFFFF && dff_loc5 == 0xFFFFFFFF && dff_loc6 == 0xFFFFFFFF && dff_loc7 == 0xFFFFFFFF ;
   // cond3 = dff_loc8 == 0xFFFFFFFF && dff_loc9 == 0xFFFFFFFF && dff_loc10 == 0xFFFFFFFF ;
   // if ( cond1 & cond2 & cond3)
   //    send_packet(2); // read 1's from dff mem
   // else 
   //    send_packet(9); // error in reading

   // // writing 0's to the dff random mem
   // dff_loc0 = 0x0; dff_loc1 = 0x0; dff_loc2 = 0x0; dff_loc3 = 0x0; dff_loc4 = 0x0; dff_loc5 = 0x0;
   // dff_loc6 = 0x0; dff_loc7 = 0x0; dff_loc8 = 0x0; dff_loc9 = 0x0; dff_loc10 = 0x0;

   // // read dff 
   // cond1 = dff_loc0 == 0x0 && dff_loc1 == 0x0 && dff_loc2 == 0x0 && dff_loc3 == 0x0 ;
   // cond2 = dff_loc4 == 0x0 && dff_loc5 == 0x0 && dff_loc6 == 0x0 && dff_loc7 == 0x0 ;
   // cond3 = dff_loc8 == 0x0 && dff_loc9 == 0x0 && dff_loc10 == 0x0 ;
   // if ( cond1 & cond2 & cond3)
   //    send_packet(3); // read 0's from dff mem
   // else 
   //    send_packet(9); // error in reading


   // // writing 1's to the sram random mem
   // sram_loc0  = 0xFFFFFFFF; sram_loc1  = 0xFFFFFFFF; sram_loc2  = 0xFFFFFFFF; sram_loc3  = 0xFFFFFFFF;
   // sram_loc4  = 0xFFFFFFFF; sram_loc5  = 0xFFFFFFFF; sram_loc6  = 0xFFFFFFFF; sram_loc7  = 0xFFFFFFFF;
   // sram_loc8  = 0xFFFFFFFF; sram_loc9  = 0xFFFFFFFF;  sram_loc10 = 0xFFFFFFFF;
   // // read sram 
   // cond1 = sram_loc0 == 0xFFFFFFFF && sram_loc1 == 0xFFFFFFFF && sram_loc2 == 0xFFFFFFFF && sram_loc3 == 0xFFFFFFFF ;
   // cond2 = sram_loc4 == 0xFFFFFFFF && sram_loc5 == 0xFFFFFFFF && sram_loc6 == 0xFFFFFFFF && sram_loc7 == 0xFFFFFFFF ;
   // cond3 = sram_loc8 == 0xFFFFFFFF && sram_loc9 == 0xFFFFFFFF && sram_loc10 == 0xFFFFFFFF ;
   // if ( cond1 & cond2 & cond3)
   //    send_packet(4); // read 1's from sram mem
   // else 
   //    send_packet(9); // error in reading


   // // writing 0's to the sram random mem
   // sram_loc0 = 0x0; sram_loc1 = 0x0; sram_loc2 = 0x0; sram_loc3 = 0x0; sram_loc4 = 0x0; sram_loc5 = 0x0;
   // sram_loc6 = 0x0; sram_loc7 = 0x0; sram_loc8 = 0x0; sram_loc9 = 0x0; sram_loc10 = 0x0;
   // // read sram 
   // cond1 = sram_loc0 == 0x0 && sram_loc1 == 0x0 && sram_loc2 == 0x0 && sram_loc3 == 0x0 ;
   // cond2 = sram_loc4 == 0x0 && sram_loc5 == 0x0 && sram_loc6 == 0x0 && sram_loc7 == 0x0 ;
   // cond3 = sram_loc8 == 0x0 && sram_loc9 == 0x0 && sram_loc10 == 0x0 ;
   // if ( cond1 & cond2 & cond3)
   //    send_packet(5); // read 0's from sram mem
   // else 
   //    send_packet(9); // error in reading