#define     SET_BIT(reg, bit)       (reg) = ((reg) | (1<<bit))
#define     CLR_BIT(reg, bit)       (reg) = ((reg) & (~(1<<bit)))
#define     CHK_BIT(reg, bit)       ((reg) & (1<<bit))

#define SRAM_BASE_ADDR          0x20000000
#define DFFRAM_BASE_ADDR        0x21000000
#define APB_GPIOA_BASE_ADDR     0x40000000
#define APB_TMR0_BASE_ADDR      0x40010000
#define APB_TMR1_BASE_ADDR      0x40020000
#define APB_UART0_BASE_ADDR     0x40030000
#define APB_SPI_BASE_ADDR       0x40040000
#define HKSPI_PORT_BASE_ADDR    0x40050000
#define APB_DBG_BASE_ADDR       0x40060000
#define AHB_EXT_BASE_ADDR       0x41000000
#define MGMT_REGS_BASE_ADDR     0xA0000000

// GPIO: PORTA & PORTB
#define GPIO_DATA_REG           0x00000000
#define GPIO_OE_REG             0x00000008
#define GPIO_IM_REG             0x00000010
#define GPIO_IE_REG             0x00000018
#define GPIO_MODE0_REG          0x00000020
#define GPIO_MODE1_REG          0x00000028


unsigned int volatile *const GPIOA_DATA = (unsigned int *)(APB_GPIOA_BASE_ADDR + GPIO_DATA_REG);
unsigned int volatile *const GPIOA_OE = (unsigned int *)(APB_GPIOA_BASE_ADDR + GPIO_OE_REG);
unsigned int volatile *const GPIOA_IM = (unsigned int *)(APB_GPIOA_BASE_ADDR + GPIO_IM_REG);
unsigned int volatile *const GPIOA_IE = (unsigned int *)(APB_GPIOA_BASE_ADDR + GPIO_IE_REG);
unsigned int volatile *const GPIOA_MODE0 = (unsigned int *)(APB_GPIOA_BASE_ADDR + GPIO_MODE0_REG);
unsigned int volatile *const GPIOA_MODE1 = (unsigned int *)(APB_GPIOA_BASE_ADDR + GPIO_MODE1_REG);

/*
unsigned int volatile *const GPIOB_DATA = (unsigned int *)(APB_GPIOB_BASE_ADDR + GPIO_DATA_REG);
unsigned int volatile *const GPIOB_OE = (unsigned int *)(APB_GPIOB_BASE_ADDR + GPIO_OE_REG);
unsigned int volatile *const GPIOB_IE = (unsigned int *)(APB_GPIOB_BASE_ADDR + GPIO_INTE_REG);
*/

// TMR: TMR0 & TMR1
#define TMR_CTRL_REG            0x00000000
#define TMR_VAL_REG             0x00000004
#define TMR_LOAD_REG            0x00000008
#define TMR_INT_REG             0x0000000C

unsigned int volatile *const TMR0_CTRL = (unsigned int *)(APB_TMR0_BASE_ADDR + TMR_CTRL_REG);
unsigned int volatile *const TMR0_VAL = (unsigned int *)(APB_TMR0_BASE_ADDR + TMR_VAL_REG);
unsigned int volatile *const TMR0_LOAD = (unsigned int *)(APB_TMR0_BASE_ADDR + TMR_LOAD_REG);
unsigned int volatile *const TMR0_ISC = (unsigned int *)(APB_TMR0_BASE_ADDR + TMR_INT_REG);

unsigned int volatile *const TMR1_CTRL = (unsigned int *)(APB_TMR1_BASE_ADDR + TMR_CTRL_REG);
unsigned int volatile *const TMR1_VAL = (unsigned int *)(APB_TMR1_BASE_ADDR + TMR_VAL_REG);
unsigned int volatile *const TMR1_LOAD = (unsigned int *)(APB_TMR1_BASE_ADDR + TMR_LOAD_REG);
unsigned int volatile *const TMR1_ISC = (unsigned int *)(APB_TMR1_BASE_ADDR + TMR_INT_REG);

// UART" UART0 & UART1
#define UART_DATA_REG           0x00000000
#define UART_STAT_REG           0x00000004
#define UART_CTRL_REG           0x00000008
#define UART_ISC_REG            0x0000000C
#define UART_BDIV_REG           0x00000010

