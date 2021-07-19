import time
import os
import sys
from random import randrange

if len(sys.argv) < 3:
    print("Expect 2 arguments: 1 - pattern type (linear, expo, random); 2 - network interface name")
    sys.exit(1)

pattern = sys.argv[1]
net_interface = str(sys.argv[2])

if pattern != "linear" and pattern != "expo" and pattern != "random":
    print("The first argument should have one of the following values: linear, expo, random")
    sys.exit(1)


def run_command(iteration, rate, net_interface, add_dev=False):

    if add_dev:
        action = "add"
    else:
        action = "change"

    command = "sudo tc qdisc " + action + " dev " + net_interface + " root netem loss " + str(rate) + "%"
    print(iteration, ":", command)
    os.system(command)


rate = 0
iteration = 0
while True:
    if pattern == "linear":
        rate += 2

    if pattern == "expo":
        rate += int(1.2 ** iteration)

    if pattern == "random":
        rate += 4 * randrange(2)

    if rate > 100:
        rate = 100

    if iteration == 0:
        run_command(iteration, rate, net_interface, True)
    else:
        run_command(iteration, rate, net_interface)

    time.sleep(60)
    iteration += 1
