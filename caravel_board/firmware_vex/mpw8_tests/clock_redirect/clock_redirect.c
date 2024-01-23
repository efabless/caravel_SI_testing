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
checking user clock and caravel clock  at gpio 15 and gpio 14
    @finish configuring 
        send packet size = 2

   
*/

void main(){

    configure_mgmt_gpio();
    GPIOs_configure(14,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(15,GPIO_MODE_MGMT_STD_OUTPUT);
    /* Apply configuration */
    GPIOs_loadConfigs();
    reg_clk_out_dest = 0x6;
    send_packet(2); // 
    
}
