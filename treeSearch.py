class Node:
    def __init__(self, state, parent, action, pathCost):
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost

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

def extractNode(frontier):
    return frontier.pop()

def treeSearch(problem):
    frontier = [Node(problem.initialState, None, problem.initialAction, 0)]
    while True:
        if not frontier:                         # Retornar [] se a fronteira ficar vazia
            return []
        node = extractNode(frontier)             # Escolher nó da fronteira de expansão
        if problem.isGoal(node.state):           # Se o nó tiver o estado objetivo,
            return problem.tracebackPath(node)   # devolver o caminho encontrado
        frontier += node.expand(problem)         # Expandir o nó atual
