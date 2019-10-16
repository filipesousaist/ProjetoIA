import math
from itertools import product, permutations

MAX_HEURISTIC = 8 # Determinada experimentalmente

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
    
    def result(self, action):
        tickets = self.tickets[:] # Cópia dos bilhetes do estado atual

        for t in action.ticketsUsed:
            tickets[t] -= 1 # Descontar os bilhetes usados para ir para a nova posição

        return State(action.newPositions, tickets)

class Action:
    def __init__(self, ticketsUsed, newPositions):
        self.ticketsUsed = ticketsUsed
        self.newPositions = newPositions

class Node:
    def __init__(self, problem, state, parent, action, pathCost):
        self.problem = problem
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost
        self.totalCost = self.calculateTotalCost()

    def expand(self):
        children = []
        for action in self.problem.getPossibleActions(self.state):
            children.append(self.childNode(action))
        return children

    def childNode(self, action):
        return Node(
            self.problem,
            self.state.result(action),  # Novo estado
            self,                       # O pai do filho é o próprio nó
            action,                     # Ação usada para gerar o filho
            self.pathCost + 1)          # O novo custo é o custo deste nó + 1
    
    def calculateTotalCost(self):
        if self.problem.anyorder: # Obter todas as permutações da posição objetivo
            goals = [list(goal) for goal in permutations(self.problem.goal, self.problem.numPolicemen)]
        else:
            goals = [self.problem.goal]

        goalMaxDistances = []
        for goal in goals: # Calcular a distância do polícia que está mais longe do seu objetivo
            distances = [self.problem.distances[self.state.positions[i]][goal[i]] for i in range(self.problem.numPolicemen)]
            goalMaxDistances.append(max(distances))
        
        estimatedDistance = min(goalMaxDistances)

        # f(n) =   g(n)      +        h(n)
        return self.pathCost + estimatedDistance

    def tracebackPath(self):
        print(self.state.positions, self.totalCost)
        if self.parent:
            return self.parent.tracebackPath() + [[self.action.ticketsUsed, self.state.positions]]
        return [[self.action.ticketsUsed, self.state.positions]]

class Frontier:
    def __init__(self, initialSize, initialNode):
        self.mainList = [[]] * initialSize
        self.mainList[initialNode.totalCost].append(initialNode)
        self.lowerBound = initialNode.totalCost
        self.upperBound = initialSize - 1
        
    def insert(self, node):
        if node.totalCost > self.upperBound:
            self.mainList += [[]] * (node.totalCost - self.upperBound)
            self.upperBound = node.totalCost
                
        self.mainList[node.totalCost].append(node)
    
    def pop(self):
        while not self.mainList[self.lowerBound]:
            self.lowerBound += 1
            if self.lowerBound > self.upperBound:
                return None

        #return self.mainList[self.lowerBound].pop()

        node = self.mainList[self.lowerBound][0]
        del self.mainList[self.lowerBound][0]
        return node

def aStar(problem): # A*
    frontier = Frontier(MAX_HEURISTIC, Node(problem, problem.initialState, None, problem.initialAction, 0))
    
    while True:
        node = frontier.pop()                    # Escolher nó da fronteira de expansão
        if not node:                             # Retornar [] se a fronteira ficar vazia
            return []
        if problem.isGoal(node.state):           # Se o nó tiver o estado objetivo,
            return node.tracebackPath()          # devolver o caminho encontrado
        for child in node.expand():              # Expandir o nó atual
            frontier.insert(child)

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
        self.anyorder = anyorder # Se interessa ou não que polícia está em cada posição objetivo

        return aStar(self)

    def getPossibleActions(self, state):
        # Guardar as ações que cada polícia pode fazer
        actionsByPoliceman = [self.transitions[pos] for pos in state.positions]

        # Lista de combinações possíveis de ações no formato ([transporte1, pos1], [transporte2, pos2], ...) 
        # Ex.: ([0, 20], [1, 36], [0, 37])
        moveCombinations = list(product(*actionsByPoliceman))

        def validTickets(comb):
            ticketsCopy = state.tickets[:]
            for move in comb: # Descontar os bilhetes usados
                ticketsCopy[move[0]] -= 1
            
            for ticketType in ticketsCopy: # Se forem usados mais bilhetes de um tipo
                if ticketType < 0:         # do que aqueles que existem, a ação é inválida
                    return False
            return True

        def validPositions(comb):
            for i in range(len(comb) - 1):
                for j in range(i + 1, len(comb)):
                    if comb[i][1] == comb[j][1]: # Dois polícias querem ir para a mesma 
                        return False             # posição -> Ação inválida
            return True
        
        # Remover as ações inválidas
        validMoveCombinations = []
        for comb in moveCombinations:
            if validTickets(comb) and validPositions(comb):
                validMoveCombinations.append(comb)

        # Lista de ações no formato Action([transporte1, transporte2, ...], [pos1, pos2, ...])
        # Ex.: ([0, 1, 0], [20, 36, 37])
        possibleActions = [Action(
            [move[0] for move in comb],
            [move[1] for move in comb])
            for comb in validMoveCombinations]
        
        return possibleActions
    
    def isGoal(self, state):
        if self.anyorder:
            for p in permutations(self.goal, self.numPolicemen):
                if state.positions == list(p):
                    return True
            return False
        return state.positions == self.goal