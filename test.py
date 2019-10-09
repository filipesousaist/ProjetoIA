from pickle import load
from pprint import pprint

with open("coords.pickle", "rb") as fp:
    coords = load(fp)

with open("mapasgraph.pickle", "rb") as fp:
    graph = load(fp)

pprint(coords)
pprint(graph)
