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
Connect the transimssion and the reciever of the uart
 Transmit any character and wait until receiev it back

    @Start of the test
        send packet with size = 2

    @recieved the correct character
        send packet with size = 6

    @recieve incorrect character
        send packet with size = 9

    @ finish test
        send packet with size = 3
        send packet with size = 3
        send packet with size = 3

*/

void uart_loopback()
{
    int j;
    configure_mgmt_gpio();
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    gpio_config_load();

    // Start test
    send_packet(2); // Start of the test

    uart_RX_enable(1);
    enable_uart_TX(1);

    print("M");
    for (j = 0; j < 1000; j++)
        ;
    wait_for_char("M");

    print("B");
    for (j = 0; j < 1000; j++)
        ;
    wait_for_char("B");

    print("A");
    for (j = 0; j < 1000; j++)
        ;
    wait_for_char("A");

    print("5");
    for (j = 0; j < 1000; j++)
        ;
    wait_for_char("5");

    print("o");
    for (j = 0; j < 1000; j++)
        ;
    wait_for_char("o");

    // finish test
    send_packet(3);
    send_packet(3);
    send_packet(3);
}