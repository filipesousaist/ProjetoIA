import pickle
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ruagomesfreiregame2sol import *

def runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

        J = 0
        if learningphase:
                n = nlearn
        else:
                n = ntest

        st = I
        for ii in range(1,n):
                aa = T[st][0]
                if learningphase:
                        a = A.selectactiontolearn(st,aa)
                else:
                        a = A.selectactiontoexecute(st,aa)
                try:
                        nst = T[st][0][a]
                except:
                        print("Error: ", st, aa, a)
                r = R[st]
                J += r
                # print(st,nsst,a,r)

                if learningphase:
                        A.learn(st,nst,a,r)
                else:
                        # print(st,nst,a,r)
                        pass

                st = nst

                if not ii%15:
                        st = I
        return J/n


# due to the randomness in the learning process, we will run everythin NREP times
# the final grades is based on the average on all of them

R1 = [-1]*114
R1[7] = 1
R1[1] = 0
R1[2] = 0
R1[3] = 0
R1[4] = 0

R2 = [0]*114
R2[10] = 10

R3 = [0]*114
R3[40] = 10

R4 = [-i if i < 50 else i for i in range(114)]

R5 = [i if i < 50 else -i for i in range(114)]

R6 = [random.uniform(-1,1) for i in range(114)]

rewards =      (R1,       R2,          R3,     R4,     R5,       R6)
expected_val = [0.3, 0.3, -0.85, -0.6, 40, 43, 23, 24, 15, 16.5, 0.4, 0.5]

NREP = 20

with open("mapasgraph2.pickle", "rb") as fp:   #Unpickling
    AA = pickle.load(fp)

fig, ax = plt.subplots()
ax.set(ylabel='Result') #, xscale='log')
ax.grid()

T = AA[0]
scores = []
try:

    val = []
    for R in rewards:
        res_1 = res_2 = 0
        for nrep in range(0,NREP):
            A = LearningAgent(114, 15)
            runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000)
            Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
            res_1 += Jn
            runagent(A, T, R, I = 1, learningphase=True, nlearn = 10000)
            Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
            res_2 += Jn
        val.append(round(res_1/NREP, 2))
        val.append(round(res_2/NREP, 2))

    # Normalized results
    max_res = res = round(sum([res/expected for res, expected in zip(val, expected_val)]), 3)

    m = 's'
    ax.plot(A.ALPHA, res, m)
    print("Current Value:", A.ALPHA, "Result:", res)
    scores.append(res)

    while True:

        if len(scores) % 5 == 0:
            print("Testing", len(scores))

        test_var = random.randrange(0, 101)/100 # 1 + random.randrange(1, 10) * 10**(-random.randrange(1, 4))

        val = []
        for R in rewards:
            res_1 = res_2 = 0
            for nrep in range(0,NREP):
                A = LearningAgent(114, 15)

                A.ALPHA = test_var

                runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000)
                Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
                res_1 += Jn
                runagent(A, T, R, I = 1, learningphase=True, nlearn = 10000)
                Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
                res_2 += Jn
            val.append(round(res_1/NREP, 2))
            val.append(round(res_2/NREP, 2))

        # Normalized results
        res = round(sum([res/expected for res, expected in zip(val, expected_val)]), 3)

        if res > max_res:
            max_res = res
            print("New Best Value Found:", test_var, "Result:", res)

        m = 'o'
        if res >= max_res:
            m = 'x'
        ax.plot(test_var, res, m)
        scores.append(res)

finally:
    print("Average Score:", sum(scores)/len(scores))
    plt.show()
