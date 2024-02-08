void putchar(char c){

    while ((reg_uart_stat &0x1) == 1); // while TX buffer full
	reg_uart_data = c;
}

void print(const char *p)
{
	while (*p)
		putchar(*(p++));
}