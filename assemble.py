from asm6502 import asm6502
import os
import re

def assemble(code_file, bin_filepath):
    code = os.system("../tools/acme -o " + bin_filepath + " -r temp.txt --symbollist temp.sym " + code_file)
    exit_status = os.WEXITSTATUS(code)
    if exit_status != 0:
        print("Assembly failed")
        exit(exit_status)

    with open("temp.sym") as file:
        lines = file.readlines()

    symbols = {}
    for line in lines:
        match = re.search("(.*)[ \t]+=[ \t]+\$([0-9a-f]+).*", line)
        if match:
            name = match.group(1).strip()
            val  = int(match.group(2), 16)
            symbols[name] = val

    return symbols
