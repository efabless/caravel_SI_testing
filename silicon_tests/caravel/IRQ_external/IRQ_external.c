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
Enable interrupt for IRQ external pin mprj_io[7] -> should be drived to 1 by the environment

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

bool IRQ_external()
{

    clear_flag();

    configure_gpio(7,GPIO_MODE_MGMT_STD_INPUT_NOPULL);

    gpio_config_load();
    enable_external1_irq(1);
    reg_irq_source = 1;
    config_uart();
    print("Start Test: IRQ_external\n");

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout =  10000000;
//    int timeout = 100000000;

    for (int i = 0; i < timeout; i++)
    {
        if (get_flag() == 1)
        {
            is_pass = true;
            return true;
        }
    }
    if (!is_pass)
    {
        return false; // timeout
    }
}
