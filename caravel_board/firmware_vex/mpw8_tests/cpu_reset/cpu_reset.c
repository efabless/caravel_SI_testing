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
check writing 1 in the reset register would restart the cpu program from the beginning 

    @ start of test 
        send packet of size 2
        send packet of size 3
    @ passing test 
        repeat the start of the test sequence
    @ failing test 
        send packet of 9 
*/

void main(){
    configure_mgmt_gpio();
    count_down(PULSE_WIDTH * 50);
    send_packet(2);
    send_packet(3);
    reg_hkspi_reset = 1;
    send_packet(9);
    return;
}