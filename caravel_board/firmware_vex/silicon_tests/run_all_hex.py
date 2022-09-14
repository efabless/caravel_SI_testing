#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os


dirs = [x[0] for x in os.walk(os.getcwd())]
for dir in dirs:
    os.chdir(dir)
    os.system(f'make clean')
    os.system(f'make hex')
    # print(os.getcwd())