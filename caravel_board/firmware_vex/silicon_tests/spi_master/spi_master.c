/*
 * SPDX-FileCopyrightText: 2020 Efabless Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * SPDX-License-Identifier: Apache-2.0
 */

#include <defs.h>
#include <csr.h>
#include "send_packet.c"
#include "bitbang.c"
// --------------------------------------------------------

/*
 *	SPI master Test
 *	- Enables SPI master
 *	- Uses SPI master to talk to external SPI module
 */

 void spi_write(char c)
{
    reg_spimaster_wdata = (unsigned long) c;
//    reg_spimaster_wdata = c;
//    spi_master_control_length_write(8);
//    spi_master_control_start_write(1);
//    reg_spimaster_control = 0x0800;
    reg_spimaster_control = 0x0801;
}
 char spi_read()
{
//    reg_spimaster_wdata = c;
//    spi_master_control_length_write(8);
//    spi_master_control_start_write(1);
//    reg_spimaster_control = 0x0800;
//    spi_write(0x00);
//    reg_spimaster_rdata = 0x00;
//    reg_spimaster_control = 0x0801;
    spi_write(0x00);
    while (reg_spimaster_status != 1);
    return reg_spimaster_rdata;
}

/*
Use SPI master to read the memory in file test_data

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

*/

void main()
{
    int i;
    uint32_t value;
    configure_mgmt_gpio();

    // For SPI operation, GPIO 1 should be an input, and GPIOs 2 to 4
    // should be outputs.

    reg_mprj_io_34  = GPIO_MODE_MGMT_STD_INPUT_NOPULL;	// SDI
    reg_mprj_io_35  = GPIO_MODE_MGMT_STD_BIDIRECTIONAL;	// SDO
    reg_mprj_io_33  = GPIO_MODE_MGMT_STD_OUTPUT;	// CSB
    reg_mprj_io_32  = GPIO_MODE_MGMT_STD_OUTPUT;	// SCK


    if(0){
        /* Apply configuration */
        reg_mprj_xfer = 1;
        while (reg_mprj_xfer == 1);
    }

    if(1){
        clear_registers();		
        clock_in_right_o_left_i_standard(0); // 5	and 32	
        clock_in_right_o_left_i_standard(0); // 4	and 33	
        clock_in_right_i_left_i_standard(0); // 3	and 34	
        clock_in_right_i_left_io_standard(0); // 2	and 35	
        clock_in_right_o_left_i_standard(0); // 1	and 36	
        clock_in_right_o_left_i_standard(0); // 0	and 37	
        load();		         // 0   and 37 and load
    }


    send_packet(1); // enable the SPI

    reg_spi_enable = 1;
    reg_spimaster_cs = 0x10001;  // sel=0, manual CS

    spi_write(0x03);        // Write 0x03 (read mode)
    spi_write(0x00);        // Write 0x00 (start address high byte)
    spi_write(0x00);        // Write 0x00 (start address middle byte)
    spi_write(0x04);        // Write 0x04 (start address low byte)

    value = spi_read();
    
    if(value == 0x93){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 

    }


    value = spi_read();

    if(value == 0x01){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 

    }

    value = spi_read();

   if(value == 0x00){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 

    }
   
    reg_spimaster_cs = 0x0000;  // release CS
    reg_spimaster_cs = 0x10001;  // sel=0, manual CS

    spi_write(0x03);        // Write 0x03 (read mode)
    spi_write(0x00);        // Write 0x00 (start address high byte)
    spi_write(0x00);        // Write 0x00 (start address middle byte)
    spi_write(0x08);        // Write 0x08 (start address low byte)

    value = spi_read();

   if(value == 0x13){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 

    }

    value = spi_read();

   if(value == 0x02){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 

    }

    reg_spimaster_cs = 0x0000;  // release CS
    reg_spimaster_cs = 0x10001;  // sel=0, manual CS

    spi_write(0x03);        // Write 0x03 (read mode)
    spi_write(0x00);        // Write 0x00 (start address high byte)
    spi_write(0x00);        // Write 0x00 (start address middle byte)
    spi_write(0x0a);        // Write 0x0a (start address low byte)

    value = spi_read();

   if(value == 0x63){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 

    }

    value = spi_read();

   if(value == 0x57){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 

    }

    value = spi_read();

   if(value == 0xb5){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 
    }

    value = spi_read();

   if(value == 0){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 
    }

    value = spi_read();

   if(value == 0x23){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 
    }


    value = spi_read();

   if(value == 0x20){
        send_packet(5); // read correct value 
    } else{
        send_packet(9); // read wrong value 
    }

    reg_spimaster_cs = 0x0000;  // release CS
    reg_spimaster_cs = 0x10001;  // sel=0, manual CS

    // End test
    send_packet(3); 
    send_packet(3); 
    send_packet(3); 

}

