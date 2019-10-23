# python gen.py enunciado.in

import pickle
import random
import sys
from math import inf

from common import Sample

agents = 3
amount = 0

def create_sample(init, goal, tickets, limit_exp, limit_depth, any_order):
    sample = Sample()
    sample.init = init
    sample.goal = goal
    sample.tickets = tickets
    sample.limit_depth = limit_depth
    sample.limit_exp = limit_exp
    sample.any_order = any_order
    return sample

samples = [
    create_sample(init=[30],            goal=[56],         tickets=[inf, inf, inf], limit_exp=2000, limit_depth=20, any_order=False),
    create_sample(init=[30],            goal=[56],         tickets=[5, 5, 2],       limit_exp=2000, limit_depth=20, any_order=False),
    create_sample(init=[1, 3, 7],       goal=[2, 21, 9],   tickets=[inf, inf, inf], limit_exp=2000, limit_depth=20, any_order=False),
    create_sample(init=[30, 40, 109],   goal=[61, 60, 71], tickets=[inf, inf, inf], limit_exp=2000, limit_depth=20, any_order=False),
    create_sample(init=[30, 40, 109],   goal=[63, 61, 70], tickets=[5, 20, 2],      limit_exp=3000, limit_depth=10, any_order=True),
]

with open(sys.argv[1], "wb") as fp:
    pickle.dump(samples, fp)
