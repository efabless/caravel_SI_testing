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

    @wait for new character
        send packet with size = 4

    @recieved the correct character
        send packet with size = 6

    @recieve incorrect character
        send packet with size = 9

    @ finish test
        send packet with size = 3
        send packet with size = 3
        send packet with size = 3

*/

void uart_reception()
{
    int j;
    configure_mgmt_gpio();
    configure_gpio(6, GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5, GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    gpio_config_load();

    empty_buffer();

    uart_RX_enable(1);

    // Start test
    send_packet(2); // Start of the test

    send_packet(4);     // wait for new character
    wait_for_char("M"); // 0x4D

    send_packet(4);     // wait for new character
    wait_for_char("B"); // 0x42

    send_packet(4);     // wait for new character
    wait_for_char("A"); // 0
    uart_RX_enable(0);
}