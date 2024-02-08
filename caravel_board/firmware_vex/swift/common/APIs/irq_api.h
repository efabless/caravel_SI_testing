
/**
 \file
*/
#ifndef IRQ_API_C_HEADER_FILE
#define IRQ_API_C_HEADER_FILE
// IRQ 
#ifndef DOXYGEN_SHOULD_SKIP_THIS
unsigned int flag;
void HK_IRQ0_Handler(void){flag = 1;}
void HK_IRQ1_Handler(void){flag = 1;}
void HK_IRQ2_Handler(void){flag = 1;}
void TMR0_Handler(void){flag = 1;clear_TMR0_Handler();}
void UART0_Handler(void){flag = 1;clear_UART0_Handler();}
void clear_TMR0_Handler(){
reg_timer0_irq =1;
}
void clear_UART0_Handler(){
reg_uart_isc =0x3;
}
char IRQ_getFlag(){
    dummyDelay(1);
    return flag;
}

void IRQ_clearFlag(){
    flag=0;
}
#endif /* DOXYGEN_SHOULD_SKIP_THIS */
/**
 * Enable or disable external1 interrupt GPIO[7] 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableExternal1(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(HK_IRQ1);
        __enable_irq();
    }else{
        NVIC_DisableIRQ(HK_IRQ1);
        __enable_irq();
    }
}

/**
 * Enable or disable external2 interrupt GPIO[12] 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableExternal2(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(HK_IRQ2);
        __enable_irq();
    }else{
        NVIC_DisableIRQ(HK_IRQ2);
        __enable_irq();
    }    
}
/**
 * Enable or disable user0 interrupt 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableUser0(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(HK_IRQ2);
        __enable_irq();
    }else{
        NVIC_DisableIRQ(HK_IRQ2);
        __enable_irq();
    }    
}
/**
 * Enable or disable user1 interrupt 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableUser1(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(HK_IRQ2);
        __enable_irq();
    }else{
        NVIC_DisableIRQ(HK_IRQ2);
        __enable_irq();
    }    
}

/**
 * Enable or disable user1 interrupt 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableUser2(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(HK_IRQ2);
        __enable_irq();
    }else{
        NVIC_DisableIRQ(HK_IRQ2);
        __enable_irq();
    }    
}
/**
 * Enable or disable timer0 interrupt 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableTimer(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(TMR0_IRQn);
        reg_timer0_config = reg_timer0_config | 0x8; // enable irq
        __enable_irq();
    }else{
        NVIC_DisableIRQ(TMR0_IRQn);
        reg_timer0_config = reg_timer0_config | 0x8; // enable irq
        __enable_irq();
    }
}
/**
 * Enable or disable UART tx interrupt 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableUartTx(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(UART0_IRQn);
        reg_uart_ctrl = reg_uart_ctrl | 0x5; // enable irq TX 
        __enable_irq();
    }else{
        NVIC_DisableIRQ(UART0_IRQn);
        reg_uart_ctrl = reg_uart_ctrl | 0x5; // enable irq TX 
        __enable_irq();
    }
}
/**
 * Enable or disable UART rx interrupt 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_enableUartRx(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(UART0_IRQn);
        reg_uart_ctrl = reg_uart_ctrl | 0xA; // enable irq rx 
        __enable_irq();
    }else{
        reg_uart_ctrl = reg_uart_ctrl & 0xF7; // enable irq rx 
        __enable_irq();
    }
}
/**
 * Enable or disable SPI interrupt 
 * 
 *  
 * @param is_enable when 1 (true) interrupt is active and firmware would detect if happened, 0 (false) interrupt is disabled and firmware would not detect if happened
 */
void IRQ_hkSpi(int is_enable){
    if (is_enable){
        NVIC_EnableIRQ(HK_IRQ0);
        __enable_irq();
    }else{
        NVIC_DisableIRQ(HK_IRQ0);
        __enable_irq();
    }
}

#endif // IRQ_API_C_HEADER_FILE
