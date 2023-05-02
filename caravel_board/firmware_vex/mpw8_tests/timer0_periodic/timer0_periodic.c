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

#include <uart.h>

#include "../defs.h"
#include "../common/send_packet.c"

/*
Testing timer interrupts 
Enable interrupt for timer0 and configure it as countdown 1 shot 
wait for interrupt

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

*/


void main(){
    uint32_t value;
    uint32_t old_value;

    configure_mgmt_gpio();

    send_packet(1);//configuring the timers and start count down

    /* Configure timer for a single-shot countdown */
	reg_timer0_config = 0; // disable
	reg_timer0_data = 0;
    reg_timer0_data_periodic  = 0x3000;
    reg_timer0_config = 1; // enable

    // Loop, waiting for the interrupt to change reg_mprj_datah
    // test path if counter value stop updated after reach 0 and also the value is always decrementing
    reg_timer0_update = 1; // update reg_timer0_value with new counter value
    old_value = reg_timer0_value;
    // value us decrementing until it reachs zero
    bool is_pass = false;
    int timeout = 400000; 
    for (int i = 0; i < timeout; i++){
        reg_timer0_update = 1; // update reg_timer0_value with new counter value
        value = reg_timer0_value;
        if (value > old_value){
            send_packet(5); //timer rollover
            is_pass = true;
            break;
        }
	    old_value = value;
    }

    if (!is_pass){
        send_packet(9); //timer hasn't rollover
    }

    // finish test
    send_packet(3);
    send_packet(3);
    send_packet(3);

}

