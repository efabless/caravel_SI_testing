#ifndef CAN_H_
#define CAN_H_

//#include <sys/mman.h>
#include <stdint.h>

#define CTU_CAN_FD_BASE                 0x30000000
#define CTU_CAN_FD_DEVICE_ID            0xCAFD

#define BIT(nr) (1UL << (nr))

#define CTU_CAN_FD_DEVICE_ID_OFFSET      0x0
#define CTU_CAN_FD_VERSION_OFFSET        0x2
#define CTU_CAN_FD_MODE_OFFSET           0x4
#define CTU_CAN_FD_SETTINGS_OFFSET       0x6
#define CTU_CAN_FD_INT_STAT_OFFSET       0x10
#define CTU_CAN_FD_INT_ENA_SET_OFFSET    0x14
#define CTU_CAN_FD_INT_ENA_CLR_OFFSET    0x18
#define CTU_CAN_FD_INT_MASK_SET_OFFSET   0x1C
#define CTU_CAN_FD_INT_MASK_CLR_OFFSET   0x20
#define CTU_CAN_FD_BTR_OFFSET            0x24
#define CTU_CAN_FD_BTR_FD_OFFSET         0x28
#define CTU_CAN_FD_RX_DATA_OFFSET        0x6C
#define CTU_CAN_FD_RX_STATUS_OFFSET      0x68
#define CTU_CAN_FD_TRV_DELAY_OFFSET      0x80
#define CTU_CAN_FD_FAULT_STATUS_OFFSET   0x2E
#define CTU_CAN_FD_TXT_COMMAND_OFFSET    0x74
#define CTU_CAN_FD_TXT_BUFFER_1_OFFSET   0x100

#define CTU_CAN_FD_RX_STATUS_RXE_BIT     0
#define CTU_CAN_FD_MODE_RST_BIT          0
#define CTU_CAN_FD_MODE_BMM_BIT          1
#define CTU_CAN_FD_MODE_STM_BIT          2
#define CTU_CAN_FD_MODE_FDE_BIT          4
#define CTU_CAN_FD_STATUS_ENA_BIT        6
#define CTU_CAN_FD_FAULT_STATUS_ERA_BIT  0
#define CTU_CAN_FD_SETTINGS_ILBP_BIT     5

#define CTU_CAN_FD_INT_STAT_RXI_BIT      0
#define CTU_CAN_FD_INT_STAT_TXI_BIT      1
#define CTU_CAN_FD_INT_STAT_EWLI_BIT     2
#define CTU_CAN_FD_INT_STAT_DOI_BIT      3
#define CTU_CAN_FD_INT_STAT_FCSI_BIT     4
#define CTU_CAN_FD_INT_STAT_ALI_BIT      5
#define CTU_CAN_FD_INT_STAT_BEI_BIT      6
#define CTU_CAN_FD_INT_STAT_OFI_BIT      7
#define CTU_CAN_FD_INT_STAT_RXFI_BIT     8
#define CTU_CAN_FD_INT_STAT_BSI_BIT      9
#define CTU_CAN_FD_INT_STAT_RBNEI_BIT    10
#define CTU_CAN_FD_INT_STAT_TXBHCI_BIT   11

#define CTU_CAN_FD_BTR_VAL               0x08233FEF  // 125kbit/s
#define CTU_CAN_FD_BTR_FD_VAL            0x0808A387  // 500kbit/s
#define CTU_CAN_FD_TRV_DELAY_VAL         0x01000000

/*
inline void ctucan_write_32(uint32_t offset, uint32_t data);
inline void ctucan_write_16(uint32_t offset, uint16_t data);
inline uint32_t ctucan_read_32(uint32_t offset);
inline uint16_t ctucan_read_16(uint32_t offset);
inline void ctucan_set_bit_32(uint32_t offset, uint32_t bit, uint32_t val);
inline void ctucan_set_bit_16(uint32_t offset, uint32_t bit, uint32_t val);
inline uint32_t ctucan_get_bit_32(uint32_t offset, int bit);
inline uint32_t ctucan_get_bit_16(uint32_t offset, int bit);
void ctucan_reset();
void ctucan_configure();
int ctucan_disable();
int ctucan_enable();
int ctucan_s_rx_empty();
int ctucan_is_initialized();
*/

#endif /* CAN_H_ */
