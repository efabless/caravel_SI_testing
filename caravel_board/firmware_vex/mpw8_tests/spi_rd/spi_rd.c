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

void main()
{
    int i;
    uint32_t value;
    configure_mgmt_gpio();
    // For SPI operation, GPIO 1 should be an input, and GPIOs 2 to 4
    // should be outputs.
    GPIOs_configure(34, GPIO_MODE_MGMT_STD_INPUT_NOPULL); // SDI
    GPIOs_configure(35, GPIO_MODE_MGMT_STD_OUTPUT);       // SDO
    GPIOs_configure(33, GPIO_MODE_MGMT_STD_OUTPUT);       // CSB
    GPIOs_configure(32, GPIO_MODE_MGMT_STD_OUTPUT);       // SCK
    GPIOs_loadConfigs();
    MSPI_enable(1);
    send_packet(2);
}