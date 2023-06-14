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

int wait_for_char()
{
    int uart_temp;
    while (uart_rxempty_read() == 1);
    uart_temp = reg_uart_data;
   
    UART_popChar();
    return uart_temp;
}

void send_uart(int data){
    while (reg_uart_txfull == 1);
	reg_uart_data = data;
 }
/*

    @Start of the test
        send packet with size = 2

    @recieve new character
        send packet with size = 4

    

*/

void main()
{
    int j;
    configure_mgmt_gpio();
    GPIOs_configure(6, GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    GPIOs_loadConfigs();

    UART_enableRX(1);
    UART_enableTX(1);

    // Start test
    send_packet(2); // Start of the test

    int int_rec;
    while(true){
        int_rec = wait_for_char(); 
        send_packet(4);     // wait for new character
        send_uart(int_rec);
    }

}