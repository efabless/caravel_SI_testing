.syntax unified
    .arch armv6-m
    .code 16

    .section .stack
    .align 3
    .equ    Stack_Size, 0x1000
    .global    __StackTop
    .global    __StackLimit

    .section .heap
    .align 3

    .equ    Heap_Size, 0
    .global    __HeapBase
    .global    __HeapLimit
    __HeapBase:
    .if    Heap_Size
    .space    Heap_Size
    .endif
    .size __HeapBase, . - __HeapBase
    __HeapLimit:
    .size __HeapLimit, . - __HeapLimit


    /* Vector Table */

    .section .isr_vector
    .align 2
    .global __isr_vector
    __isr_vector:
    .long   __StackTop                 /* Top of Stack                  */
    .long   Reset_Handler              /* Reset Handler                 */
    .long   NMI_Handler                /* NMI Handler                   */
    .long   HardFault_Handler          /* Hard Fault Handler            */
    .long   MemManage_Handler          /* Reserved                      */
    .long   BusFault_Handler           /* Reserved                      */
    .long   UsageFault_Handler         /* Reserved                      */
    .long   0                          /* Reserved                      */
    .long   0                          /* Reserved                      */
    .long   0                          /* Reserved                      */
    .long   0                          /* Reserved                      */
    .long   SVC_Handler                /* SVCall Handler                */
    .long   DebugMon_Handler           /* Debug Monitor Handler         */
    .long   0                          /* Reserved                      */
    .long   PendSV_Handler             /* PendSV Handler                */
    .long   SysTick_Handler            /* SysTick Handler               */

    /* External Interrupts */
    .long   0
    .long   0
    .long   0
    .long   HK_IRQ0_Handler
    .long   HK_IRQ1_Handler
    .long   HK_IRQ2_Handler
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   PORTA_Handler
    .long   TMR0_Handler
    .long   TMR1_Handler
    .long   UART0_Handler
    .long   SPI_Handler
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0
    .long   0

    .size    __isr_vector, . - __isr_vector



    /* Reset Handler */
    .text
    .thumb
    .thumb_func
    .align 2
    .global     Reset_Handler
    .type       Reset_Handler, %function
Reset_Handler:
    // Write 0x8 to 0xA0000040 to enable RAM
    ldr r0, =0xA0000040   // Load the address into r0
    ldr r1, =0x8          // Load the immediate value 0x8 into r1
    str r1, [r0]          // Store the value in r1 to the address in r0
    // Initialize core registers to avoid problems with X in simulation
    mov r1, r0
    mov r2, r0

    mov r4, r0
    mov r5, r0
    mov r6, r0
    mov r7, r0
    mov r8, r0
    mov r9, r0

    //copy data section
    ldr r0, =_sidata
    ldr r1, =_sdata
    ldr r2, =_edata
    cmp r1, r2
    bhs end_init
    loop_init:
    ldr r3, [r0]
    str r3, [r1]
    adds r0, #4
    adds r1, #4
    cmp r1, r2
    blo loop_init
    end_init:

    bl main
    b .

    .thumb
    .thumb_func
    .align 2
    .global     Hard_Fault_Handler
    .type       Hard_Fault_Handler, %function
Hard_Fault_Handler:
    b .

    .pool
    .size Reset_Handler, . - Reset_Handler

    /*   Macro to define default handlers. Default handler
    *    will be weak symbol and just dead loops. They can be
    *    overwritten by other handlers */
    .macro    def_default_handler    handler_name
    .align 1
    .thumb_func
    .weak    \handler_name
    .type    \handler_name, %function
    \handler_name :
        b .
    .size    \handler_name, . - \handler_name
    .endm

    //System Exception Handlers

    def_default_handler    NMI_Handler
    def_default_handler    HardFault_Handler
    def_default_handler    MemManage_Handler
    def_default_handler    BusFault_Handler
    def_default_handler    UsageFault_Handler
    def_default_handler    SVC_Handler
    def_default_handler    DebugMon_Handler
    def_default_handler    PendSV_Handler
    def_default_handler    SysTick_Handler

    //IRQ Handlers

    def_default_handler     HK_IRQ0_Handler
    def_default_handler     HK_IRQ1_Handler
    def_default_handler     HK_IRQ2_Handler

    def_default_handler     PORTA_Handler
    def_default_handler     PORTB_Handler
    def_default_handler     TMR0_Handler
    def_default_handler     TMR1_Handler
    def_default_handler     UART0_Handler
    def_default_handler     UART1_Handler
    def_default_handler     SPI_Handler
    def_default_handler     I2C_Handler  

    .end
