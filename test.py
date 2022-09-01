import py65
import assemble
import os
from py65.monitor import Monitor
from io import StringIO
import time
import math
from pathlib import Path

# py65mon source is here: https://github.com/mnaberez/py65/blob/master/py65/monitor.py


tasks = []

def add_task(name, file, start_symbol, pre, post, expect):
    tasks.append((name, file, start_symbol, pre, post, expect))

def run_tasks():
    spreadsheet = []
    file_sizes = []
    task_index = 0
    for (name, file, start_symbol, pre, post, expect) in tasks:
        spreadsheet.append({})
        file_sizes.append({})
        code = file
        print("Running task " + code)
        (file_size, cycles) = run_task(name, code, start_symbol, pre, post, expect)
        file_sizes[task_index] = (name, file_size)
        print("Task " + code + " completed")
        for key in cycles:
            spreadsheet[task_index][key] = cycles[key]
        task_index += 1
    return (file_sizes, spreadsheet)

def set_memory(mon, addr, val):
    mon._mpu.memory[addr] = val
    #mon.do_fill(str(addr) + " " + '{:02x}'.format(val & 255))

def set_register(mon, register, val):
    if val < 256:
        mon.do_registers(register + "=" + '{:02x}'.format(val))
    else:
        mon.do_registers(register + "=" + '{:04x}'.format(val))

def get_memory(mon, addr):
    return mon._mpu.memory[addr]

def get_register(mon, register):
    if register == "a":
        return mon._mpu.a
    if register == "x":
        return mon._mpu.x
    if register == "y":
        return mon._mpu.y
    return -1

def run_task(name, codefile, start_symbol, pre, post, expect):
    symbols = assemble.assemble(codefile, "build/TESTME")

    load = symbols.get('_start') or symbols[start_symbol]
    loadHexString = '{:04x}'.format(load)
    start = symbols[start_symbol]
    startHexString = '{:04x}'.format(start)
    print ("load %s start %s" % (loadHexString,startHexString))
    mon = Monitor()
    mon.do_load("build/TESTME $" + loadHexString)

    file_size = os.path.getsize("build/TESTME")

    start_time = time.perf_counter()
    cycles = {}
    for v in range(0,65536):
        pre(mon, symbols, v)

        # HACK - make sure when we execute the final RTS, we return to $ffff, where a
        # BRK instruction ends the test. Hopefully there was no code there!
        set_memory(mon, 0xffff, 0)      # BRK instruction
        set_memory(mon, 0x1fe, 0xfe)    # Put $fffe on the stack so RTS returns to memory location $FFFF
        set_memory(mon, 0x1ff, 0xff)
        mon._mpu.sp = 253               # Set stack pointer

        oldCycles = mon._mpu.processorCycles

        # DEBUG!
        #set_register(mon, "pc", start)
        #for i in range(0,200):
        #    mon.do_step("")
        #    mon.onecmd("registers")

        mon.do_goto(startHexString)
        result = post(mon, symbols, v)

        if (v % 10000) == 0:
            print("progress " + str(v))

        if expect:
            expected = expect(v)
            if result != expected:
                print("FAILED. For value " + str(v) + " expected result " + str(expected) + " but got " + str(result))

        cycles[v] = mon._mpu.processorCycles - oldCycles
    end_time = time.perf_counter()
    print("time: " + str(end_time - start_time))

    ave_cycles = 0
    best_cycles = float('inf')
    worst_cycles = 0
    for v in cycles:
        worst_cycles = max(worst_cycles, cycles[v])
        best_cycles = min(best_cycles, cycles[v])
        ave_cycles += cycles[v]
    ave_cycles = ave_cycles / 65536
    print("best cycles: " + str(best_cycles))
    print("worst cycles: " + str(worst_cycles))
    print("average cycles: " + str(ave_cycles))

    return (file_size, cycles)

