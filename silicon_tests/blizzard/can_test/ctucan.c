#include "ctucan.h"

#define INLINE 

INLINE void ctucan_write_32(uint32_t offset, uint32_t data)
{
	char *base = (char *) CTU_CAN_FD_BASE;
	volatile uint32_t *reg = (volatile uint32_t *)(base + offset);
	*reg = data;
}

INLINE void ctucan_write_16(uint32_t offset, uint16_t data)
{
	char *base = (char *) CTU_CAN_FD_BASE;
	volatile uint16_t *reg = (volatile uint16_t *)(base + offset);
	*reg = data;
}

/* read functions */

INLINE uint32_t ctucan_read_32(uint32_t offset)
{
	char *base = (char *) CTU_CAN_FD_BASE;
	volatile uint32_t *reg = (volatile uint32_t *)(base + offset);
	return *reg;
}

INLINE uint16_t ctucan_read_16(uint32_t offset)
{
	char *base = (char *) CTU_CAN_FD_BASE;
	volatile uint16_t *reg = (volatile uint16_t *)(base + offset);
	return *reg;
}

/* bit access */

INLINE void ctucan_set_bit_32(uint32_t offset, uint32_t bit, uint32_t val)
{
	uint32_t reg_val = ctucan_read_32(offset);
	reg_val = (reg_val & ~BIT(bit)) | ((!!val) << bit);
	ctucan_write_32(offset, reg_val);
}

INLINE void ctucan_set_bit_16(uint32_t offset, uint32_t bit, uint32_t val)
{
	uint16_t reg_val = ctucan_read_16(offset);
	reg_val = (reg_val & ~BIT(bit)) | ((!!val) << bit);
	ctucan_write_16(offset, reg_val);
}

INLINE uint32_t ctucan_get_bit_32(uint32_t offset, int bit)
{
	uint32_t reg_value = ctucan_read_32(offset);
	return !!(reg_value & BIT(bit));
}

INLINE uint32_t ctucan_get_bit_16(uint32_t offset, int bit)
{
	uint16_t reg_value = ctucan_read_16(offset);
	return !!(reg_value & BIT(bit));
}

void ctucan_reset()
{
	ctucan_set_bit_16(CTU_CAN_FD_MODE_OFFSET, CTU_CAN_FD_MODE_RST_BIT, 1);
}

void ctucan_configure()
{
	ctucan_write_32(CTU_CAN_FD_BTR_OFFSET, CTU_CAN_FD_BTR_VAL);
	ctucan_write_32(CTU_CAN_FD_BTR_FD_OFFSET, CTU_CAN_FD_BTR_FD_VAL);
	ctucan_write_32(CTU_CAN_FD_TRV_DELAY_OFFSET, CTU_CAN_FD_TRV_DELAY_VAL);
}

void ctucan_interrupt_enable(int irq_bit)
{
	ctucan_set_bit_16(CTU_CAN_FD_INT_ENA_SET_OFFSET, irq_bit, 1);
}

void ctucan_interrupt_unmask(int irq_bit)
{
	ctucan_set_bit_16(CTU_CAN_FD_INT_MASK_CLR_OFFSET, irq_bit, 1);
}

void ctucan_interrupt_clean(int irq_bit)
{
	ctucan_set_bit_16(CTU_CAN_FD_INT_ENA_CLR_OFFSET, irq_bit, 1);
}

void ctucan_interrupts_mask_all()
{
	uint16_t reg_val = ctucan_read_16(CTU_CAN_FD_INT_MASK_SET_OFFSET);
	uint16_t mask = 0x0FFF;
	reg_val = (reg_val & ~mask) | mask;
	ctucan_write_16(CTU_CAN_FD_INT_MASK_SET_OFFSET, reg_val);
}

void ctucan_configure_interrupts()
{
	ctucan_interrupts_mask_all();

	ctucan_interrupt_enable(CTU_CAN_FD_INT_STAT_RXI_BIT);
	ctucan_interrupt_enable(CTU_CAN_FD_INT_STAT_TXI_BIT);
	ctucan_interrupt_unmask(CTU_CAN_FD_INT_STAT_RXI_BIT);
	ctucan_interrupt_unmask(CTU_CAN_FD_INT_STAT_TXI_BIT);
}

void ctucan_enable_selfack()
{
	ctucan_set_bit_16(CTU_CAN_FD_MODE_OFFSET, CTU_CAN_FD_MODE_STM_BIT, 1);
}

void ctucan_enable_loop()
{
	ctucan_set_bit_16(CTU_CAN_FD_SETTINGS_OFFSET, CTU_CAN_FD_SETTINGS_ILBP_BIT, 1);
}

int ctucan_disable()
{
	ctucan_set_bit_16(CTU_CAN_FD_SETTINGS_OFFSET, CTU_CAN_FD_STATUS_ENA_BIT, 0);
	return (ctucan_get_bit_16(CTU_CAN_FD_SETTINGS_OFFSET, CTU_CAN_FD_STATUS_ENA_BIT) == 0) ? 0 : -1;
}

int ctucan_enable()
{
	ctucan_set_bit_16(CTU_CAN_FD_SETTINGS_OFFSET, CTU_CAN_FD_STATUS_ENA_BIT, 1);
	return (ctucan_get_bit_16(CTU_CAN_FD_SETTINGS_OFFSET, CTU_CAN_FD_STATUS_ENA_BIT) == 1) ? 0 : -1;
}

int ctucan_is_rx_empty()
{
	return ctucan_get_bit_16(CTU_CAN_FD_RX_STATUS_OFFSET, CTU_CAN_FD_RX_STATUS_RXE_BIT) == 1;
}

int ctucan_is_initialized()
{
	return ctucan_get_bit_16(CTU_CAN_FD_FAULT_STATUS_OFFSET, CTU_CAN_FD_FAULT_STATUS_ERA_BIT) == 1;
}
