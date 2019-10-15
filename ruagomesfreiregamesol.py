import math
from itertools import product, permutations

def bfs(transitions, src):
    N = len(transitions)

    vertices = [src]
    distance = [math.inf] * N
    distance[src] = 0

    for i in range(N - 1):
        v = vertices[0]
        vertices = vertices[1:]

        for t in transitions[v]:
            child = t[1] # Transições são da forma (tipo_de_bilhete, vértice)
            if distance[child] == math.inf:
                distance[child] = distance[v] + 1
                vertices.append(child)

    return distance

class State:
    def __init__(self, positions, tickets):
        self.positions = positions
        self.tickets = tickets

class Action:
    def __init__(self, ticketsUsed, newPositions):
        self.ticketsUsed = ticketsUsed
        self.newPositions = newPositions

class Node:
    def __init__(self, state, parent, action, pathCost, problem):
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost
        self.totalCost = self.calculateTotalCost(problem)

    def expand(self, problem):
        children = []
        for action in problem.getPossibleActions(self.state):
            children.append(self.childNode(problem, action))
        return children

    def childNode(self, problem, action):
        return Node(
            problem.result(self.state, action),       # Novo estado
            self,                                     # O pai do filho é o próprio nó
            action,                                   # Ação usada para gerar o filho
            self.pathCost + 1)                        # O novo custo é o custo deste nó + 1
    
    def calculateTotalCost(self, problem):
        estimatedDistance = problem.distance[]
        # f(n) =   g(n)      +    h(n)
        return self.pathCost + estimatedDistance


class MinPriorityQueue:
    def __init__(self):
        self.nodes = []
    
    def pop(self):
        l = len(self.nodes)
        if l == 0:
            return None
        elif l == 1:
            return self.nodes.pop()
        
        firstNode = self.nodes[0]
        self.nodes[0] = self.nodes.pop()
        self.fixSubtree(0)

        return firstNode

    def fixSubtree(self, root):
        size = len(self.nodes)
        
        left = 2 * root + 1
        right = 2 * root + 2
        largest = root
        largestVal = self.nodes[largest].totalCost

        if left < size:
            leftVal = self.nodes[left].totalCost
            if leftVal < rootVal:
                largest = left

    def exchange(self, n1, n2):
        temp = self.n1
        self.n1 = self.n2
        self.n2 = temp

def treeSearch(problem):
    frontier = PriorityQueue()
    frontier = [Node(problem.initialState, None, problem.initialAction, 0)]
    while True:
        if not frontier:                         # Retornar [] se a fronteira ficar vazia
            return []
        node = extractNode(frontier)             # Escolher nó da fronteira de expansão
        if problem.isGoal(node.state):           # Se o nó tiver o estado objetivo,
            return problem.tracebackPath(node)   # devolver o caminho encontrado
        for child in node.expand(problem):       # Expandir o nó atual


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
        if self.anyorder:
            for p in permutations(self.goal, self.numPolicemen):
                if state.positions == list(p):
                    return True
            return False
        return state.positions == self.goal

