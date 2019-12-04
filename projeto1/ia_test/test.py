# python test.py input.in --map --save passed.in

import os
import pickle
import argparse
import matplotlib.pyplot as plt
import time

from tabulate import tabulate
from solution import SearchProblem

from common import validate_path

class TestResult:
	time = 0.0
	error = None
	path = []

class TestCase:

	def __init__(self, coordinates, model):
		self.coordinates = coordinates
		self.model = model

	def run_test(self, sample):
		search_problem = SearchProblem(sample.goal, self.model, self.coordinates)

		time_start = time.process_time()
		solution_path = search_problem.search(
			sample.init,
			tickets=sample.tickets,
			limitdepth=sample.limit_depth,
			limitexp=sample.limit_exp,
			anyorder=sample.any_order)
		time_lapsed = (time.process_time() - time_start) * 1000

		sample.path = solution_path
		sample.time = time_lapsed
		validation = validate_path(self.model, sample)

		result = TestResult()
		result.error = validation
		result.path = solution_path
		result.time = time_lapsed

		return result

	def plot_path(self, path, filename):
		plt.clf()
		img = plt.imread("map.png")
		plt.imshow(img)

		agents_location = path[0][1]
		agents_quantity = len(agents_location)
		colors = ['r', 'g', 'b']

		for agent_index in range(agents_quantity):
			current_state = agents_location[agent_index]
			for movement in path:
				next_state = movement[1][agent_index]

				[current_x, current_y] = self.coordinates[current_state - 1]
				[next_x, next_y] = self.coordinates[next_state - 1]

				color = colors[agent_index % len(colors)]

				plt.plot([current_x, next_x], [current_y, next_y], color)
				current_state = next_state

		plt.axis('off')
		fig = plt.gcf()
		fig.set_size_inches(18.5, 10.5)
		fig.savefig(filename, dpi=100)


def parse_args():

	parser = argparse.ArgumentParser()
	parser.add_argument("pickle", help="Pickle file with input")

	parser.add_argument("-m", "--map", help="Generate map plot for each test", action="store_true")
	parser.add_argument("-s", "--save", help="Save passed tests to file", default=None)
	parser.add_argument("-t", "--time", help="Save only with time below value", type=float, default=0)

	return parser.parse_args()


def create_output_root():
	output_root = "output"

	if not os.path.exists(output_root):
		os.mkdir(output_root)

	return output_root


def create_output_folder(root):
	i = 0
	while True:
		output_folder = "%s/%d" % (root, i)
		if not os.path.exists(output_folder):
			os.makedirs(output_folder)
			break
		else:
			i += 1
	return output_folder


def main():

	args = parse_args()

	output_root = create_output_root()
	output_folder = create_output_folder(output_root)

	print("saving to", output_folder)

	with open(args.pickle, "rb") as fp:
		samples = pickle.load(fp)

	with open("coordinates.pickle", "rb") as fp:
		coordinates = pickle.load(fp)

	with open("mapgraph.pickle", "rb") as fp:
		[_, model] = pickle.load(fp)

	headers = ["#", "ms", "status"]
	table = []

	total = len(samples)
	saved_samples = []
	passed = 0
	failed = 0
	time_total = 0

	test_case = TestCase(coordinates, model)

	for i, sample in enumerate(samples):
		init = sample.init
		goal = sample.goal
		tickets = sample.tickets

		print("running %d/%d" % (i + 1, total), end='\r')
		test_result = test_case.run_test(sample)
		time_total += test_result.time

		table.append([test_result.time, test_result.error])

		test_folder = output_folder + "/test-{:03d}".format(i)
		os.mkdir(test_folder)

		with open(test_folder + "/res.out", "w") as fp:
			test_table = [
				["init", init],
				["goal", goal],
				["tickets", tickets],
				["time", test_result.time],
				["error", test_result.error],
				["solution", test_result.path],
				["any order", sample.any_order]
			]
			fp.write(tabulate(test_table, tablefmt="plain"))

		if args.map:
			test_case.plot_path(test_result.path, test_folder + "/map.png")

		if test_result.error is None:
			passed += 1
			if args.save:
				if sample.time < args.time or sample.time == 0:
					saved_samples.append(sample)
		else:
			failed += 1

	summary_table = tabulate(table, headers, showindex="always", tablefmt="plain")

	if args.save:
		with open(args.save, "wb") as fp:
			pickle.dump(saved_samples, fp)

	with open(output_folder + "/summary.out", "w") as fp:
		fp.write("elapsed: {}\n".format(time_total))
		fp.write(summary_table)

	print("passed: %d (%.2f%%), failed: %d (%.2f%%), total: %d (%fms)" % (
		passed,
		passed * 100 / total,
		failed,
		failed * 100 / total,
		total,
		time_total))

	print(summary_table)

if __name__ == "__main__":
	main()