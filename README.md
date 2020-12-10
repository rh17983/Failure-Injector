# Fault-Injector
###### The scrips must be run locally on the target machine

## 1. CPU Hog fault injection
#### python cpu_hog.py fault-injection-intensity-pattern fault-injection-interval

where:<br>
1. fault-injection-intensity-pattern is a string indicating one of the following injection intensity patterns: {linear, expo, random}
2. fault-injection-interval is a positive integer indicating the time period (in seconds) between the sequential injections

#### Examples:
1. python cpu_hog.py linear 60
2. python cpu_hog.py expo 60
3. python cpu_hog.py random 10


## 2. Packet Loss fault injection
#### python packet_loss.py fault-injection-intensity-pattern initial-loss-rate

where:<br>
1. fault-injection-intensity-pattern is a string indicating one of the following injection intensity patterns: {linear, expo, random}
2. initial-loss-rate is an integer in the range [0 - 99] indicating the initial loss rate (%)

#### Examples:
1. python redis_packet_loss.py linear 25
2. python redis_packet_loss.py expo 1
3. python redis_packet_loss.py random 0