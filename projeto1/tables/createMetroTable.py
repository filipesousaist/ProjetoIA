from pickle import load
from pprint import pprint
import math

def bfs(transitions, src):
    N = len(transitions)

    vertices = [src]
    distance = [math.inf] * N
    distance[src] = 0

    for i in range(N - 1):
        if not vertices:
            return distance

        v = vertices[0]
        vertices = vertices[1:]

        for t in transitions[v]:
            if (t[0] != 2):
                continue

            child = t[1] # Transições são da forma (tipo_de_bilhete, vértice)
            if distance[child] == math.inf:
                distance[child] = distance[v] + 1
                vertices.append(child)

    return distance

with open("mapasgraph2.pickle", "rb") as fp:
    graph = load(fp)

transitions = graph[1]

distances = [[]]
for v in range(1, len(transitions)):
    distances.append(bfs(transitions, v))

print(distances)