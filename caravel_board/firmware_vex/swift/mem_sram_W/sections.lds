MEMORY
{
    FLASH (rx)      : ORIGIN = 0x00000000, LENGTH = 4M
    RAM (xrw)       : ORIGIN = 0x20000000, LENGTH = 2K
    DFF (xrw)       : ORIGIN = 0x21000000, LENGTH = 1K
    USER_RAM (xrw)   : ORIGIN = 0x41000000, LENGTH = 2K
}

ENTRY(Reset_Handler)

SECTIONS {
    /* The program code and other data goes into FLASH */
    .text :
    {
        . = ALIGN(4);
        *(.isr_vector*)
        . = ALIGN(4);
        . = 0x400;
        *(.text)           /* .text sections (code) */
        *(.text*)          /* .text* sections (code) */
        . = ALIGN(256);
        *(.rodata)         /* .rodata sections (constants, strings, etc.) */
        *(.rodata*)        /* .rodata* sections (constants, strings, etc.) */
        *(.srodata)        /* .rodata sections (constants, strings, etc.) */
        *(.srodata*)       /* .rodata* sections (constants, strings, etc.) */
        . = ALIGN(4);
        _etext = .;        /* define a global symbol at end of code */
        _sidata = _etext; /* This is used by the startup in order to initialize the .data section */
    } >FLASH


    /* This is the initialized data section
    The program executes knowing that the data is in the DFF
    but the loader puts the initial values in the FLASH (inidata).
    It is one task of the startup to copy the initial values from FLASH to DFF. */
    .data : AT ( _etext )
    {
        . = ALIGN(4);
        _sdata = .;        /* create a global symbol at data start; used by startup code in order to initialise the .data section in DFF */
        _ram_start = .;    /* create a global symbol at ram start for garbage collector */
        . = ALIGN(4);
        *(.data)           /* .data sections */
        *(.data*)          /* .data* sections */
        *(.sdata)           /* .sdata sections */
        *(.sdata*)          /* .sdata* sections */
        . = ALIGN(4);
        _edata = .;        /* define a global symbol at data end; used by startup code in order to initialise the .data section in DFF */
    } >DFF

    /* Uninitialized data section */
    .bss :
    {
        . = ALIGN(4);
        _sbss = .;         /* define a global symbol at bss start; used by startup code */
        *(.bss)
        *(.bss*)
        *(.sbss)
        *(.sbss*)
        *(COMMON)

        . = ALIGN(4);
        _ebss = .;         /* define a global symbol at bss end; used by startup code */
    } >DFF

    /* this is to define the start of the heap, and make sure we have a minimum size */
    .heap :
    {
        . = ALIGN(4);
        _heap_start = .;    /* define a global symbol at heap start */
    } >DFF
    .stack_dummy (COPY):
    {
        *(.stack*)
    } >DFF
    __StackTop = ORIGIN(DFF) + LENGTH(DFF);
    /* __StackTop = ORIGIN(DFF) + 0x1000; */
    __StackLimit = __StackTop - SIZEOF(.stack_dummy);
}
