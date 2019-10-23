# Run this in debug mode to inspect pickle content
import pickle

with open("coordinates.pickle", "rb") as fp:
    coordinates = pickle.load(fp)

with open("mapgraph.pickle", "rb") as fp:
    mapasgraph = pickle.load(fp)

with open("input.in", "rb") as fp:
    pickle_input = pickle.load(fp)

pass  # Set debug point here