unsigned int volatile *const UART0_DATA = (unsigned int *)(APB_UART0_BASE_ADDR + UART_DATA_REG);
unsigned int volatile *const UART0_STAT = (unsigned int *)(APB_UART0_BASE_ADDR + UART_STAT_REG);
unsigned int volatile *const UART0_CTRL = (unsigned int *)(APB_UART0_BASE_ADDR + UART_CTRL_REG);
unsigned int volatile *const UART0_ISC = (unsigned int *)(APB_UART0_BASE_ADDR + UART_ISC_REG);
unsigned int volatile *const UART0_BDIV = (unsigned int *)(APB_UART0_BASE_ADDR + UART_BDIV_REG);

/*
unsigned int volatile *const UART1_DATA = (unsigned int *)(APB_UART1_BASE_ADDR + UART_DATA_REG);
unsigned int volatile *const UART1_STAT = (unsigned int *)(APB_UART1_BASE_ADDR + UART_STAT_REG);
unsigned int volatile *const UART1_CTRL = (unsigned int *)(APB_UART1_BASE_ADDR + UART_CTRL_REG);
unsigned int volatile *const UART1_ISC = (unsigned int *)(APB_UART1_BASE_ADDR + UART_ISC_REG);
unsigned int volatile *const UART1_BDIV = (unsigned int *)(APB_UART1_BASE_ADDR + UART_BDIV_REG);
*/
/* SPI Master Controllers */
#define SPI_DATA_REG            0x00
#define SPI_CFG_REG             0x08
#define SPI_STATUS_REG          0x10
#define SPI_CTRL_REG            0x18
#define SPI_PRE_REG             0x20
#define SPI_IM_REG              0x30
#define SPI_IC_REG              0x38

// CTRL register fields
#define     SPI_GO_BIT          0x0
#define     SPI_GO_SIZE         0x1
#define     SPI_SS_BIT          0x1
#define     SPI_SS_SIZE         0x1

// CFG register fields
#define     SPI_CPOL_BIT        0x0
#define     SPI_CPOL_SIZE       0x1
#define     SPI_CPHA_BIT        0x1
#define     SPI_CPHA_SIZE       0x1
#define     SPI_CLKDIV_BIT      0x2
#define     SPI_CLKDIV_SIZE     0x8

// status register fields
#define     SPI_DONE_BIT        0x0
#define     SPI_DONE_SIZE       0x1

unsigned int volatile *const SPI_CTRL = (unsigned int *)(APB_SPI_BASE_ADDR + SPI_CTRL_REG);
unsigned int volatile *const SPI_DATA = (unsigned int *)(APB_SPI_BASE_ADDR + SPI_DATA_REG);
unsigned int volatile *const SPI_STATUS = (unsigned int *)(APB_SPI_BASE_ADDR + SPI_STATUS_REG);
unsigned int volatile *const SPI_CFG = (unsigned int *)(APB_SPI_BASE_ADDR + SPI_CFG_REG);
unsigned int volatile *const SPI_IM = (unsigned int *)(APB_SPI_BASE_ADDR + SPI_IM_REG);
unsigned int volatile *const SPI_IC = (unsigned int *)(APB_SPI_BASE_ADDR + SPI_IC_REG);
unsigned int volatile *const SPI_PRE = (unsigned int *)(APB_SPI_BASE_ADDR + SPI_PRE_REG);


/* I2C Master Controller */
/*
#define     I2C_PRE_LO_REG      0x0
#define     I2C_PRE_HI_REG      0x8
#define     I2C_CTRL_REG        0x10
#define     I2C_TX_REG          0x18
#define     I2C_RX_REG          0x20
#define     I2C_CMD_REG         0x28
#define     I2C_STAT_REG        0x30
#define     I2C_IM_REG          0x38

#define     I2C_CMD_STA         0x80
#define     I2C_CMD_STO         0x40
#define     I2C_CMD_RD          0x20
#define     I2C_CMD_WR          0x10
#define     I2C_CMD_ACK         0x08
#define     I2C_CMD_IACK        0x01

#define     I2C_CTRL_EN         0x80
#define     I2C_CTRL_IEN        0x40

#define     I2C_STAT_RXACK      0x80
#define     I2C_STAT_BUSY       0x40
#define     I2C_STAT_AL         0x20
#define     I2C_STAT_TIP        0x02
#define     I2C_STAT_IF         0x01

unsigned int volatile * const I2C_PRE_LO = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_PRE_LO_REG);
unsigned int volatile * const I2C_PRE_HI = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_PRE_HI_REG);
unsigned int volatile * const I2C_CTRL = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_CTRL_REG);
unsigned int volatile * const I2C_TX = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_TX_REG);
unsigned int volatile * const I2C_RX = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_RX_REG);
unsigned int volatile * const I2C_CMD = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_CMD_REG);
unsigned int volatile * const I2C_STAT = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_STAT_REG);
unsigned int volatile * const I2C_IM = (unsigned int *) (APB_I2C_BASE_ADDR + I2C_IM_REG);
*/

