import random
import numpy
from numpy import *

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
        self.exploration_rate = 0.8
        self.inverse_sensitivity = 1
        self.TEMPERATURE = 1

        self.visited = [False] * nS

        self.Q = [None for _ in range(nS)]
        self.Epsilon = [None for _ in range(nS)]
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

        self.exploration_rate = max(0.2, self.exploration_rate * 0.9992)

        if not self.visited[st]:
            self.visited[st] = True
            self.Q[st] = [0] * numActions
            self.Epsilon[st] = 1

        if random.random() < self.Epsilon[st]: # Explore
            probabilities = []
            summation = 0
            
            for actionIndex in range(numActions):
                summation += exp(1) ** (self.Q[st][actionIndex] / self.TEMPERATURE)
            
            for actionIndex in range(numActions):
                probabilities.append((exp(1) ** (self.Q[st][actionIndex] / self.TEMPERATURE)) / summation)
            
            a = int(numpy.random.choice([actionIndex for actionIndex in range(numActions)], 1, p = probabilities))

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

        self.alpha = max(0.15, self.alpha * 0.9992)
        
        self.Q[ost][a] += self.alpha * (r + self.GAMMA * (max(self.Q[nst]) if self.visited[nst] else 0) - self.Q[ost][a])

        self.Epsilon[ost] = self.GAMMA * (1 - (exp(1) ** (-abs(self.alpha * \
            (r + self.GAMMA * (max(self.Q[nst]) if self.visited[nst] else 0)\
            - self.Q[ost][a])) / self.inverse_sensitivity))) / (1 + (exp(1) ** (-abs(self.alpha * \
            (r + self.GAMMA * (max(self.Q[nst]) if self.visited[nst] else 0)\
            - self.Q[ost][a])) / self.inverse_sensitivity))) + (1 - self.GAMMA) * self.Epsilon[ost]

        return
