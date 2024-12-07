import math

def bfs(transitions, src):
    N = len(transitions)

    vertices = [src]
    distance = [math.inf] * N
    distance[src] = 0

    for _ in range(N - 1):
        v = vertices[0]
        vertices = vertices[1:]

        for t in transitions[v]:
            child = t[1] # Transições são da forma (tipo_de_bilhete, vértice)
            if distance[child] == math.inf:
                distance[child] = distance[v] + 1
                vertices.append(child)

    return distance