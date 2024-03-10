# TODO change path for every machine
TOOLCHAIN_PATH=/home/marwan/Downloads/riscv/bin/
#TOOLCHAIN_PATH=/home/rady/riscv64-unknown-elf-gcc-8.3.0-2020.04.1-x86_64-linux-ubuntu14/bin/


TOOLCHAIN_PREFIX=riscv64
PATTERN = $(TESTNAME)
 

hex:  ${PATTERN:=.hex}

$(info generating hex for [${TESTNAME}])

# ../../gpio_config/gpio_config_data.c: ../../gpio_config/gpio_config_def.py
# 	cd ../../gpio_config; python3 ../../gpio_config/gpio_config_builder.py

SOURCE_FILES = ../../common/crt0_vex.S ../../common/isr.c
LINKER_SCRIPT ?= ../../common/sections.lds
$(TESTNAME).elf: $(TESTNAME).c  $(LINKER_SCRIPT) $(SOURCE_FILES)
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-gcc -I../../common/ -O0 -mabi=ilp32 -march=rv32i -D__vexriscv__ -Wl,-Bstatic,-T,$(LINKER_SCRIPT),--strip-debug -ffreestanding -nostdlib -o $@ $(SOURCE_FILES) ../../common/gpio_program.c $<

	${TOOLCHAIN_PATH}$(TOOLCHAIN_PREFIX)-unknown-elf-objdump -s  $(TESTNAME).elf > $(TESTNAME).lst

$(TESTNAME).hex: $(TESTNAME).elf
	$(TOOLCHAIN_PATH)riscv64-unknown-elf-objcopy -O verilog $< $@
	sed -ie 's/@10/@00/g' $@
	
%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-objcopy -O binary $< $@

client: client.c
	gcc client.c -o client

flash: $(TESTNAME).hex
	python3 ../util/caravel_hkflash.py $(TESTNAME).hex
	python3 ../util/caravel_hkstop.py

flash2: $(TESTNAME).hex
	python3 ../util/caravel_flash.py $(TESTNAME).hex

# ---- Clean ----

clean:
	rm -f *.elf *.hex *.bin *.vvp *.vcd *.hexe *.lst *.hexe *.lst

.PHONY: clean hex all flash