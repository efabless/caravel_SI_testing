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

// This include is relative to $CARAVEL_PATH (see Makefile)
// #include <defs.h>
// #include <stub.c>
#include "ctucan.c"
#include <common.h>

/*
 * Scan-chain Test:
 * - Configures directions for control ports
 *   +==========+===============+===========+
 *   | GPIO     | Functionality | Direction |
 *   +==========+===============+===========+
 *   | GPIO[0]  | TEST_EN       | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[1]  | IO_ISOL_N     | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[2]  | RESET         | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[8]  | VRp           | Analog    |
 *   +----------+---------------+-----------+
 *   | GPIO[9]] | VRm           | Analog    |
 *   +----------+---------------+-----------+
 *   | GPIO[11] | SC_TAIL       | output    |
 *   +----------+---------------+-----------+
 *   | GPIO[12] | CCFF_HEAD     | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[15] | Ain           | Analog    |
 *   +----------+---------------+-----------+
 *   | GPIO[16] | Aout          | Analog    |
 *   +----------+---------------+-----------+
 *   | GPIO[25] | CAN TX        | output    |
 *   +----------+---------------+-----------+
 *   | GPIO[26] | SC_HEAD       | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[27] | CAN RX        | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[30] | PROG_RESET    | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[35] | CCFF_TAIL     | output    |
 *   +----------+---------------+-----------+
 *   | GPIO[36] | CLK           | input     |
 *   +----------+---------------+-----------+
 *   | GPIO[37] | PROG_CLK      | input     |
 *   +----------+---------------+-----------+
*/

#define DAC_BASE        0x30040000
#define ADC_BASE        0x30080000

#define ADC_CTRL_SOC    0x1
#define ADC_CTRL_EN     0x2


#define dac_data_reg    (*(volatile uint32_t*)(DAC_BASE + 0))
#define dac_ena_reg     (*(volatile uint32_t*)(DAC_BASE + 4))

#define adc_ctrl__reg   (*(volatile uint32_t*)(ADC_BASE + 0))
#define adc_clkdiv_reg  (*(volatile uint32_t*)(ADC_BASE + 4))
#define adc_data_reg    (*(volatile uint32_t*)(ADC_BASE + 8))
#define adc_eoc_reg     (*(volatile uint32_t*)(ADC_BASE + 12))

void receive_frame()
{
	uint8_t data[64];
	uint32_t tmp;
	uint32_t ffw = ctucan_read_32(CTU_CAN_FD_RX_DATA_OFFSET);
	uint32_t id = ctucan_read_32(CTU_CAN_FD_RX_DATA_OFFSET);
	uint32_t ts_l = ctucan_read_32(CTU_CAN_FD_RX_DATA_OFFSET);
	uint32_t ts_h = ctucan_read_32(CTU_CAN_FD_RX_DATA_OFFSET);

	int j = 0;
	uint32_t rwcnt = (ffw >> 11) & 0x1F;
	for (int i = 0; i < rwcnt - 3; i++) {
		tmp = ctucan_read_32(CTU_CAN_FD_RX_DATA_OFFSET);
		data[i*4+0] = (tmp >> 0)  & 0xFF;
		data[i*4+1] = (tmp >> 8)  & 0xFF;
		data[i*4+2] = (tmp >> 16) & 0xFF;
		data[i*4+3] = (tmp >> 24) & 0xFF;
		j = i * 4;
	}
/*
	printf("\n# Received frame!\n");
	printf("Frame format:     %08X\n", ffw);
	printf("Frame identifier: %08X\n", id);
	printf("Frame timestamp L: %08X\n", ts_l);
	printf("Frame timestamp H: %08X\n", ts_h);
	printf("Frame data:");
	for (int i = 0; i < j; ++i) {
		printf("%02X ", data[i]);
	}
	printf("\n");
*/
}


