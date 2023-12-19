#TOOLCHAIN_PATH=/opt/riscv32imc/bin/
# TOOLCHAIN_PATH=/ef/apps/bin/

# Set the prefix for `riscvXX-unknown-elf-*`
# On installations using `multilib`, this will be `riscv64` even for compiling to 32-bit targets
# TOOLCHAIN_PREFIX=riscv32

INCLUDES=-I$(shell pwd) -I../../ -I../../generated/
VOLTAGE=$(shell python3 -c "from gpio_config_def import voltage; print(voltage)")

# ---- Test patterns for project raven ----

.SUFFIXES:
TESTNAME = bitbang_o_h


include ../common/Makefile.common