unsigned int volatile *const DBG_DATA = (unsigned int *)(APB_DBG_BASE_ADDR + GPIO_DATA_REG);
unsigned int volatile *const DBG_OE = (unsigned int *)(APB_DBG_BASE_ADDR + GPIO_OE_REG);
unsigned int volatile *const DBG_IM = (unsigned int *)(APB_DBG_BASE_ADDR + GPIO_IM_REG);

#define LA_IN_REG0      0x00
#define LA_IN_REG1      0x04
#define LA_OUT_REG0     0x10
#define LA_OUT_REG1     0x14
#define LA_OEB_REG0     0x20
#define LA_OEB_REG1     0x24
#define LA_IEA_REG0     0x30
#define LA_IEA_REG1     0x34
#define MGMT_CTRL_REG   0x40

#define DBG         0x10
#define SPI         0x20
#define UART        0x40
#define USER_AHB    0x08
// #define USER_IRQ0   0x01
// #define USER_IRQ1   0x02
// #define USER_IRQ2   0x04

unsigned int volatile *const MGMT_CTRL = (unsigned int *)(MGMT_REGS_BASE_ADDR + MGMT_CTRL_REG);

// address translation: 4005ABB0 <==> 26A0_00BB
#define HK_SPI_STATUS   0x1000
#define HK_SPI_PRODID   0x1040
#define HK_SPI_PRJID    0x1080
#define HK_SPI_PLLEN    0x10C0
#define HK_SPI_PLLBP    0x1100
#define HK_SPI_IRQ      0x1140
#define HK_SPI_RESET    0x1180
#define HK_SPI_TRAP     0x1280
#define HK_SPI_PLLTRIM  0x11C0
#define HK_SPI_SRC      0x1200
#define HK_SPI_DIV      0x1240

#define HK_SYS_POWER    0x2000
#define HK_SYS_OUTREDIR 0x2040          
#define HK_SYS_INREDIR  0x20C0          
#define HK_SYS_SPIDIS   0x2100

#define HK_GPIO_CTRL    0x0000
#define HK_GPIO_PWRCTRL 0x0040

// configurations
#define ARM    1
#define SKY    1
#define AHB    1
#define LA_SIZE 64
#define CTRL_BITS_SIZE   13 // number of control bits in gpio control module 
#define TRAP_SUP 0 // trap support
#define PLL_SUP 0 // pll support

#define reg_mprj_xfer   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x000))
#define reg_mprj_datal  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x0c0))
#define reg_mprj_datah  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x100))
#define reg_mprj_io_0   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x240))
#define reg_mprj_io_1   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x280))
#define reg_mprj_io_2   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x2c0))
#define reg_mprj_io_3   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x300))
#define reg_mprj_io_4   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x340))
#define reg_mprj_io_5   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x380))
#define reg_mprj_io_6   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x3c0))
#define reg_mprj_io_7   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x400))
#define reg_mprj_io_8   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x440))
#define reg_mprj_io_9   (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x480))
#define reg_mprj_io_10  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x4c0))
#define reg_mprj_io_11  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x500))
#define reg_mprj_io_12  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x540))
#define reg_mprj_io_13  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x580))
#define reg_mprj_io_14  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x5c0))
#define reg_mprj_io_15  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x600))
#define reg_mprj_io_16  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x640))
#define reg_mprj_io_17  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x680))
#define reg_mprj_io_18  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x6c0))
#define reg_mprj_io_19  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x700))
#define reg_mprj_io_20  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x740))
#define reg_mprj_io_21  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x780))
#define reg_mprj_io_22  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x7c0))
#define reg_mprj_io_23  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x800))
#define reg_mprj_io_24  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x840))
#define reg_mprj_io_25  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x880))
#define reg_mprj_io_26  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x8c0))
#define reg_mprj_io_27  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x900))
#define reg_mprj_io_28  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x940))
#define reg_mprj_io_29  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x980))
#define reg_mprj_io_30  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0x9c0))
#define reg_mprj_io_31  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0xa00))
#define reg_mprj_io_32  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0xa40))
#define reg_mprj_io_33  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0xa80))
#define reg_mprj_io_34  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0xac0))
#define reg_mprj_io_35  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0xb00))
#define reg_mprj_io_36  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0xb40))
#define reg_mprj_io_37  (*(volatile unsigned int*)(HKSPI_PORT_BASE_ADDR + 0xb80))


