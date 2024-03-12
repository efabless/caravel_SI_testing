# caravel_SI_testing 

## requirements
- python 3.6 or later

## Installation
```
git clone https://github.com/efabless/caravel_SI_testing.git
pip install -r requirements.txt
```

## caravel.py

caravel.py is a wrapper that has APIs needed to test the silicon

- Initialise device and configures IOs
- Turns on the power supply and puts the positive power supply to 1.6v
- Flashes the CPU using `caravel_board/firmware_vex/util/caravel_hkflash.py`
- Receive Packet from the specified IO 
- Counts the pulses in the packet and displays the number of pulses

## Get started
To run the regression you can use `si_test.py`
```
python3 si_test.py [--option]
```
### options:
```  
  -f, --flash_only      Only Flash test
  
  -r, --run_only        Run test without flash
  
  -v, --verbose         Run with high verbosity
  
  -t TEST, --test TEST  Run Standalone test if in manifest
  
  -temp TEMPERATURE, --temperature TEMPERATURE
                        Temperature monitoring
                        
  -l, --last_test       Start the regression from the last test in the runs directory
```
**Find discription of all tests [here](/caravel_board/hex_files/README.md)**
