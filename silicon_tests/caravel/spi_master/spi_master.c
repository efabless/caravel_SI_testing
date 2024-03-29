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

// --------------------------------------------------------

/*
 *	SPI master Test
 *	- Enables SPI master
 *	- Uses SPI master to talk to external SPI module
 */
/*
Use SPI master to read the memory in file test_data

    @ enabling SPi
        send packet with size = 1

    @ read correct value
        send packet with size = 5

    @ read wrong value

        send packet with size = 9

    @ finish test
    send packet with size = 3
    send packet with size = 3
    send packet with size = 3

*/

void main()
{
    int i;
    uint32_t value;
    configure_mgmt_gpio();
    // For SPI operation, GPIO 1 should be an input, and GPIOs 2 to 4
    // should be outputs.
    configure_gpio(34,GPIO_MODE_MGMT_STD_INPUT_NOPULL); // SDI
    configure_gpio(35,GPIO_MODE_MGMT_STD_OUTPUT);       // SDO
    configure_gpio(33,GPIO_MODE_MGMT_STD_OUTPUT);       // CSB
    configure_gpio(32,GPIO_MODE_MGMT_STD_OUTPUT);       // SCK
    gpio_config_load();

    reg_spimaster_clk_divider = 0x4;
    enable_spi(1);
    enable_CS(1);  // sel=0, manual CS
    send_packet(2);
    count_down(PULSE_WIDTH * 5);

    value = spi_write_reg(); //

    //    spi_write(0x40); // Caravel Stream Write
    // for(int i = 0; i < 10000; i++);

    //    spi_write(0x01); // Write register for mfg code
    // for(int i = 0; i < 20000; i++);

    //    value = spi_read(); // 0xD

    if (value == 0x04)
        send_packet(5); // read correct value
    else
        send_packet(9); // read wrong value

    enable_CS(0);  // release CS
    enable_CS(1);  // sel=0, manual CS

    // End test
    send_packet(3);
    send_packet(3);
    send_packet(3);
}
