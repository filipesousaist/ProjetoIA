import math
from itertools import product
from bfs import bfs
from treeSearch import treeSearch

class State:
    def __init__(self, positions, tickets):
        self.positions = positions
        self.tickets = tickets
    
    def __eq__(self, state):
        return self.positions == state.positions and \
               self.tickets == state.tickets

class Action:
    def __init__(self, ticketsUsed, newPositions):
        self.ticketsUsed = ticketsUsed
        self.newPositions = newPositions
    
    def __eq__(self, action):
        return self.ticketsUsed == action.ticketsUsed and \
               self.newPositions == action.newPositions

class SearchProblem:
    def __init__(self, goal, model, auxheur = []):
        self.goal = goal
        self.transitions = model
        self.numVertices = len(self.transitions) - 1
        self.distances = [[]]
        for v in range(1, self.numVertices + 1):
            self.distances.append(bfs(self.transitions, v))

    def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf, math.inf, math.inf], anyorder = False):
        self.initialState = State(init, tickets)   # Estado inicial (posições, bilhetes)
        self.numPolicemen = len(init) # Nº de polícias
        result = treeSearch(self)
        return result

    def getPossibleActions(self, state):
        # Guardar as ações que cada polícia pode fazer
        actionsByPoliceman = [self.transitions[pos] for pos in state.positions]
        actionCombinations = list(product(*actionsByPoliceman))
        possibleActions = [Action(
            [action[0] for action in actionCombination],
            [action[1] for action in actionCombination])
            for actionCombination in actionCombinations]
        return possibleActions

    def result(self, state, action):
        tickets = state.tickets[:] # Cópia dos bilhetes do estado atual

        for t in action.ticketsUsed:
            tickets[t] -= 1 # Descontar os bilhetes usados para ir para a nova posição

        return State(action, tickets)

    def tracebackPath(self, node):
        if node.parent:
            return self.tracebackPath(node.parent) + [[node.action.ticketsUsed, node.state.postions]]
        return [[[], node.state.positions]]
    
    def isGoal(self, state):
        return state.positions == self.goal

