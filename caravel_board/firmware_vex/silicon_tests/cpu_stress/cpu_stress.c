#include <defs.h>
#include "send_packet.c"

// --------------------------------------------------------
// Main program entry point
// --------------------------------------------------------
int A[]={1, 40, 2, 5, 22, 11, 90, 200, 10, 20, 25};

// int factorial(int n) {
//    int fac=1;
//    for(int i=1; i<=n;++i){
//       fac = fac * i; 
//    }
//    return fac;
// }

int fibbonacci(int n) {
   if(n == 0){
      return 0;
   } else if(n == 1) {
      return 1;
   } else {
      return (fibbonacci(n-1) + fibbonacci(n-2));
   }
}

void recursiveInsertionSort(int arr[], int n){
   if (n <= 1)
      return;
   recursiveInsertionSort( arr, n-1 );
   int nth = arr[n-1];
   int j = n-2;
   while (j >= 0 && arr[j] > nth){
      arr[j+1] = arr[j];
      j--;
   }
   arr[j+1] = nth;
}


void quick_sort(int number[],int first,int last){
   int i, j, pivot, temp;

   if(first<last){
      pivot=first;
      i=first;
      j=last;

      while(i<j){
         while(number[i]<=number[pivot]&&i<last)
            i++;
         while(number[j]>number[pivot])
            j--;
         if(i<j){
            temp=number[i];
            number[i]=number[j];
            number[j]=temp;
         }
      }

      temp=number[pivot];
      number[pivot]=number[j];
      number[j]=temp;
      quick_sort(number,first,j-1);
      quick_sort(number,j+1,last);

   }
}
int f4(int a, int b, int c, int d){
   return a + b + c + d;
}

int f5(int a, int b, int c, int d, int e){
   return e + f4(a, b, c, d);
}

int f6(int a, int b, int c, int d, int e, int f){
   return f + f5(a, b, c, d, e);
}

int f7(int a, int b, int c, int d, int e, int f, int g){
   return g + f6(a, b, c, d, e, f);
}
int f8(int a, int b, int c, int d, int e, int f, int g, int h){
   return h + f7(a, b, c, d, e, f, g);
}
/*

   @ pass first phase
      send packet with size = 1
   @ pass second phase 
      send packet with size = 2
   @ pass third phase 
      send packet with size = 3
   @ pass forth phase 
      send packet with size = 4
   @ pass fifth phase 
      send packet with size = 5
   @ failing any phase 
      send packet with size = 9
   @ test finish 
      send packet with size = 1
      send packet with size = 1
      send packet with size = 1
   
*/
void main()
{
   int n;
   int B[10];
    configure_mgmt_gpio();

    // start test
   //  reg_mprj_datal = 0xAAAA0000;

   //  n =factorial(12);
   //  if(n != 479001600)
   //      reg_mprj_datal = 0xFFFF0000; //fail

   //  reg_mprj_datal = 0x11110000; //phase 1 pass

   n = fibbonacci(10);
   if(n != 55)
      send_packet(9); // fail
   else
      send_packet(1);//phase 1 pass 
	
    int sumA = 0;
    for(int i=0; i<10; i++){
        B[i] = A[i];
        sumA += A[i];
    }

   if(sumA != 401)
      send_packet(9); // fail
   else 
    send_packet(2); //phase 2 pass

    recursiveInsertionSort(B, 10);

    int sumB = 0;
    for(int i=0; i<10; i++){
        sumB += B[i];
    }

   if(sumA != sumB)
      send_packet(9); // fail
   else 
      send_packet(3); //phase 3 pass

    for(int i=0; i<10; i++){
        B[i] = A[i];
        sumA += A[i];
    }
    quick_sort(B, 0, 9);

    for(int i=0; i<10; i++){
        sumB += B[i];
    }

   if(sumA != sumB)
      send_packet(9); // fail
   else 
      send_packet(4); //phase 4 pass
    
    int sum = f8(10, 20, 30, 40, 50, 60, 70, 80);

   if(sum != (10+20+30+40+50+60+70+80))
      send_packet(9); // fail
   else 
      send_packet(5); //phase 5 pass

   // test finish 
   send_packet(1);
   send_packet(1);
   send_packet(1);
}