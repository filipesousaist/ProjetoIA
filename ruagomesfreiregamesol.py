import math
from itertools import product
from bfs import bfs
from treeSearch import treeSearch

class State:
    def __init__(self, positions, tickets):
        self.positions = positions
        self.tickets = tickets

class Action:
    def __init__(self, ticketsUsed, newPositions):
        self.ticketsUsed = ticketsUsed
        self.newPositions = newPositions

class SearchProblem:
    def __init__(self, goal, model, auxheur = []):
        self.goal = goal
        self.transitions = model
        self.numVertices = len(self.transitions) - 1
        self.distances = [[]]
        for v in range(1, self.numVertices + 1):
            self.distances.append(bfs(self.transitions, v))

    def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf, math.inf, math.inf], anyorder = False):
        self.initialState = State(init, tickets) # Estado inicial (posições, bilhetes)
        self.initialAction = Action([], init) # Ação inicial
        self.numPolicemen = len(init) # Nº de polícias
        result = treeSearch(self)
        return result

    def getPossibleActions(self, state):
        # Guardar as ações que cada polícia pode fazer
        actionsByPoliceman = [self.transitions[pos] for pos in state.positions]

        # Lista de combinações possíveis de ações no formato ([transporte1, pos1], [transporte2, pos2], ...) 
        # Ex.: ([0, 20], [1, 36], [0, 37])
        actionCombinations = list(product(*actionsByPoliceman))

        # Remover as ações inválidas
        validActionCombinations = []
        for comb in actionCombinations:
            ticketsCopy = state.tickets[:]
            for action in comb: # Descontar os bilhetes usados
                ticketsCopy[action[0]] -= 1
            validTickets = True
            for ticketType in ticketsCopy: # Se forem usados mais bilhetes de um tipo
                if ticketType < 0:         # do que aqueles que existem, a ação é inválida
                    validTickets = False
                    break
            if not validTickets:
                continue
            
            validPositions = True
            for i in range(len(comb)):
                for j in range(i + 1, len(comb)):
                    if comb[i][1] == comb[j][1]: # Dois polícias querem ir para a mesma posição -> Ação inválida
                        validPositions = False
                        break
                if not validPositions:
                    break
            if not validPositions: 
                continue

            validActionCombinations.append(comb)

        # Lista de ações no formato Action([transporte1, transporte2, ...], [pos1, pos2, ...])
        # Ex.: ([0, 1, 0], [20, 36, 37])
        possibleActions = [Action(
            [action[0] for action in actionCombination],
            [action[1] for action in actionCombination])
            for actionCombination in validActionCombinations]
        
        return possibleActions

    def result(self, state, action):
        tickets = state.tickets[:] # Cópia dos bilhetes do estado atual

        for t in action.ticketsUsed:
            tickets[t] -= 1 # Descontar os bilhetes usados para ir para a nova posição

        return State(action.newPositions, tickets)

    def tracebackPath(self, node):
        if node.parent:
            return self.tracebackPath(node.parent) + [[node.action.ticketsUsed, node.state.postions]]
        return [[[], node.state.positions]]
    
    def isGoal(self, state):
        return state.positions == self.goal

