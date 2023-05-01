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
Testing IRQ interrupts 
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


void main(){
    clear_flag();
    configure_mgmt_gpio();

    // setting bit 7 as input
    configure_gpio(7, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    // gpio_config_io();

    // automatic bitbang approach
    gpio_config_load();

    enable_external1_irq(1);
    user_irq_1_ev_pending_write(1);
    send_packet(1);//wait for environment to make mprj[7] high 

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 400000;

    for (int i = 0; i < timeout; i++){
        if (get_flag() == 1){
            send_packet(5);//test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass)
    {
        send_packet(9); // timeout
    }

    // finish test
    send_packet(3);
    send_packet(3);
    send_packet(3);
}
