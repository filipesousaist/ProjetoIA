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

        self.ALPHA = 0.75
        self.GAMMA = 0.5
        self.EXPLORATION_RATE = 0.9

        self.visited = [False] * nS

        self.Q = [None for _ in range(nS)]
        self.N = [None for _ in range(nS)]
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
            return random.randint(0, numActions - 1)

        if random.random() < self.EXPLORATION_RATE: # Explore
            #self.EXPLORATION_RATE = max(0.7, self.EXPLORATION_RATE * 0.98)

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

        self.N[ost][a] += 1
        
        self.Q[ost][a] += self.ALPHA * (r + self.GAMMA * (max(self.Q[nst]) if self.visited[nst] else 0) - self.Q[ost][a])

        return
