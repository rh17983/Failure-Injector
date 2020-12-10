# Fault-Injector

## 1. CPU Hog fault injection
#### python cpu_hog.py fault-injection-intensity-pattern fault-injection-interval

where:<br>
1. fault-injection-intensity-pattern is a string indicating one of the following injection intensity patterns: {linear, expo, random}
2. fault-injection-interval is an integer indicating the time period between the sequential injections

#### Example:
1. python cpu_hog.py linear 60
2. python cpu_hog.py expo 60
3. python cpu_hog.py random 10