#define USER_SPACE_ADDR 0x41000000 
#define USER_SPACE_SIZE 0xFFFFFC // sum with USER_SPACE_ADDR is the address of last address

// Debug reg DEBUG_ON
#define reg_debug_1 (*(volatile unsigned int*)(AHB_EXT_BASE_ADDR + USER_SPACE_SIZE))
#define reg_debug_2 (*(volatile unsigned int*)(AHB_EXT_BASE_ADDR + USER_SPACE_SIZE - 4))

// Useful GPIO mode values
// #define GPIO_MODE_MGMT_STD_INPUT_NOPULL    0x0403
// #define GPIO_MODE_MGMT_STD_INPUT_PULLDOWN  0x0c01
// #define GPIO_MODE_MGMT_STD_INPUT_PULLUP	   0x0801
// #define GPIO_MODE_MGMT_STD_OUTPUT	   0x1809
// #define GPIO_MODE_MGMT_STD_BIDIRECTIONAL   0x1801
// #define GPIO_MODE_MGMT_STD_ANALOG   	   0x000b

// #define GPIO_MODE_USER_STD_INPUT_NOPULL	   0x0402
// #define GPIO_MODE_USER_STD_INPUT_PULLDOWN  0x0c00
// #define GPIO_MODE_USER_STD_INPUT_PULLUP	   0x0800
// #define GPIO_MODE_USER_STD_OUTPUT	   0x1808
// #define GPIO_MODE_USER_STD_BIDIRECTIONAL   0x1800
// #define GPIO_MODE_USER_STD_OUT_MONITORED   0x1802
// #define GPIO_MODE_USER_STD_ANALOG   	   0x000a

/*
[2:0] USER_IRQ_ENa 
[3] AHB_Ena // to enable interface with user project
[4]DBG_ENa
[5]SPI_ENa
[6]UART_ENa
[7]QSPI_ENa
*/
// unsigned int volatile  *const MGMT_CTRL = (unsigned int *)(MGMT_REGS_BASE_ADDR + MGMT_CTRL_REG);
#define reg_wb_enable (*(volatile unsigned int*)(MGMT_REGS_BASE_ADDR + MGMT_CTRL_REG))


// Housekeeping
#define reg_hkspi_status      (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_STATUS))
#define reg_hkspi_chip_id     (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_PRODID))
#define reg_hkspi_user_id     (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_PRJID))
#define reg_hkspi_pll_ena     (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_PLLEN))
#define reg_hkspi_pll_bypass  (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_PLLBP))
#define reg_hkspi_irq         (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_IRQ))
#define reg_hkspi_reset       (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_RESET))
#define reg_hkspi_trap        (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_TRAP))
#define reg_hkspi_pll_trim    (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_PLLTRIM))
#define reg_hkspi_pll_source  (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_SRC))
#define reg_hkspi_pll_divider (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SPI_DIV))
#define reg_hkspi_disable     (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SYS_SPIDIS))
#define reg_clk_out_dest      (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SYS_OUTREDIR))
#define reg_irq_source        (*(volatile unsigned int*) (HKSPI_PORT_BASE_ADDR + HK_SYS_INREDIR))

