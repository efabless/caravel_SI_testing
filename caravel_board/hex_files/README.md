# tests senarios

## Cpu stress 

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

      
## Mem stress 	

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
      
## IRQ_timer

    @configuring the timers and start count down 
        send packet size = 1

    @received interrupt correctly  test pass
        send packet size = 5

    @ timeout                       test fail
        send packet size = 9

    @ end test 
        send packet size = 3
        send packet size = 3
        send packet size = 3

## timer0_oneshot

    @configuring the timers and start count down 
        send packet size = 1

    @timer reach 0
        send packet size = 5

    @ timer updated incorrectly
        send packet size = 9

    @ end test 
        send packet size = 3
        send packet size = 3
        send packet size = 3
        
## IRQ_uart 

    @request sending data through the uart 
        send packet size = 1

    @received interrupt correctly  test pass
        send packet size = 5

    @ timeout                       test fail
        send packet size = 9

    @ end test 
        send packet size = 3
        send packet size = 3
        send packet size = 3
        
## timer0_periodic 

    @configuring the timers and start count down 
        send packet size = 1

    @timer rollover  test pass
        send packet size = 5

    @ timer has not rollover
        send packet size = 9

    @ end test 
        send packet size = 3
        send packet size = 3
        send packet size = 3

## cpu_bitbang_left7
### gpio[7:0] used as output 
    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ sending each pulse at gpio[7:0] 
        send packet size = 5  # betweeb each 2 3-packet size gpio[7:0] should be monitored
    @ finish test 
        send packet size = 3 
        send packet size = 3 
        send packet size = 3 
### Following patterns should seen at gpio[7:0]
    gpio_7: 10 10 10 10 10 10 10 10 
    gpio_6: 00 10 10 10 10 10 10 10 
    gpio_5: 00 00 10 10 10 10 10 10 
    gpio_4: 00 00 00 10 10 10 10 10 
    gpio_3: 00 00 00 00 10 10 10 10 
    gpio_2: 00 00 00 00 00 10 10 10 
    gpio_1: 00 00 00 00 00 00 10 10
    gpio_0: 00 00 00 00 00 00 00 10 

## cpu_bitbang_left7_i
### gpio[7:0] used as input 
    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ waiting for pattern new pattern
        send packet size = 5  
    @ found pattern 
        send packet size = 7  
    @ can't find pattern timeout 
        send packet size = 9
    @ finish test 
        send packet size = 3 
        send packet size = 3 
        send packet size = 3 

### Following patterns should sent to gpio[7:0]
    0xAA 
    0x55  
    0xFF 
    0x00


## cpu_bitbang_right8
### gpio[37:30] used as output 
    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ sending each pulse at gpio[37:30] 
        send packet size = 7  # betweeb each 2 3-packet size gpio[37:30] should be monitored
    @ finish test 
        send packet size = 3 
        send packet size = 3 
        send packet size = 3 
### Following patterns should seen at gpio[7:0]
    gpio_37: 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
    gpio_36: 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 
    gpio_35: 00 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
    gpio_34: 00 00 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 
    gpio_33: 00 00 00 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
    gpio_32: 00 00 00 00 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 
    gpio_31: 00 00 00 00 00 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
    gpio_30: 00 00 00 00 00 00 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 


## cpu_bitbang_right8_i
### gpio[37:30] used as input 
    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ waiting for pattern new pattern
        send packet size = 5  
    @ found pattern 
        send packet size = 7  
    @ can't find pattern timeout 
        send packet size = 9
    @ finish test 
        send packet size = 3 
        send packet size = 3
        send packet size = 3

### Following patterns should sent to gpio[37:30]
    0xAA 
    0x55  
    0xFF 
    0x00

## IRQ_external
### mprj[7] used as input and need to be asserted 
    @wait for environment to make mprj[7] high
        send packet size = 1

    @received interrupt correctly  test pass
        send packet size = 5

    @ timeout                       test fail
        send packet size = 9

    @ end test 
        send packet size = 3
        send packet size = 3
        send packet size = 3
**NOTE** housekeeping SPI should used to update register irq_1_inputsrc to 1 see verilog code
 
## spi_master
### external memory should be used like the flash mem
    @ enabling SPi 
        send packet with size = 1

    @ read correct value 
        send packet with size = 5

    @ read wrong value 

        send packet with size = 9 

    @ finish test
    send packet with size = 3
    send packet with size = 3
    send packet with size = 3
**NOTE** csb=mprj_io[33], clk=mprj_io[32], io0=mprj_io[35], io1=mprj_io[34]
### external memory should have 
    @00000000
    6F 00 00 0B 93 01 00 00 13 02 63 57 b5 00 23 20
    13 00 00 00 13 00 00 00 13 00 00 00 13 00 00 00 

## uart
### SER_TX mprj[6] used as output 
**NOTE** python code should get all the data received on SER_TX and decode it code like the on at vip/tbuart.v
    
    @Start of transmitting 
        send packet with size = 2

    @End of transmitting
        send packet with size = 5

    @ finish test 
        send packet with size = 3
        send packet with size = 3
        send packet with size = 3

## uart_loopback
### SER_TX mprj[6] and SER_RX mprj[5] should be connected

    @Start of the test 
        send packet with size = 1

    @sent new character  
        send packet with size = 4
>Transmit any character and wait until receiev it back

    @recieved the correct character 
        send packet with size = 6

    @timeout didn't recieve the character 
        send packet with size = 9

    @ finish test 
        send packet with size = 3
        send packet with size = 3
        send packet with size = 3

 
## cpu_bitbang_#_o
### connect the # gpio as output

    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 1
    @ start sending 10 pulses at gpio[#] 
        send packet size = 5 
    @ stop sending pulses at gpio[#] 
        send packet size = 7
    @ finish test 
        send packet size = 3 
        send packet size = 3 
        send packet size = 3 

 
 
## cpu_bitbang_#_i
### connect the # gpio as input

    @ before bit bang
        send packet size = 1 
    @after bitbang 
        send packet size = 2
    @ wait for high input 
        send packet size = 5 
    @ wait for low input 
        send packet size = 7
    @ wait for high input 
        send packet size = 5 
    @ wait for low input 
        send packet size = 7
    @ can't find input timeout
        send packet size = 9
    @ finish test 
        send packet size = 3 
        send packet size = 3 
        send packet size = 3  

## mem_dff_test/mem_sram_test

   @ start of test 
      send packet with size = 1
   @ error reading 
      send packet with size = 9
   @ test finish 
      send packet with size = 3
      send packet with size = 3
      send packet with size = 3

 