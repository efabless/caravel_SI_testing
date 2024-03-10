TOOLCHAIN_PATH=/home/marwan/Downloads/riscv/bin/
# TOOLCHAIN_PATH=/usr/local/bin/
#TOOLCHAIN_PATH=/opt/riscv32imc/bin/
# TOOLCHAIN_PATH=/ef/apps/bin/

# Set the prefix for `riscvXX-unknown-elf-*`
# On installations using `multilib`, this will be `riscv64` even for compiling to 32-bit targets
TOOLCHAIN_PREFIX=riscv64
#TOOLCHAIN_PREFIX=riscv32

INCLUDES=-I$(shell pwd) -I../../ -I../../generated/
VOLTAGE=$(shell python3 -c "from gpio_config_def import voltage; print(voltage)")

# ---- Test patterns for project raven ----

.SUFFIXES:

PATTERN = timer0_periodic

hex:  ${PATTERN:=.hex}

#../../gpio_config/gpio_config_data.c: ../../gpio_config/gpio_config_def.py
#	cd ../../gpio_config; python3 ../../gpio_config/gpio_config_builder.py

# gpio_config_data.c: gpio_config_def.py gpio_config_io.py
# 	python3 ../../gpio_config/gpio_config_builder.py

#%.elf: %.c ../../sections.lds ../../crt0_vex.S ../../gpio_config/gpio_config_data.c
#%.elf: %.c ../../sections.lds ../../crt0_vex.S gpio_config_data.c
#	$(TOOLCHAIN_PATH)riscv64-unknown-elf-gcc -I../../ -I../../generated/ -I../common/ -O0 -mabi=ilp32 -march=rv32i -D__vexriscv__ -Wl,-Bstatic,-T,../../sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ ../../crt0_vex.S ../../isr.c ../../gpio_program.c $<
#	${TOOLCHAIN_PATH}riscv64-unknown-elf-objdump -s  uart.elf > uart.lst

%.elf: %.c ../../sections.lds ../../crt0_vex.S
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-gcc $(INCLUDES) -O0 -mabi=ilp32 -march=rv32i -D__vexriscv__ -Wl,-Bstatic,-T,../../sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ ../../crt0_vex.S ../../isr.c $<
	${TOOLCHAIN_PATH}$(TOOLCHAIN_PREFIX)-unknown-elf-objdump -D $@ > $*.lst

%.hex: %.elf
	$(TOOLCHAIN_PATH)riscv64-unknown-elf-objcopy -O verilog $< $@
	sed -ie 's/@10/@00/g' $@
	
%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-objcopy -O binary $< $@

client: client.c
	gcc client.c -o client

flash: timer0_periodic.hex
	python3 ../util/caravel_hkflash.py timer0_periodic.hex
	python3 ../util/caravel_hkstop.py

flash2: timer0_periodic.hex
	python3 ../util/caravel_flash.py timer0_periodic.hex

# ---- Clean ----

clean:
	rm -f *.elf *.hex *.bin *.vvp *.vcd *.hexe *.lst *.hexe *.lst gpio_config_data.c

.PHONY: clean hex all flash