// Mgmt gpio (0x4000_0000)
#define reg_gpio_mode1  (*(volatile unsigned int*) (APB_GPIOA_BASE_ADDR + 0x28))
#define reg_gpio_mode0  (*(volatile unsigned int*) (APB_GPIOA_BASE_ADDR + 0x20))
#define reg_gpio_ien    (*(volatile unsigned int*) (APB_GPIOA_BASE_ADDR + 0x18))
#define reg_gpio_oe     (*(volatile unsigned int*) (APB_GPIOA_BASE_ADDR + 0x8))
#define reg_gpio_in     (*(volatile unsigned int*) (APB_GPIOA_BASE_ADDR + 0x0))
#define reg_gpio_out    (*(volatile unsigned int*) (APB_GPIOA_BASE_ADDR + 0x0))
#define REG_GPIO_INVERTED 1

// Timer 0 
#define reg_timer0_config           (*(volatile unsigned int*) (APB_TMR0_BASE_ADDR + TMR_CTRL_REG))
#define reg_timer0_data             (*(volatile unsigned int*) (APB_TMR0_BASE_ADDR + TMR_VAL_REG))       
#define reg_timer0_data_periodic    (*(volatile unsigned int*) (APB_TMR0_BASE_ADDR + TMR_LOAD_REG))   
#define reg_timer0_irq              (*(volatile unsigned int*) (APB_TMR0_BASE_ADDR + TMR_INT_REG))      

// UART
#define reg_uart_data     (*(volatile unsigned int*) (APB_UART0_BASE_ADDR + UART_DATA_REG))
#define reg_uart_stat     (*(volatile unsigned int*) (APB_UART0_BASE_ADDR + UART_STAT_REG))
#define reg_uart_ctrl     (*(volatile unsigned int*) (APB_UART0_BASE_ADDR + UART_CTRL_REG))
#define reg_uart_isc      (*(volatile unsigned int*) (APB_UART0_BASE_ADDR + UART_ISC_REG))
#define reg_uart_clkdiv   (*(volatile unsigned int*) (APB_UART0_BASE_ADDR + UART_BDIV_REG))


// SPI Master Configuration      
#define reg_spimaster_wdata        (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_DATA_REG))
#define reg_spimaster_rdata        (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_DATA_REG))
#define reg_spimaster_cfg          (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_CFG_REG))
#define reg_spimaster_status       (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_STATUS_REG))
#define reg_spimaster_control      (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_CTRL_REG))
#define reg_spimaster_clk_divider  (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_PRE_REG))
#define reg_spi_IM                 (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_IM_REG))
#define reg_spi_IC                 (*(volatile unsigned int*) (APB_SPI_BASE_ADDR + SPI_IC_REG))


// Logic Analyzer
#define reg_la1_data    (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_OUT_REG1))
#define reg_la0_data    (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_OUT_REG0))

#define reg_la1_data_in (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_IN_REG1))
#define reg_la0_data_in (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_IN_REG0))

#define reg_la1_oenb    (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_OEB_REG1))
#define reg_la0_oenb    (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_OEB_REG0))

#define reg_la1_iena    (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_IEA_REG1))
#define reg_la0_iena    (*(volatile unsigned int*) (MGMT_REGS_BASE_ADDR + LA_IEA_REG0))

// RAM PARAMETER
#define DFF1_START_ADDR 0x20000000 
#define DFF1_SIZE 2048
#define DFF2_START_ADDR 0x21000000 
#define DFF2_SIZE 1024 

#define CPU_TYPE VexRISC

enum gpio_mode {
                GPIO_MODE_MGMT_STD_INPUT_NOPULL = 0x0403,
                GPIO_MODE_MGMT_STD_INPUT_PULLDOWN =0x0c01,
                GPIO_MODE_MGMT_STD_INPUT_PULLUP=0x0801,
                GPIO_MODE_MGMT_STD_OUTPUT=0x1809,
                GPIO_MODE_MGMT_STD_BIDIRECTIONAL=0x1801,
                GPIO_MODE_MGMT_STD_ANALOG=0x000b,
                GPIO_MODE_USER_STD_INPUT_NOPULL=0x0402,
                GPIO_MODE_USER_STD_INPUT_PULLDOWN=0x0c00,
                GPIO_MODE_USER_STD_INPUT_PULLUP=0x0800,
                GPIO_MODE_USER_STD_OUTPUT=0x1808,
                GPIO_MODE_USER_STD_BIDIRECTIONAL=0x1800,
                GPIO_MODE_USER_STD_OUT_MONITORED=0x1802,
                GPIO_MODE_USER_STD_ANALOG=0x000a};