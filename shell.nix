{
    pkgs ? import <nixpkgs> {},
    pkgsCross ? import <nixpkgs> {
        crossSystem = {
            config = "riscv64-none-elf";
        };
    }    
}:

pkgsCross.mkShell {
    buildInputs = [
        (pkgs.python3.withPackages(ps: with ps; [
            async-timeout
            contourpy
            cycler
            fonttools
            ifaddr
            markdown-it-py
            matplotlib
            mdurl
            numpy
            packaging
            pillow
            psutil
            pyparsing
            python-dateutil
            pyvisa
            pyvisa-py
            rich
            six
            typing-extensions
            zeroconf
        ]))
    ];
    
    TOOLCHAIN_ARCH="rv32i_zicsr";
    TOOLCHAIN_PREFIX="riscv64-none-elf";
}
