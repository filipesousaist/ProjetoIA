from ruagomesfreiregame2sol import *
from bookEnv2 import *
import sys

NUM_LEARNING_1 = 250
NUM_LEARNING_2 = 1000
NUM_TESTS_1 = 10
NUM_TESTS_2 = 15

REPEAT = 10

SHOW_AMOUNT = 30

def main():
    myEnv = Environment()

    results1 = [] # Lista com objetos {alpha: ***, gamma: ***, totalReward: ***}
    results2 = [] # Lista com objetos {alpha: ***, gamma: ***, totalReward: ***}

    for alpha in [i / 50 for i in range(51)]:
        print("Started alpha = " + str(alpha))
        for gamma in [i / 50 for i in range(51)]:

            reward1 = reward2 = 0
            for _ in range(REPEAT):
                myAgent = LearningAgent(myEnv.WIDTH * myEnv.HEIGHT, 4)
                myAgent.ALPHA = alpha
                myAgent.GAMMA = gamma
                reward1 += runAgent(myAgent, myEnv, NUM_LEARNING_1, NUM_TESTS_1)
                
                myAgent = LearningAgent(myEnv.WIDTH * myEnv.HEIGHT, 4)
                myAgent.ALPHA = alpha
                myAgent.GAMMA = gamma
                reward2 += runAgent(myAgent, myEnv, NUM_LEARNING_2, NUM_TESTS_2)
            
            results1.append({'alpha': alpha, 'gamma': gamma, 'avgReward': reward1 / REPEAT / NUM_TESTS_1}) 
            results2.append({'alpha': alpha, 'gamma': gamma, 'avgReward': reward2 / REPEAT / NUM_TESTS_2})

    print("Finished all tests")

    sortFunc = lambda obj: obj['avgReward']

    results1.sort(key = sortFunc, reverse = True)
    print('-----------')
    print('| TESTS 1 |')
    print('-----------')
    for i in range(SHOW_AMOUNT):
        print(results1[i])

    results2.sort(key = sortFunc, reverse = True)
    print('-----------')
    print('| TESTS 2 |')
    print('-----------')
    for i in range(SHOW_AMOUNT):
        print(results2[i])

def runAgent(myAgent, myEnv, numLearning, numTests):
    myEnv.resetAgent()
    currentState = myEnv.getState()
    for _ in range(numLearning):
        actionIndex = myAgent.selectactiontolearn(currentState, myEnv.getActions())

        reward = myEnv.getReward()
        myEnv.moveAgent(actionIndex)
        nextState = myEnv.getState()
        myAgent.learn(currentState, nextState, actionIndex, reward)
        currentState = nextState

    totalReward = 0
    myEnv.resetAgent()
    currentState = myEnv.getState()
    for _ in range(numTests):
        actionIndex = myAgent.selectactiontoexecute(currentState, myEnv.getActions())

        totalReward += myEnv.getReward()
        myEnv.moveAgent(actionIndex)
        nextState = myEnv.getState()
        currentState = nextState

    return totalReward

if __name__ == '__main__':
    main()