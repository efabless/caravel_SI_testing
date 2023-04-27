
TOOLCHAIN_PATH=/home/marwan/Downloads/riscv/bin/
#TOOLCHAIN_PATH=/opt/riscv32imc/bin/
# TOOLCHAIN_PATH=/ef/apps/bin/

# Set the prefix for `riscvXX-unknown-elf-*`
# On installations using `multilib`, this will be `riscv64` even for compiling to 32-bit targets
TOOLCHAIN_PREFIX=riscv64
#TOOLCHAIN_PREFIX=riscv32

# ---- Test patterns for project raven ----

.SUFFIXES:

PATTERN = mem_dff2_halfW

hex:  ${PATTERN:=.hex}

../../gpio_config/gpio_config_data.c: ../../gpio_config/gpio_config_def.py
	cd ../../gpio_config; python3 ../../gpio_config/gpio_config_builder.py

%.elf: %.c ../../sections.lds ../../crt0_vex.S
	$(TOOLCHAIN_PATH)riscv64-unknown-elf-gcc -I../../ -I../../generated/ -I../common/ -O0 -mabi=ilp32 -march=rv32i -D__vexriscv__ -Wl,-Bstatic,-T,../../sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ ../../crt0_vex.S ../../isr.c ../../gpio_program.c $<

	${TOOLCHAIN_PATH}riscv64-unknown-elf-objdump -s  mem_dff2_halfW.elf > mem_dff2_halfW.lst

%.hex: %.elf
	$(TOOLCHAIN_PATH)riscv64-unknown-elf-objcopy -O verilog $< $@
	sed -ie 's/@10/@00/g' $@
	
%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-objcopy -O binary $< $@

client: client.c
	gcc client.c -o client

flash: mem_dff2_halfW.hex
	python3 ../util/caravel_hkflash.py mem_dff2_halfW.hex
	python3 ../util/caravel_hkstop.py

flash2: mem_dff2_halfW.hex
	python3 ../util/caravel_flash.py mem_dff2_halfW.hex

# ---- Clean ----

clean:
	rm -f *.elf *.hex *.bin *.vvp *.vcd *.hexe *.lst *.hexe *.lst

.PHONY: clean hex all flash




