<<<<<<< HEAD:projeto2/ruagomesfreiregame2solDYNAQ2.py
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

        self.ALPHA = 0.7
        self.GAMMA = 0.8
        self.EXPLORATION_RATE = 0.8
        self.UPDATE_TIMES = 10

        self.visited = [False] * nS

        self.Q = [None for _ in range(nS)]
        self.N = [None for _ in range(nS)]
        self.model = [[] for _ in range(nS)]
        self.visitedSet = set()
        self.usedActions = [set() for _ in range(nS)]
        # define this function
    
    
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

        self.EXPLORATION_RATE = max(0.2, self.EXPLORATION_RATE * 0.9992)

        if not self.visited[st]:
            self.visited[st] = True
            self.visitedSet.add(st)
            self.Q[st] = [0] * numActions
            self.N[st] = [0] * numActions
            for _ in range(numActions):
                self.model[st].append(None)
            return random.randint(0, numActions - 1)

        if random.random() < self.EXPLORATION_RATE: # Explore
            numExecutions = self.N[st] # Number of times that each action was executed in this state
            minExecutions = min(numExecutions) # Minimum number of executions fora action of  that state
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

        self.ALPHA = max(0.15, self.ALPHA * 0.9992)

        self.N[ost][a] += 1

        self.usedActions[ost].add(a)
        
        self.Q[ost][a] += self.ALPHA * (r + self.GAMMA * (max(self.Q[nst]) if self.visited[nst] else 0) - self.Q[ost][a])

        #Model Update
        self.model[ost][a] = (r, nst)

        for _ in range(self.UPDATE_TIMES):
            randomState = random.choice(list(self.visitedSet))
            randomAction = random.choice(list(self.usedActions[randomState]))
            
            (reward, newState) = model[randomState][randomAction]

            self.Q[randomState][randomAction] += self.ALPHA * (reward + self.GAMMA * (max(self.Q[newState]) if self.visited[state] else 0) - self.Q[randomState][randomAction])

        return
=======
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

        self.alpha = 0.7
        self.GAMMA = 0.8
        self.THETA = 0.01
        #self.EXPLORATION_RATE = 0.8
        self.PREDICT_ANTECESSOR_RATE = 0.5

        self.visited = [False] * nS

        self.Q = [None for _ in range(nS)]
        self.N = [None for _ in range(nS)]
        self.model = [[] for _ in range(nS)]
        self.queue = []
        # define this function
    
    
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

        if not self.visited[st]:
            self.visited[st] = True
            self.Q[st] = [0] * numActions
            self.N[st] = [0] * numActions
            for _ in range(numActions):
                self.model[st].append({})

            return random.randint(0, numActions - 1)

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

        self.N[ost][a] += 1

        # Update model
        currentModel = self.model[ost][a]
        if nst not in currentModel:
            currentModel[nst] = {'reward': r, 'frequency': 1}
        else:
            currentModel[nst]['frequency'] += 1
        
        # Determine priority
        priority = abs(r + self.GAMMA * (max(self.Q[nst]) if self.visited[nst] else 0) - self.Q[ost][a])

        if priority > self.THETA:
            orderedInsert(self.queue, {'state': ost, 'action': a, 'priority': priority})
        
        while len(self.queue):
            # Determine (state, action) with highest priority
            element = self.queue.pop()
            state, action = element['state'], element['action']

            currentModel = self.model[state][action]

            weightedSum = 0
            for nextState in currentModel:
                r = currentModel[nextState]['reward']
                maxQ = max(self.Q[nextState]) if self.visited[nextState] else 0
                factor = currentModel[nextState]['frequency'] / self.N[state][action]
                weightedSum += factor * (r + self.GAMMA * maxQ)

            self.Q[state][action] += self.alpha * (weightedSum - self.Q[state][action])

            for ancestorState, ancestorAction, reward in self.getPredictedAncestors(state):
                priority = abs(reward + self.GAMMA * (max(self.Q[state]) if self.visited[state] else 0) - self.Q[ancestorState][ancestorAction])
                if priority > self.THETA:
                    orderedInsert(self.queue, {'state': ancestorState, 'action': ancestorAction, 'priority': priority})

        self.alpha = max(0.15, self.alpha * 0.9992)
        
        return

    def getPredictedAncestors(self, state):
        for oldState in range(self.nS):
            if self.visited[state]:
                for action in range(len(self.model[oldState])):
                    if state in self.model[oldState][action] and \
                       self.model[oldState][action][state]['frequency'] / self.N[oldState][action] >= self.PREDICT_ANTECESSOR_RATE:
                       yield (oldState, action, self.model[oldState][action][state]['reward'])
    

def orderedInsert(queue, element):
    for i in range(len(queue)):
        if element['priority'] >= queue[i]['priority']:
            queue.insert(i, element)
            return
    queue.append(element)
    
>>>>>>> e5065a83fcf98177f7312dcf9828ccd3003a225b:PROJETO2/ruagomesfreiregame2sol.py
