import math


frequency = 2450
signalLevel = -60
# frequency = 2412
# signalLevel = -57

print(10 ** ((27.55 - (20 * math.log10(frequency)) + abs(signalLevel))/20))
