import random

# LearningAgent to implement
# no knowledeg about the environment can be used
# the code should work even with another environment
class LearningAgent:

    # init
    # nS maximum number of states
    # nA maximum number of action per state
    def __init__(self,nS,nA):

        # define this function
        self.nS = nS
        self.nA = nA
    
        self.GAMMA = 0.8
        self.UPDATE_TIMES = 15

        self.ALPHA_MIN = 0.15
        self.ALPHA_MULT = 0.9992
        self.EXPLORATION_MIN = 0.2
        self.EXPLORATION_MULT = 0.9992

        self.alpha = 0.7
        self.exploration_rate = 0.8

        self.visited = [False] * nS

        self.Q = [None for _ in range(nS)]
        self.N = [None for _ in range(nS)]
        self.model = [[] for _ in range(nS)]
        self.visitedSet = set()
        self.usedActions = [set() for _ in range(nS)]
    
    # Select one action, used when learning  
    # st - is the current state
    # aa - is the set of possible actions
    # for a given state they are always given in the same order
    # returns
    # a - the index to the action in aa
    def selectactiontolearn(self,st,aa):
        # define this function
        # print("select one action to learn better")
        a = 0

        numActions = len(aa)

        self.exploration_rate = max(self.EXPLORATION_MIN, self.exploration_rate * self.EXPLORATION_MULT)

        if not self.visited[st]:
            self.visited[st] = True
            self.visitedSet.add(st)
            self.Q[st] = [0] * numActions
            self.N[st] = [0] * numActions
            for _ in range(numActions):
                self.model[st].append([])
            return random.randint(0, numActions - 1)

        if random.random() < self.exploration_rate: # Explore
            numExecutions = self.N[st] # Number of times that each action was executed in this state
            minExecutions = min(numExecutions) # Minimum number of executions for an action of that state
            minIndices = [actionIndex for actionIndex in range(numActions) if numExecutions[actionIndex] == minExecutions]
            
            a = random.choice(minIndices) # Choose randomly if there is more than one with the same value
            
        else: # Exploit best state
            rewards = self.Q[st]
            maxReward = max(rewards)
            maxIndices = [actionIndex for actionIndex in range(numActions) if rewards[actionIndex] == maxReward]

            a = random.choice(maxIndices) # Choose randomly if there is more than one with the same value
        
        return a

    # Select one action, used when evaluating
    # st - is the current state    
    # aa - is the set of possible actions
    # for a given state they are always given in the same order
    # returns
    # a - the index to the action in aa
    def selectactiontoexecute(self,st,aa):
        # define this function
        a = 0
        # print("select one action to see if I learned")
        
        numActions = len(aa)

        if not self.visited[st]:
            return random.randint(0, numActions - 1)

        rewards = self.Q[st]
        maxReward = max(rewards)
        maxIndices = [actionIndex for actionIndex in range(numActions) if rewards[actionIndex] == maxReward]

        a = random.choice(maxIndices) # Choose randomly if there is more than one with the same value

        return a


    # this function is called after every action
    # ost - original state
    # nst - next state
    # a - the index to the action taken
    # r - reward obtained
    def learn(self,ost,nst,a,r):
        # define this function
        #print("learn something from this data")

        self.alpha = max(self.ALPHA_MIN, self.alpha * self.ALPHA_MULT)

        self.N[ost][a] += 1

        self.usedActions[ost].add(a)
        
        self.Q[ost][a] += self.alpha * (r + self.GAMMA * (max(self.Q[nst]) if self.visited[nst] else 0) - self.Q[ost][a])

        #Model Update
        self.model[ost][a].append({'reward': r, 'newState': nst})

        for _ in range(self.UPDATE_TIMES):
            randomState = random.choice(list(self.visitedSet))
            randomAction = random.choice(list(self.usedActions[randomState]))
            
            currentModel = self.model[randomState][randomAction]
            rewards = 0
            maxQs = 0
            for outcome in currentModel:
                rewards += outcome['reward']
                maxQs += max(self.Q[outcome['newState']]) if self.visited[outcome['newState']] else 0
            
            weightedSum = (rewards + self.GAMMA * maxQs) / self.N[randomState][randomAction]

            self.Q[randomState][randomAction] += self.alpha * (weightedSum - self.Q[randomState][randomAction])

        return
