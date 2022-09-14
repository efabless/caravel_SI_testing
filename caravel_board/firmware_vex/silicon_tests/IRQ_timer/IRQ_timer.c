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

/*
Testing timer interrupts 
Enable interrupt for timer0 and configure it as countdown 1 shot 
wait for interrupt

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

*/

extern uint16_t flag;

void main(){
    uint16_t data;
    int i;

    flag = 0;
    configure_mgmt_gpio();

    irq_setmask(0);
	irq_setie(1);


	irq_setmask(irq_getmask() | (1 << TIMER0_INTERRUPT));

    /* Configure timer for a single-shot countdown */
	reg_timer0_config = 0;
	reg_timer0_data = 3000;
    reg_timer0_irq_en = 1;
    reg_timer0_config = 1;
    send_packet(1);//configuring the timers and start count down

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 4000; 

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

