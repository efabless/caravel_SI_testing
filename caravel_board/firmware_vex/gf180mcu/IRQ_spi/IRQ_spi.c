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
Testing uart interrupts
Enable interrupt for timer0 and configure it as countdown 1 shot
wait for interrupt

    @enable irq for spi
        send packet size = 2

    @received interrupt correctly  test pass
        send packet size = 5

    @ timeout                       test fail
        send packet size = 9

    @ end test
        send packet size = 3
        send packet size = 3
        send packet size = 3

*/

bool IRQ_spi()
{

    clear_flag();
    enable_hk_spi_irq(1);
    user_irq_0_ev_pending_write(1);
    reg_hkspi_irq = 1;
    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 400000;

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
        return false;
    }
}
