# caravel_SI_testing 

## requirements
- python 3.6 or later
- pyftdi (download using `pip3 install pyftdi`)

## caravel.py

caravel.py is a wrapper that has APIs needed to test the silicon

- Initialise device and configures IOs
- Turns on the power supply and puts the positive power supply to 1.6v
- Flashes the CPU using `caravel_board/firmware_vex/util/caravel_hkflash.py`
- Receive Packet from the specified IO 
- Counts the pulses in the packet and displays the number of pulses

## Get started

```
git clone git@github.com:efabless/caravel_SI_testing.git
python3 cpu_test.py [--option]
```
### options:
```  
  -sp, --send_packet    send packet test
  
  -b, --blink           blink test
  
  -cs, --cpu_stress     cpu stress test
  
  -ms, --mem_stress     memory stress test for both OPENram and DFFRAM
  
  -mtd, --mem_test_dffram
                        memory test for DFFRAM
                        
  -mts, --mem_test_sram
                        memory test for OPENram
                        
  -it, --irq_timer      IRQ timer test
  
  -to, --timer0_oneshot
                        timer0 oneshot test
                        
  -iu, --irq_uart       irq uart test
  
  -tp, --timer0_periodic
                        timer0 periodic test
                        
  -bb37, --cpu_bitbang_37_o
                        cpu_bitbang_37_o test
                        
  -bb36, --cpu_bitbang_36_o
                        cpu_bitbang_36_o test
                        
  -va, --voltage_all    automatically change test voltage
  
  -v VOLTAGE, --voltage VOLTAGE
                        change test voltage
                        
  -a, --all             run all tests
```
**Find discription of all tests [here](/caravel_board/hex_files/README.md)**


## Configure ios

Run the configuration of ios using:
```
python3 io_config.py --part <part_name> [--options]
```

### options:
```
  -o, --gpio_output     run gpio output configuration test
  
  -oh, --gpio_output_h  run gpio output high configuration test
  
  -oa, --gpio_output_all
                        run gpio output all configuration test
                        
  -ol, --gpio_output_l  run gpio output low configuration test
  
  -c, --chain           run gpio chain configuration test
  
  -v VOLTAGE, --voltage VOLTAGE
                        change test voltage
                        
  -va, --voltage_all    automatically change test voltage
  
  -p PART, --part PART  part name
```

# io configuration results

can be found [here](https://docs.google.com/spreadsheets/d/12yxbwXLbh5ytF1l4kJ_JKm7qokom1a_YTviKQIKbjMI/edit#gid=0)
