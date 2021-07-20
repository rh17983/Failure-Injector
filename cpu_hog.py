#!/usr/bin/python
import math
import random
import signal
import sys
import time
from multiprocessing import Process, Value
from random import randrange


def signal_handler(signal_, frame):
    global flag
    flag.value = False
    sys.exit(0)


def cpuhog(loop, sleep):
    while flag.value:
        looptimes = loop.value
        for ii in range(looptimes):
            yy = math.sqrt(2)
        time.sleep(sleep.value)
        # print("cpuhog", loop.value, sleep.value)
    sys.exit(0)


if len(sys.argv) < 2:
    print("Expected 1 argument: Injection intensity pattern")
    sys.exit(1)

pattern = sys.argv[1]

proc_num = 5

flag = Value('b', True)
signal.signal(signal.SIGTERM, signal_handler)

cpuinfo_raw = open('/proc/cpuinfo').readlines()
cpuinfo = list(filter(lambda x: x is not None, [float(line.split(':')[1].strip(' ')) * 3000 if 'MHz' in line else None for line in cpuinfo_raw]))
cpunum = len(cpuinfo)
print("Number of CPUs: ", cpunum)

percent_init = 0
thread_pool = []
sleeptime_lst = []
loop_lst = []

# loop by each CPU to create a threads for each CPU
for i in range(cpunum):

    cpu_clock = float(cpuinfo[i])
    print("cpu_clock:", cpu_clock)

    loop_init = int(cpu_clock * percent_init / 100.0)
    sleep_init = cpu_clock - loop_init

    looptime = Value('i', loop_init)
    sleeptime = Value('d', sleep_init * 1.0 / cpu_clock)

    for j in range(proc_num):
        p = Process(target=cpuhog, args=(looptime, sleeptime,))
        thread_pool.append(p)

    sleeptime_lst.append(sleeptime)
    loop_lst.append(looptime)

for cpu_index in range(cpunum):
    for j in range(proc_num):
        thread_index = cpu_index * proc_num + j
        thread_pool[thread_index].start()
        print("Thread ", thread_index, " started!")

percent = 0
iteration = 0
while flag.value:
    if pattern == "linear":
        percent += 1

    if pattern == "expo":
        percent = int(2 ** iteration)

    if pattern == "random":
        percent += 2 * randrange(2)

    if percent > 100:
        percent = 100

    for i in range(cpunum):
        cpu_clock = float(cpuinfo[i])
        loop_new = int(cpu_clock * percent / 100.0)
        sleep_new = cpu_clock - loop_new

        if sleep_new <= 0.000000000001:
            sleep_new = 0.000000000001

        loop_lst[i].value = loop_new
        sleeptime_lst[i].value = sleep_new * 1.0 / cpu_clock

        print("Cpu_clock:", cpu_clock, "Percent:", percent, "Loop time: " + str(loop_lst[i].value), "Sleep time: " + str(sleeptime_lst[i].value))

    iteration += 1
    time.sleep(60)

for p in thread_pool:
    p.terminate()
