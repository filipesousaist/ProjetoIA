from ruagomesfreiregame2sol import *
import random

DIRECTIONS = {
    'UP': (0, -1),
    'RIGHT': (1, 0),
    'DOWN': (0, 1),
    'LEFT': (-1, 0)
}

DIR_LIST = ('UP', 'RIGHT', 'DOWN', 'LEFT')

class Environment:
    def __init__(self):
        self.HIT_RATE = 1

        self.WIDTH = 4
        self.HEIGHT = 3

        self.rewards = [[-0.04 for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
        
        self.rewards[1][1] = None

        self.rewards[0][3] = 1
        self.rewards[1][3] = -1

    def getState(self):
        return self.agentY * self.WIDTH + self.agentX
    
    def getActions(self):
        return DIRECTIONS
    
    def getReward(self):
        return self.rewards[self.agentY][self.agentX]

    def moveAgent(self, directionIndex):
        if random.random() > self.HIT_RATE:
            directionIndex += random.choice([-1, 1])
        
        direction = DIR_LIST[directionIndex % 4]

        moveDir = DIRECTIONS[direction]
        newX, newY = self.agentX + moveDir[0], self.agentY + moveDir[1]

        if 0 <= newX < self.WIDTH and 0 <= newY < self.HEIGHT and self.rewards[newY][newX] != None:
            self.agentX, self.agentY = newX, newY
        
        # debug
        #input()
        #self.display()

    def resetAgent(self):
        self.agentX = 0
        self.agentY = 2

    def display(self):
        def sep():
            print('-'.join(['+'] * (self.WIDTH + 1)))
        
        sep()
        for y in range(self.HEIGHT):
            line = '|'
            for x in range(self.WIDTH):
                if x == self.agentX and y == self.agentY:
                    line += 'A'
                elif self.rewards[y][x] == None:
                    line += '#'
                else:
                    line += ' '
                line += '|'
            print(line)
            sep()