def task1_pre(mon, symbols, v):
    set_memory(mon, symbols["MLO"], v & 255)
    set_memory(mon, symbols["MHI"], v // 256)

def task1_post(mon, symbols, v):
    result = mon._mpu.y
    return result

def task2_pre(mon, symbols, v):
    set_memory(mon, symbols["Numberl"], v & 255)
    set_memory(mon, symbols["Numberh"], v // 256)

def task2_post(mon, symbols, v):
    result = get_memory(mon, symbols["Root"])
    return result

def expect(v):
    return int(math.sqrt(v))

def task3_pre(mon, symbols, v):
    mon._mpu.a = v & 255
    mon._mpu.x = v // 256

def task3_post(mon, symbols, v):
    result = mon._mpu.y
    return result

def task4_pre(mon, symbols, v):
    set_memory(mon, symbols["ARG"], v & 255)
    set_memory(mon, symbols["ARG"] + 1, v // 256)

def task4_post(mon, symbols, v):
    result = get_memory(mon, symbols["ODD"])
    return result

def task5_pre(mon, symbols, v):
    set_memory(mon, symbols["ARGLO"], v & 255)
    set_memory(mon, symbols["ARGHI"], v // 256)

def task5_post(mon, symbols, v):
    result = get_memory(mon, symbols["ROOT"])
    return result

def task6_pre(mon, symbols, v):
    set_memory(mon, symbols["Q"], v & 255)
    set_memory(mon, symbols["R"], v // 256)

def task6_post(mon, symbols, v):
    result = get_memory(mon, symbols["Q"])
    return result

def task7_pre(mon, symbols, v):
    set_memory(mon, symbols["NUML"], v & 255)
    set_memory(mon, symbols["NUMH"], v // 256)

def task7_post(mon, symbols, v):
    result = get_memory(mon, symbols["ROOT"])
    return result

def task8_pre(mon, symbols, v):
    set_memory(mon, symbols["num"], v & 255)
    set_memory(mon, symbols["num"]+1, v // 256)

def task8_post(mon, symbols, v):
    return mon._mpu.x

def task9_pre(mon, symbols, v):
    mon._mpu.a = v & 255
    mon._mpu.x = v // 256

def task9_post(mon, symbols, v):
    result = mon._mpu.y
    return result

def task10_pre(mon, symbols, v):
    set_memory(mon, symbols["MLO"], v & 255)
    set_memory(mon, symbols["MHI"], v // 256)

def task10_post(mon, symbols, v):
    result = mon._mpu.y
    return result

def task11_pre(mon, symbols, v):
    set_memory(mon, symbols["val"], v & 255)
    set_memory(mon, symbols["val"]+1, v // 256)

def task11_post(mon, symbols, v):
    result = mon._mpu.x
    return result

def task12_pre(mon, symbols, v):
    set_memory(mon, symbols["_a"], v & 255)
    set_memory(mon, symbols["_a"]+1, v // 256)

def task12_post(mon, symbols, v):
    result = get_memory(mon, symbols["_z"])
    return result

def task13_pre(mon, symbols, v):
    set_memory(mon, symbols["in_lo"], v & 255)
    mon._mpu.x = v // 256

def task13_post(mon, symbols, v):
    result = mon._mpu.a
    return result

def task14_pre(mon, symbols, v):
    set_memory(mon, symbols["in_lo"], v & 255)
    mon._mpu.x = v // 256

def task14_post(mon, symbols, v):
    result = mon._mpu.a
    return result

def task15_pre(mon, symbols, v):
    mon._mpu.a = v & 255
    mon._mpu.x = v // 256

def task15_post(mon, symbols, v):
    result = mon._mpu.a
    return result

def task16_pre(mon, symbols, v):
    set_memory(mon, symbols["byte"], v & 255)
    set_memory(mon, symbols["byte"] + 1, v // 256)

def task16_post(mon, symbols, v):
    result = mon._mpu.y
    return result

def task17_pre(mon, symbols, v):
    set_memory(mon, symbols["input"], v & 255)
    set_memory(mon, symbols["input"] + 1, v // 256)

def task17_post(mon, symbols, v):
    result = mon._mpu.y
    return result

def task18_pre(mon, symbols, v):
    set_memory(mon, symbols["input"], v & 255)
    set_memory(mon, symbols["input"] + 1, v // 256)

def task18_post(mon, symbols, v):
    result = mon._mpu.a
    return result

# 1. Add tasks
add_task("sqrt1 (https://codebase64.org/doku.php?id=base:fast_sqrt)", "sqrt/sqrt1.a", "start", task1_pre, task1_post, expect)
add_task("sqrt2 (http://www.6502.org/source/integers/root.htm)",      "sqrt/sqrt2.a", "SqRoot", task2_pre, task2_post, expect)
add_task("sqrt3 (http://www.txbobsc.com/aal/1986/aal8611.html#a1)",   "sqrt/sqrt3.a", "SQRT", task3_pre, task3_post, expect)
#too slow!
add_task("sqrt4 (http://www.txbobsc.com/aal/1985/aal8506.html#a2)",   "sqrt/sqrt4.a", "SQRT", task4_pre, task4_post, expect)
add_task("sqrt5 (http://www.txbobsc.com/aal/1986/aal8609.html#a8)",   "sqrt/sqrt5.a", "SQR3", task5_pre, task5_post, expect)
add_task("sqrt6 (https://www.bbcelite.com/master/main/subroutine/ll5.html)", "sqrt/sqrt6.a", "LL5", task6_pre, task6_post, expect)
add_task("sqrt7 (http://6502org.wikidot.com/software-math-sqrt)",     "sqrt/sqrt7.a", "start", task7_pre, task7_post, expect)
#too slow!
add_task("sqrt8 (https://mdfs.net/Info/Comp/6502/ProgTips/SqRoot)",     "sqrt/sqrt8.a", "sqr", task8_pre, task8_post, expect)
add_task("sqrt9 (https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt9.a)", "sqrt/sqrt9.a", "sqrt16", task9_pre, task9_post, expect)
add_task("sqrt10 (https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt10.a)", "sqrt/sqrt10.a", "start", task10_pre, task10_post, expect)
add_task("sqrt11 (http://forum.6502.org/viewtopic.php?p=90611#p90611)", "sqrt/sqrt11.a", "sqrt", task11_pre, task11_post, expect)
add_task("sqrt12 (https://gitlab.riscosopen.org/RiscOS/Sources/Apps/Diversions/Meteors/-/blob/master/Srce6502/MetSrc2#L961)", "sqrt/sqrt12.a", "squareroot", task12_pre, task12_post, expect)
add_task("sqrt13 (https://stardot.org.uk/forums/viewtopic.php?p=367937#p367937)", "sqrt/sqrt13.a", "sqrt13", task13_pre, task13_post, expect)
add_task("sqrt14 (https://stardot.org.uk/forums/viewtopic.php?p=367937#p367937)", "sqrt/sqrt14.a", "sqrt14", task14_pre, task14_post, expect)
add_task("sqrt15 (https://stardot.org.uk/forums/viewtopic.php?p=367937#p367937)", "sqrt/sqrt15.a", "sqrt15", task15_pre, task15_post, expect)
#too slow!
add_task("sqrt16 (https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt16.a)",   "sqrt/sqrt16.a", "sqrt", task16_pre, task16_post, expect)
add_task("sqrt17 (https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt17.a)",   "sqrt/sqrt17.a", "sqrt", task17_pre, task17_post, expect)
add_task("sqrt18 (https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt18.a)",   "sqrt/sqrt18.a", "sqrt", task18_pre, task18_post, expect)

# 2. Run tasks
(file_sizes, spreadsheet) = run_tasks()

# 3. Write out results
with open("sizes.csv", "w") as file:
    file.write("test_name, file_size\n")
    for entry in file_sizes:
        file.write(str(entry[0]) + ", " + str(entry[1]) + "\n")

# 3a. Write out results
with open("results.csv", "w") as file:
    i = 0
    file.write("number")
    for (name, f, start_symbol, pre, post, expect) in tasks:
        file.write("," + name)
    file.write("\n")
    vals = {}
    for col in spreadsheet:
        for row in col:
            vals[row] = 1

    for val in vals:
        file.write(str(i))
        for col in spreadsheet:
            file.write("," + str(col[val]))
        file.write("\n")
        i += 1
