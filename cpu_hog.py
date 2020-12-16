#!/usr/bin/python

import random
import signal
import sys
import time
from multiprocessing import Process, Value


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
cpuinfo = filter(lambda x: x is not None, [float(line.split(':')[1].strip(' ')) * 3000 if 'MHz' in line else None for line in cpuinfo_raw])
cpunum = len(cpuinfo)

print("Nnumber of CPU: ", cpunum)

percent_init = 0
thread_pool = []
sleeptime_lst = []
loop_lst = []

# loop by each CPU to create a threads for each CPU
for i in range(cpunum):

    cpu_clock = float(cpuinfo[i])
    loop_init = int(cpu_clock * percent_init / 100.0)
    sleep_init = cpu_clock - loop_init

    looptime = Value('i', loop_init)
    sleeptime = Value('d', sleep_init * 1.0 / cpu_clock)

    p = Process(target=cpuhog, args=(looptime, sleeptime,))
    thread_pool.append(p)
    p = Process(target=cpuhog, args=(looptime, sleeptime,))
    thread_pool.append(p)
    p = Process(target=cpuhog, args=(looptime, sleeptime,))
    thread_pool.append(p)
    p = Process(target=cpuhog, args=(looptime, sleeptime,))
    thread_pool.append(p)
    p = Process(target=cpuhog, args=(looptime, sleeptime,))
    thread_pool.append(p)

    sleeptime_lst.append(sleeptime)
    loop_lst.append(looptime)

print(len(thread_pool))

step_size = 5
for i in range(cpunum):
    for j in range(step_size):
        thread_id = i * step_size + j
        thread_pool[thread_id].start()
        print("Thread ", thread_id, " started!")

percent = percent_init
expo_scale = 1

while flag.value:

    time.sleep(interval)

    if percent < 500:
        scale = 1

        if _linear:
            scale = 1

        if _random:
            if random.random() > 0.5:
                scale = 0
            else:
                scale = 1

        if _exponential:
            scale = expo_scale
            expo_scale += 1

        percent += scale

    for i in range(cpunum):
        cpu_clock = float(cpuinfo[i])
        loop_new = int(cpu_clock * percent / 100.0)
        sleep_new = cpu_clock - loop_new

        if sleep_new <= 0.000000000001:
            sleep_new = 0.000000000001

        loop_lst[i].value = loop_new
        print("Looptimes: " + str(loop_lst[i].value))
        sleeptime_lst[i].value = sleep_new * 1.0 / cpu_clock
        print("Sleeptime: " + str(sleeptime_lst[i].value))

#    print percent, [v.value for v in loop_lst],
# [v.value for v in sleeptime_lst]

for p in thread_pool:
    p.terminate()
