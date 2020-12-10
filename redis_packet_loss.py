import time
import os
import sys
from random import randrange

if len(sys.argv) < 3:
    print("Expect 2 arguments: 1 - pattern type (linear, expo, random); 2 - initial loss rate (%)")
    sys.exit(1)

pattern = sys.argv[1]
rate = int(sys.argv[2])

if pattern != "linear" and pattern != "expo" and pattern != "random":
    print("The first argument should have one of the following values: linear, expo, random")
    sys.exit(1)

if rate < 0 or rate > 100:
    print("The second argument should have the value in a range between 0 and 100")
    sys.exit(1)

if pattern == "linear":
    rate_inc = 1

if pattern == "expo":
    rate_inc = 2

if pattern == "random":
    rate_inc = 2


def run_packet_loss_rate_change_command(rate):
    command = "sudo tc qdisc change dev eth0 root netem loss " + str(rate) + "%"
    print(command)
    os.system(command)


command = "sudo tc qdisc add dev eth0 root netem loss " + str(rate) + "%"
os.system(command)

iteration = 0
while True:

    if pattern == "linear":
        rate = rate + rate_inc
        if rate > 100:
            rate = 100
        run_packet_loss_rate_change_command(rate)

    if pattern == "expo":
        rate = rate_inc ** iteration
        if rate > 100:
            rate = 100
        run_packet_loss_rate_change_command(rate)

    if pattern == "random":
        rate = rate + rate_inc * randrange(2)
        if rate > 100:
            rate = 100
        run_packet_loss_rate_change_command(rate)

    time.sleep(60)
    iteration += 1
