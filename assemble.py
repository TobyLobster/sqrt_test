import os
import re

def assemble(code_file, bin_filepath):
    code = os.system("${ACME=acme} -o " + bin_filepath + " -r build/temp.txt --symbollist build/temp.sym " + code_file)
    exit_status = os.WEXITSTATUS(code)
    if exit_status != 0:
        print("Assembly failed")
        exit(exit_status)

    with open("build/temp.sym") as file:
        lines = file.readlines()

    symbols = {}
    for line in lines:
        match = re.search("(.*)[ \t]+=[ \t]+\$([0-9a-f]+).*", line)
        if match:
            name = match.group(1).strip()
            val  = int(match.group(2), 16)
            symbols[name] = val

    return symbols
