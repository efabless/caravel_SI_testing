MEMORY {
	vexriscv_debug : ORIGIN = 0xf00f0000, LENGTH = 0x00000100
	dff : ORIGIN = 0x00000000, LENGTH = 0x00000400
	sram : ORIGIN = 0x01000000, LENGTH = 0x00000800
	flash : ORIGIN = 0x10000000, LENGTH = 0x01000000
	mprj : ORIGIN = 0x30000000, LENGTH = 0x00100000
	hk : ORIGIN = 0x26000000, LENGTH = 0x00100000
	csr : ORIGIN = 0xf0000000, LENGTH = 0x00010000
}
