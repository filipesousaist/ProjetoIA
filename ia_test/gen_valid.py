# python gen_valid.py input.in

import itertools
import pickle
import random
import sys
import copy

from common import Sample

class Config:
	amount = 5
	agents = 3

	states = range(1, 113 + 1)
	tickets = range(10, 11)

	# Used for calculating path
	limit_depth = range(4, 6)
	limit_exp = range(1000, 2000)

	# Bigger limit when saving
	limit_depth_error = 10
	limit_exp_error = 1000

	any_order = False

class Generator:
	def __init__(self):
		self.limit_exp = 0

	def create_random_samples(self, n):
		samples = []
		while n > 0:
			init = random.sample(Config.states, k=Config.agents)
			tickets = random.choices(Config.tickets, k=3)
			depth = random.choice(Config.limit_depth)

			limit_exp = self.limit_exp = random.choice(Config.limit_exp)
			path = self.random_path(init, tickets, depth)

			if path is not None:
				sample = Sample()
				sample.init = init
				sample.tickets = tickets
				sample.limit_exp = limit_exp + Config.limit_exp_error
				sample.limit_depth = depth + Config.limit_depth_error
				sample.any_order = Config.any_order
				sample.path = [[[], init]] + copy.deepcopy(path)

				sample.goal = list(path[-1][1])
				if Config.any_order:
					random.shuffle(sample.goal) # Random-order goal

				samples.append(sample)
				n -= 1

		return samples

	def random_path(self, pos, tickets, depth):

		if len(pos) > len(set(pos)):
			return None
		elif depth == 0:
			# We have found a valid path!
			return []
		elif self.limit_exp == 0:
			return None

		self.limit_exp -= 1

		def get_choices(p):
			x = model[p]
			random.shuffle(x)
			return x

		choices = map(get_choices, pos)
		movements = itertools.product(*choices)

		for movement in movements:
			[transport, position] = zip(*movement)
			# Reduce tickets
			child_tickets = tickets[:]
			for t in transport:
				child_tickets[t] -= 1
			# Have we spent all tickets?
			if any(child_tickets[t] < 0 for t in transport):
				continue
			position = list(position)
			transport = list(transport)
			# Continue searching for path
			result = self.random_path(position, child_tickets, depth - 1)
			if result is None:
				continue
			else:
				return [[transport, position]] + result

		return None

with open("mapgraph.pickle", "rb") as fp:
	[_, model] = pickle.load(fp)

samples = Generator().create_random_samples(Config.amount)

with open(sys.argv[1], "wb") as fp:
	pickle.dump(samples, fp)
