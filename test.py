import py65
import assemble
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
    task_index = 0
    for (name, file, start_symbol, pre, post, expect) in tasks:
        spreadsheet.append({})
        code = file
        print("Running task " + code)
        cycles = run_task(name, code, start_symbol, pre, post, expect)
        print("Task " + code + " completed")
        for key in cycles:
            spreadsheet[task_index][key] = cycles[key]
        task_index += 1
    return spreadsheet

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
    symbols = assemble.assemble(codefile, "TESTME")

    start = symbols[start_symbol]
    startHexString = '{:04x}'.format(start)

    mon = Monitor()
    mon.do_load("./TESTME $" + startHexString)
    start_time = time.perf_counter()
    cycles = {}
    for v in range(0,65536):
        pre(mon, symbols, v)

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
    return cycles

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

#def taskadc1_pre(mon, symbols, v):
#    set_memory(mon, symbols["mem1"], v & 255)
#    set_memory(mon, symbols["mem2"], v // 256)
#
#def taskadc1_post(mon, symbols, v):
#    flags[v] = mon._mpu.p
#    return 0


# 1. Add tasks
add_task("sqrt1 (https://codebase64.org/doku.php?id=base:fast_sqrt)", "sqrt/sqrt1.a", "start", task1_pre, task1_post, expect)
add_task("sqrt2 (http://www.6502.org/source/integers/root.htm)",      "sqrt/sqrt2.a", "SqRoot", task2_pre, task2_post, expect)
add_task("sqrt3 (http://www.txbobsc.com/aal/1986/aal8611.html#a1)",   "sqrt/sqrt3.a", "SQRT", task3_pre, task3_post, expect)
#too slow!
#add_task("sqrt4 (http://www.txbobsc.com/aal/1985/aal8506.html#a2)",   "sqrt/sqrt4.a", "SQRT", task4_pre, task4_post, expect)
add_task("sqrt5 (http://www.txbobsc.com/aal/1986/aal8609.html#a8)",   "sqrt/sqrt5.a", "SQR3", task5_pre, task5_post, expect)
add_task("sqrt6 (https://www.bbcelite.com/master/main/subroutine/ll5.html)", "sqrt/sqrt6.a", "LL5", task6_pre, task6_post, expect)
add_task("sqrt7 (http://6502org.wikidot.com/software-math-sqrt)",     "sqrt/sqrt7.a", "start", task7_pre, task7_post, expect)
#too slow!
#add_task("sqrt8 (https://mdfs.net/Info/Comp/6502/ProgTips/SqRoot)",     "sqrt/sqrt8.a", "sqr", task8_pre, task8_post, expect)
add_task("sqrt9 (https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt9.a)", "sqrt/sqrt9.a", "sqrt16", task9_pre, task9_post, expect)
add_task("sqrt10 (https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt10.a)", "sqrt/sqrt10.a", "start", task10_pre, task10_post, expect)
add_task("sqrt11 (http://forum.6502.org/viewtopic.php?p=90611#p90611)", "sqrt/sqrt11.a", "sqrt", task11_pre, task11_post, expect)

#flags = [0] * 65536
#add_task("adc1", "sqrt/adc1.a", "adc1", taskadc1_pre, taskadc1_post, None)

# 2. Run tasks
spreadsheet = run_tasks()

# 3. Write out results
#with open("results.csv", "w") as file:
#    file.write("overflow flag,")
#    for x in range(0,256):
#        if x != 0:
#            file.write(",")
#        file.write(str(x))
#
#    for v in range(0,65536):
#        x = v & 255
#        y = v // 256
#        if x == 0:
#            file.write("\n" + str(y) + ",")
#        if x != 0:
#            file.write(",")
#        file.write(str((flags[v] & 1)//1))


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