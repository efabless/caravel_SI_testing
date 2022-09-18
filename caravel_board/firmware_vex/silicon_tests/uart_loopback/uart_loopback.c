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
#include <stub.c>
#include "send_packet.c"
// #include "bitbang.c"
#include "../../gpio_config/gpio_config_io.c"

void wait_for_char(char *c){
    int time_out = 1000000;
    bool is_found = false;
    for (int i = 0; i < time_out; i++)
    {
        if (reg_uart_data == *c){
            is_found =  true;
            send_packet(6); // recieved the correct character
            break;
        }
    }
    if (~is_found){
        send_packet(9); // timeout didn't recieve the character
    }
}

/*
Connect the transimssion and the reciever of the uart 
 Transmit any character and wait until receiev it back

    @Start of the test 
        send packet with size = 1

    @sent new character 
        send packet with size = 4

    @recieved the correct character 
        send packet with size = 6

    @timeout didn't recieve the character 
        send packet with size = 9

    @ finish test 
        send packet with size = 3
        send packet with size = 3
        send packet with size = 3

*/

void main()
{
    int j;
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_5 = 0x1803;
    gpio_config_io();

	// clear_registers();	
    // clock_in_right_o_left_o_standard(0); // 6	and 31	
    // clock_in_right_o_left_i_standard(0); // 5	and 32	
    // clock_in_right_o_left_i_standard(0); // 4	and 33	
    // clock_in_right_o_left_i_standard(0); // 3	and 34	
    // clock_in_right_o_left_i_standard(0); // 2	and 35	
    // clock_in_right_o_left_i_standard(0); // 1	and 36	
    // clock_in_right_o_left_i_standard(0); // 0	and 37	
    // load();		                         //  load


    configure_mgmt_gpio();

    reg_uart_enable = 1;

    // Start test
    send_packet(1); // Start of the test

    print("M");
    send_packet(4); // sent new character
    wait_for_char("M");
    
    
    print("B");
    send_packet(4); // sent new character
    wait_for_char("B");
    
        
    print("F");
    send_packet(4); // sent new character
    wait_for_char("F");


    // finish test
    send_packet(3); 
    send_packet(3); 
    send_packet(3); 

}
