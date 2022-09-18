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

#include <csr.h>
#include <soc.h>
#include <irq_vex.h>
#include <uart.h>

#include <defs.h>
#include "send_packet.c"
// #include "bitbang.c"
#include "../../gpio_config/gpio_config_io.c"

/*
Testing timer interrupts 
Enable interrupt for IRQ external pin mprj_io[7] -> should be drived to 1 by the environment
**NOTE** housekeeping SPI should used to update register irq_1_inputsrc to 1 see verilog code

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

*/

extern uint16_t flag;

void main(){
    uint16_t data;
    int i;

    flag = 0;
    configure_mgmt_gpio();

    // setting bit 7 as input 
    reg_mprj_io_7 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    gpio_config_io();
    //  bitbang approach
    // if(1){
    //     clear_registers();	
    //     clock_in_right_o_left_i_standard(0); // 7	and 30	
    //     clock_in_right_o_left_i_standard(0); // 6	and 31	
    //     clock_in_right_o_left_i_standard(0); // 5	and 32	
    //     clock_in_right_o_left_i_standard(0); // 4	and 33	
    //     clock_in_right_o_left_i_standard(0); // 3	and 34	
    //     clock_in_right_o_left_i_standard(0); // 2	and 35	
    //     clock_in_right_o_left_i_standard(0); // 1	and 36	
    //     clock_in_right_o_left_i_standard(0); // 0	and 37	
    //     load();		         // 0   and 37 and load
    // }

    // automatic bitbang approach
    if(0){
        reg_mprj_xfer = 1;
        while (reg_mprj_xfer == 1);
    }


    irq_setmask(0);
	irq_setie(1);

	// irq_setmask(irq_getmask() | (1 << TIMER0_INTERRUPT));

	// irq_setmask(irq_getmask() | 0x3f);
	irq_setmask(irq_getmask() | (1 << USER_IRQ_4_INTERRUPT));
	// irq_setmask(irq_getmask() | ( 0x3f));
    reg_user4_irq_en =1;
    send_packet(1);//wait for environment to make mprj[7] high 

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