void send_frame()
{
	/* Insert CAN frame to TXT buffer 1 */

	uint32_t frame_format_word = 0;
	frame_format_word |= 8;                                             // DLC 8
	frame_format_word |= (0 << 7);                                      // CAN 2.0 Frame
	ctucan_write_32(CTU_CAN_FD_TXT_BUFFER_1_OFFSET, frame_format_word);  // Store frame format word

	uint32_t id_word = (55 << 18);                                      // Identifier: 55
	ctucan_write_32(CTU_CAN_FD_TXT_BUFFER_1_OFFSET + 0x4, id_word);      // Store identifier word
	ctucan_write_32(CTU_CAN_FD_TXT_BUFFER_1_OFFSET + 0x8, 0);            //
	ctucan_write_32(CTU_CAN_FD_TXT_BUFFER_1_OFFSET + 0xC, 0);            // Transmit now
	ctucan_write_32(CTU_CAN_FD_TXT_BUFFER_1_OFFSET + 0x10, 0xAABBCCDD);  // Data: 0xAA, 0xBB, 0xCC, 0xDD
	ctucan_write_32(CTU_CAN_FD_TXT_BUFFER_1_OFFSET + 0x14, 0x11223344);  // Data: 0x11, 0x22, 0x33, 0x44

	/* Issue Set ready command */
	uint32_t command = 0;
	command |= 0x2;                                                     // Set Ready command
	command |= (1 << 8);                                                // Choose TXT Buffer 1
	ctucan_write_32(CTU_CAN_FD_TXT_COMMAND_OFFSET, command);             // Issue the command
}

int can_init(){
  ctucan_reset();

	//printf("Disabling CTU CAN\n");
	int ret = ctucan_disable();
	if (ret < 0) {
		//printf("Unable to disable CTU CAN core\n");
    dac_data_reg = 0x90;
		return(-1);
	}

	//printf("Configuring CTU CAN\n");
	ctucan_configure_interrupts();
	ctucan_configure();
	ctucan_enable_selfack();
	ctucan_enable_loop();

	//printf("Enabling CTU CAN\n");
	ret = ctucan_enable();
	if (ret < 0) {
		//printf("Unable to enable CTU CAN core\n");
    dac_data_reg = 0x91;
		return(-1);
	}

	//do {
		//printf("Waiting CTU CAN\n");
	//} 
  dac_data_reg = 0x80;
  while (!ctucan_is_initialized());

	//printf("CTU CAN initialized\n");
}


void main() {
  mgmt_gpio_wr(1);
  mgmt_gpio_o_enable();

  
  configure_all_gpios(GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
  // Only specify those should be in output mode
  configure_gpio(11,GPIO_MODE_USER_STD_OUTPUT);
  configure_gpio(35,GPIO_MODE_USER_STD_OUTPUT);
   // analog IOs
  configure_gpio(8,GPIO_MODE_USER_STD_ANALOG);
  configure_gpio(9,GPIO_MODE_USER_STD_ANALOG);
  configure_gpio(15,GPIO_MODE_USER_STD_ANALOG);
  configure_gpio(16,GPIO_MODE_USER_STD_ANALOG);

  // Implementation outputs
  configure_gpio(20,GPIO_MODE_USER_STD_OUTPUT);
  configure_gpio(25,GPIO_MODE_USER_STD_OUTPUT);

  gpio_config_load();


/*
  dac_data_reg = 0x69;

  (*(volatile uint32_t*)(0x30000000 + 0)) = 0xABCD0120;

  can_init();

  send_frame();

  receive_frame();
  */
//  dac_ena_reg = 1;
//   dac_data_reg = 10;
//   dac_data_reg = 20;
//   dac_data_reg = 50;
//   dac_ena_reg = 0;

//   adc_clkdiv_reg = 4; // adc_clk = sys_clk/10
//   adc_ctrl__reg = ADC_CTRL_EN;
//   adc_ctrl__reg = ADC_CTRL_EN | ADC_CTRL_SOC;
//   while(adc_eoc_reg == 0);
//   dac_data_reg = 70;
//   adc_ctrl__reg = ADC_CTRL_EN | ADC_CTRL_SOC;
//   while(adc_eoc_reg == 0);
//   dac_data_reg = 90;

//   dac_data_reg = 0x69;

 //(*(volatile uint32_t*)(0x30000000 + 0)) = 0xABCD6969;

  can_init();
//   dac_data_reg = 0x70;

	while (1){
  		send_frame();
 		mgmt_gpio_wr(0); // test finished 
		count_down(PULSE_WIDTH);
 		mgmt_gpio_wr(1); // test finished 
		count_down(PULSE_WIDTH);
	}
//   count_down(PULSE_WIDTH * 100);
  //   dac_data_reg = 0x71;

//   while(ctucan_is_rx_empty());
//   receive_frame();
//   dac_data_reg = 0x72;
  mgmt_gpio_wr(0); // test finished 

}