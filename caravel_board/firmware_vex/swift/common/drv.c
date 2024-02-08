void mgmt_enable(unsigned int dev) { *MGMT_CTRL = *MGMT_CTRL | dev; }

char uart_getc() {
  // if(uart == 0){
  while ((*UART0_STAT & 2) == 0)
    ;
  return (*UART0_DATA);
  /*} else if(uart == 1){
      while((*UART1_STAT & 2) == 0);
      return(*UART1_DATA);
  } else return -1;*/
}

void uart_putc(char c) {
  // if(uart == 0){
  while ((*UART0_STAT & 1) != 0)
    ;
  *UART0_DATA = c;
  /*} else if(uart == 1){
      while((*UART1_STAT & 1) != 0);
      *UART1_DATA = c;
  } else return -1;*/
}

void tmr_en(int tmr) {
  if (tmr == 0)
    *TMR0_CTRL |= 0x01;
  else
    *TMR1_CTRL |= 0x01;
}

void tmr_dis(int tmr) {
  if (tmr == 0)
    *TMR0_CTRL &= 0xFE;
  else
    *TMR1_CTRL &= 0xFE;
}

// SPI
int spi_init(unsigned char cpol, unsigned char cpha, unsigned char clkdiv) {
  unsigned int cfg_value = 0;
  cfg_value |= cpol;
  cfg_value |= (cpha << 1);
  // cfg_value |=  ((unsigned int)clkdiv << 2);
  *SPI_CFG = cfg_value;
  *SPI_PRE = clkdiv;
}

unsigned int spi_status() { return *SPI_STATUS & 1; }

unsigned char spi_read() { return *SPI_DATA; }

int spi_write(unsigned char data) {
  *SPI_DATA = data;
  SET_BIT(*SPI_CTRL, SPI_GO_BIT);
  CLR_BIT(*SPI_CTRL, SPI_GO_BIT);
  while (!spi_status())
    ;
  return 0;
}

int spi_start() {
  SET_BIT(*SPI_CTRL, SPI_SS_BIT);
  return 0;
}

int spi_end() {
  CLR_BIT(*SPI_CTRL, SPI_SS_BIT);
  return 0;
}

/* i2c */
/*
int i2c_init(unsigned int pre){
    *(I2C_PRE_LO) = pre & 0xff;
    *(I2C_PRE_HI) = pre & 0xff00;
    *(I2C_CTRL) = I2C_CTRL_EN | I2C_CTRL_IEN;
}

int i2c_start(unsigned char control)
{
        *(I2C_TX) = control;
        *(I2C_CMD) = I2C_CMD_STA | I2C_CMD_WR;
        while( ((*I2C_STAT) & I2C_STAT_TIP) != 0 );

        if( ((*I2C_STAT) & I2C_STAT_RXACK)) {
            *(I2C_CMD) = I2C_CMD_STO;
            return 0;
        }
        return 1;
}
int i2c_stop(){
    *(I2C_CMD) = I2C_CMD_STO;
}

int i2c_sendByte(unsigned char b){
        *(I2C_TX) = b;
        *(I2C_CMD) = I2C_CMD_WR;
        while( (*I2C_STAT) & I2C_STAT_TIP );
        if( ((*I2C_STAT) & I2C_STAT_RXACK )){
            *(I2C_CMD) = I2C_CMD_STO;
            return 0;
        }
        return 1;
}
int i2c_readByte(){
    *(I2C_CMD) = I2C_CMD_RD;
    while( ((*I2C_STAT) & I2C_STAT_TIP) != 0 );
    return *(I2C_RX);
}
*/

void M23LC_write_byte(unsigned int addr, unsigned int data) {
  spi_start();
  spi_write(0x2);
  spi_write(addr >> 8);   // Address high byte
  spi_write(addr & 0xFF); // Address low byte
  spi_write(data);
  spi_end();
}

unsigned char M23LC_read_byte(unsigned short addr) {
  spi_start();
  spi_write(0x3);
  spi_write(addr >> 8);   // Address high byte
  spi_write(addr & 0xFF); // Address low byte
  spi_write(0);           // just write a dummy data to get the data out
  spi_end();
  return spi_read();
}

void dbg_init() {
  *DBG_IM = 0;
  *DBG_OE = 0;
  *DBG_DATA = 0;
}

void dbg_write(unsigned data) { *DBG_OE = data; }
