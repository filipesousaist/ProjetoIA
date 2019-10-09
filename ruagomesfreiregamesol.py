import math
from bfs import bfs
from treeSearch import treeSearch

class State:
    def __init__(self, positions, tickets):
        self.positions = positions
        self.tickets = tickets

class SearchProblem:
    def __init__(self, goal, model, auxheur = []):
        self.goal = goal
        self.transitions = model
        self.numVertices = len(self.transitions) - 1
        self.distances = [[]]
        for v in range(1, self.numVertices + 1):
            self.distances.append(bfs(self.transitions, v))

    def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf, math.inf, math.inf], anyorder = False):
        self.initialState = State(init, tickets)
        return treeSearch(self)

    def result(self, state, action):
        tickets = state.tickets[:] # Cópia dos bilhetes do estado atual

        ticketsUsed = getTicketsUsed(state.position, action)
        for t in ticketsUsed:
            tickets[t] -= 1 # Descontar os bilhetes usados para ir para a nova posição

        return State(action, tickets)


    def getTicketsUsed(self, pos1, pos2):
        numPos = len(pos1)

        ticketsUsed = []
        for i in range(numPos):
            for edge in self.transitions[pos1[i]]:
                if edge[1] == pos2[i]:
                    ticketsUsed[i] = edge[0]
                    break

    def tracebackPath(self, node):
        if node.parent:
            ticketsUsed = getTicketsUsed(node.parent.state.positions, node.state.positions)
            return tracebackPath(node.parent) + [[ticketsUsed, node.state.postions]]
        return [[[], node.state.positions]]
