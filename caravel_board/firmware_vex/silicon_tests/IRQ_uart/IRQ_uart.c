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
#include <soc.h>
#include <irq_vex.h>
#include <uart.h>
#include <stub.c>

#include "send_packet.c"
#include "bitbang.c"

/*
Testing timer interrupts 
Enable interrupt for timer0 and configure it as countdown 1 shot 
wait for interrupt

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

*/

extern uint16_t flag;

void main(){
    uint16_t data;
    int i;

    flag = 0;
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_5 = 0x1803;

	clear_registers();	
    clock_in_right_o_left_o_standard(0); // 6	and 31	
    clock_in_right_o_left_i_standard(0); // 5	and 32	
    clock_in_right_o_left_i_standard(0); // 4	and 33	
    clock_in_right_o_left_i_standard(0); // 3	and 34	
    clock_in_right_o_left_i_standard(0); // 2	and 35	
    clock_in_right_o_left_i_standard(0); // 1	and 36	
    clock_in_right_o_left_i_standard(0); // 0	and 37	
    load();		 

    configure_mgmt_gpio();
    reg_uart_enable = 1;
    reg_uart_irq_en =1;
    irq_setmask(0);
	irq_setie(1);


	irq_setmask(irq_getmask() | (1 << UART_INTERRUPT));

    send_packet(1);//request sending data through the uart 
    print("M");

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 400000; 

    for (int i = 0; i < timeout; i++){
        if (flag == 1){
            send_packet(5);//test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass){
        send_packet(9);// timeout
    }

    // finish test
    send_packet(3);
    send_packet(3);
    send_packet(3);

}

