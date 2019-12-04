# python validate.py input.in

# Tests whether a file of samples has valid solutions

import pickle
import sys

from common import validate_path

with open(sys.argv[1],  "rb") as fp:
	samples = pickle.load(fp)

with open("mapgraph.pickle", "rb") as fp:
	[_, model] = pickle.load(fp)

passed = 0
total = len(samples)

for sample in samples:
	if validate_path(model, sample) is None:
		passed += 1

failed = total - passed

print("passed: %d (%.2f%%)" % (passed, passed * 100.0 / total))
print("failed: %d (%.2f%%)" % (failed, failed * 100.0 / total))
print("total:", total)