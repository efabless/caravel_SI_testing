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
#include <stub.c>
#include "send_packet.c"

/*
send pattern Monitor: Test UART (RTL) passed\n on UART SER_TX mprj[6]
python code should get all the data received on mprj and decode it code like the on at vip/tbuart.v

    @Start of transmitting 
        send packet with size = 2

    @End of transmitting
        send packet with size = 5

    @ finish test 
        send packet with size = 3
        send packet with size = 3
        send packet with size = 3

*/
void main(){
    int j;
    configure_mgmt_gpio();

    reg_uart_enable = 1;

    // Start test
    send_packet(2); // start of transmitting

    print("Monitor: Test UART (RTL) passed\n");

    // Allow transmission to complete before signalling that the program
    // has ended.
    for (j = 0; j < 160; j++);
    send_packet(5); // end of transmitting

    // finish test
    send_packet(3); 
    send_packet(3); 
    send_packet(3); 

}
