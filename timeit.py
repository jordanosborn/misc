#!/usr/local/bin/python3
from time import time
from math import sqrt, log10, floor
from sys import argv
import subprocess as sp

times = []
mean = lambda l: sum(l) / len(l)
stdev = lambda l: sqrt(mean(list(map(lambda x: x ** 2, l))) - mean(l) ** 2)
maxString = lambda l: max(list(map(lambda s: len(s), l)))

try:
	try:
		_, commands, roundover = argv
	except ValueError:
		_, commands = argv
		roundover = 10
	maxTab = maxString(commands.split(';')) + 1
	roundover = int(roundover)
except ValueError:
	print("Args incorrectly formatted try: timeit \"command1;command2\":string roundover:int")
else:
	print("Command\tMean\tStdv".expandtabs(maxTab))
	for i, command in enumerate(commands.split(';')):
		for j in range(0, int(roundover)):
			t0 = time()
			sp.run(command.strip().split(), stdout=sp.DEVNULL)
			times.append(time() - t0)
		std = stdev(times)
		lg = -floor(log10(std))
		n = lg + 1 if int(std * 10 ** lg) == 1 else lg
		print("{}\t{}\t{}".format(command, round(mean(times), n), round(std, n)).expandtabs(maxTab))
