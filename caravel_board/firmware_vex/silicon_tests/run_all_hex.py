#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cgi import test
import os

def change_ram(str,new_str,file_path):
    # Read in the file
    with open(file_path, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(str, new_str)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)

dirs = [x[0] for x in os.walk(os.getcwd())]
del dirs[0]
file_path =f'{os.getcwd()}/../sections.lds'

change_ram(" > sram"," > dff",file_path)
# print(f'{os.getcwd()}/../sections.lds')
for dir in dirs:
    os.chdir(dir)
    testname = os.path.basename(dir)
    print(testname)
    if testname in ["common", "mem_stress_dff"]:
        continue
    os.system(f'make clean')
    os.system(f'make hex')
    os.rename(f'{testname}.hex',f'{testname}_dff.hex')

change_ram(" > dff"," > sram",file_path)
for dir in dirs:
    os.chdir(dir)
    testname = os.path.basename(dir)
    print(testname)
    if testname in ["common", "mem_stress_sram"]: 
        continue
    os.system(f'make hex')
    os.rename(f'{testname}.hex',f'{testname}_sram.hex')


