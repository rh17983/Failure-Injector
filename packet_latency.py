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


def run_command(iteration, delay, net_interface, add_dev=False):

    # sudo tc qdisc add dev ens3 root netem delay 97ms
    # sudo tc qdisc change dev ens3 root netem delay 7ms
    # tc -s qdisc

    if add_dev:
        action = "add"
    else:
        action = "change"

    command = "sudo tc qdisc " + action + " dev " + net_interface + " root netem delay " + str(delay) + "ms"
    print(iteration, ":", command)
    # os.system(command)


delay = 0

iteration = 0
while True:

    if pattern == "linear":
        delay += 15

    if pattern == "expo":
        delay += int(1.15 ** iteration)

    if pattern == "random":
        delay += 25 * randrange(2)

    if iteration == 0:
        run_command(iteration, delay, net_interface, True)
    else:
        run_command(iteration, delay, net_interface)

    time.sleep(1)
    iteration += 1
