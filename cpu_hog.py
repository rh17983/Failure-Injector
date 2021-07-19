#!/usr/bin/python

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
        for i in range(looptimes):
            pass
        time.sleep(sleep.value)
    sys.exit(0)


if len(sys.argv) < 3:
    print("Expected 2 arguments: (1) Injection intensity patternt, (2) Injection interval")
    sys.exit(1)

_linear = False
_random = False
_exponential = False

intensity = str(sys.argv[1])
try:
    interval = int(sys.argv[2])
except ValueError:
    print("interval cannot be parsed!!Aborting..")
    sys.exit(1)

if intensity == 'linear':
    _linear = True

if intensity == 'expo':
    _exponential = True

if intensity == 'random':
    _random = True


flag = Value('b', True)
signal.signal(signal.SIGTERM, signal_handler)

cpuinfo_raw = open('/proc/cpuinfo').readlines()
cpuinfo = list(filter(lambda x: x is not None, [float(line.split(':')[1].strip(' ')) * 3000 if 'MHz' in line else None for line in cpuinfo_raw]))
cpunum = len(cpuinfo)
print("Number of CPU: ", cpunum)

percent_init = 0
thread_pool = []
sleeptime_lst = []
loop_lst = []

proc_num = 20

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

    if _linear:
        percent += 1

    if _exponential:
        percent = int(2 ** iteration)

    if _random:
        percent += 2 * randrange(2)

    if percent > 100:
        percent = 100

    for i in range(cpunum):
        cpu_clock = float(cpuinfo[i])
        print("cpu_clock:", cpu_clock, "percent:", percent)

        loop_new = int(cpu_clock * percent / 100.0)
        sleep_new = cpu_clock - loop_new

        if sleep_new <= 0.000000000001:
            sleep_new = 0.000000000001

        loop_lst[i].value = loop_new
        sleeptime_lst[i].value = sleep_new * 1.0 / cpu_clock
        print("Loop time: " + str(loop_lst[i].value), "Sleep time: " + str(sleeptime_lst[i].value))

    iteration += 1
    time.sleep(interval)

#    print percent, [v.value for v in loop_lst],
# [v.value for v in sleeptime_lst]

for p in thread_pool:
    p.terminate()
