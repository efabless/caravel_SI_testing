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

#include <common.h>

/*
Testing timer interrupts 
Enable interrupt for timer0 and configure it as countdown 1 shot 
wait for interrupt

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

*/

bool timer0_oneshot()
{
    uint32_t value;
    uint32_t old_value;

    /* Configure timer for a single-shot countdown */
    timer0_configureOneShot(0xF3000);


    // Loop, waiting for the interrupt to change reg_mprj_datah
    // test path if counter value stop updated after reach 0 and also the value is always decrementing
    timer0_updateValue();  // update reg_timer0_value with new counter value
    old_value = timer0_readValue();
    // value us decrementing until it reachs zero
    while (1) {
        timer0_updateValue();  // update reg_timer0_value with new counter value
        value = timer0_readValue();
        if (value < old_value || value == 0){
            //send_packet(5); //timer updated correctly
            if (value==0)
                break;
        }else{
            return false; // timer updated incorrectly
        }
	    old_value = value;
        // if(value==0){
        //     //send_packet(7); //timer reach 0
        //     break;
        // }
    }

    // check after 10 iterations that value don't change from 0
	for (int i = 0; i < 10; i++);
        timer0_updateValue(); // update reg_timer0_value with new counter value

    if (timer0_readValue() == 0){
        return true; // timer updated correctly
    }else{
        return false; // timer updated incorrectly
    }
}
