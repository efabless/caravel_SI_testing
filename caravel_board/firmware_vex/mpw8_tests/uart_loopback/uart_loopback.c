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

#include <uart.h>

#include <defs.h>
// #include "send_packet.c"
// #include <defs.h>
#include <stub.c>
#include "../common/send_packet.c"
#include "../../gpio_config/gpio_config_io.c"

void wait_for_char(char *c)
{
    while (uart_rxempty_read() == 1)
        ;
    if (reg_uart_data == *c)
    {
        send_packet(6); // recieved the correct character
    }
    else
    {
        send_packet(9); // recieved incorrect correct character
    }
    uart_ev_pending_write(UART_EV_RX);
}
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
void set_registers()
{

    reg_mprj_io_0 = GPIO_MODE_MGMT_STD_ANALOG;
    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_5 = GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_7 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_8 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_9 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_10 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_11 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_12 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_13 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_14 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_15 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_16 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_17 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_18 = GPIO_MODE_MGMT_STD_OUTPUT;

    reg_mprj_io_19 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_20 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_21 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_22 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_23 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_24 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_25 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_26 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_27 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_28 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_29 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_30 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_31 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_32 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_33 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_34 = GPIO_MODE_MGMT_STD_OUTPUT;
    //    reg_mprj_io_34 = 0x0403;
    reg_mprj_io_35 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_36 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_37 = GPIO_MODE_MGMT_STD_OUTPUT;
    //    reg_mprj_io_37 = 0x0403;
}
void main()
{
    int j;
    configure_mgmt_gpio();
    set_registers();
    reg_mprj_datah = 0;
    reg_mprj_datal = 0;
    gpio_config_io();

    // clear_registers();
    // clock_in_right_o_left_o_standard(0); // 6	and 31
    // clock_in_right_o_left_i_standard(0); // 5	and 32
    // clock_in_right_o_left_i_standard(0); // 4	and 33
    // clock_in_right_o_left_i_standard(0); // 3	and 34
    // clock_in_right_o_left_i_standard(0); // 2	and 35
    // clock_in_right_o_left_i_standard(0); // 1	and 36
    // clock_in_right_o_left_i_standard(0); // 0	and 37
    // load();		                         //  load

    // Start test
    send_packet(2); // Start of the test

    reg_uart_enable = 1;

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