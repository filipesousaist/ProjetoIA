from ruagomesfreiregame2sol import *
import random

DIRECTIONS = {
    'UP': (0, -1),
    'RIGHT': (1, 0),
    'DOWN': (0, 1),
    'LEFT': (-1, 0)
}

DIR_LIST = ['UP', 'RIGHT', 'DOWN', 'LEFT']

class Agent:
    def __init__(self):
        self.x = 0
        self.y = 2    

class Environment:
    def __init__(self):
        self.HIT_RATE = 0.8

        self.WIDTH = 4
        self.HEIGHT = 3

        self.rewards = [[-0.04 for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
        self.rewards[1][1] = None
        self.rewards[0][3] = 1
        self.rewards[1][3] = -1

    def calculateStateNumber(self, x, y):
        return y * self.WIDTH + x

    # Returns new state
    def moveAgent(self, agent, direction):
        if random.random() > self.HIT_RATE:
            index = DIR_LIST.index(direction)
            index += random.choice([-1, 1])
            direction = DIRECTIONS[index % 4]

        moveDir = DIRECTIONS[direction]
        newX, newY = agent.x + moveDir[0], agent.y + moveDir[1]

        if 0 <= newX < self.WIDTH and 0 <= newY < self.HEIGHT and self.rewards[newY][newX] != None:
            agent.x, agent.y = newX, newY

        return calculateStateNumber(agent.x, agent.y)