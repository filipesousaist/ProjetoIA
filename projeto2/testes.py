import pickle
import random
import matplotlib.pyplot as plt
from ruagomesfreiregame2solDYNAQ import *
import sys
from time import time

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def runagent1(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

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
        nst = T[st][0][a]
        r = R[st]
        J += r

        if learningphase:
            A.learn(st,nst,a,r)

        st = nst

        if not ii%15:
            st = I
    return J/n


def runagent2(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

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
            if random.uniform(0, 1) < 0.1:
                nst = st
            else:
                nst = T[st][0][a]

        except:
            print(st,a)
        r = R[st]
        J += r

        if learningphase:
            A.learn(st,nst,a,r)
        else:
            pass

        st = nst

        if not ii%15:
            st = I
    return J/n

def runagent3(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

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

                if (a%2) == 0:
                    R[st] += 2
                else:
                    R[st] -= 1

                J += r
                if learningphase:
                    A.learn(st,nst,a,r)

                st = nst

                if not ii%15:
                    st = I
        return J/n

def runagent4(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

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

            if (st<50):
                R[a] -= 1
            else:
                R[st] += 1
        # if
            J += r
        # print(st,nsst,a,r)
            if learningphase:
                A.learn(st,nst,a,r)

            st = nst

            if not ii%15:
                st = I
        return J/n

def runagent5(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

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

        if (st<50):
            R[st] = 0
        else:
            R[st] = 1
    # if
        J += r
# print(st,nsst,a,r)
        if learningphase:
            A.learn(st,nst,a,r)

        st = nst

        if not ii%15:
            st = I
    return J/n

def runagent6(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

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

        if (st>50):
            for iii in range(50,114):
                R[st] = - R[114-st]

        J += r
        if learningphase:
            A.learn(st,nst,a,r)

        st = nst

        if not ii%15:
            st = I
    return J/n

def runagent7(A, T, R, I = 1, learningphase=True, nlearn = 1000, ntest = 100):

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

        R[st] = - R[st]

        J += r
        if learningphase:
            A.learn(st,nst,a,r)
        st = nst

        if not ii%15:
            st = I
    return J/n


NREP = 5
runagent = runagent2
test_name = "DynaQ - Without decaying discounting_factor - " + runagent.__name__ + "  - " + str(NREP) + " reps"
print(test_name)

# due to the randomness in the learning process, we will run everythin NREP times
# the final grades is based on the average on all of them
val = [0] * 10

start_time = time()

exemplo = "Exemplo 1"
printProgressBar(0, NREP, exemplo)
for nrep in range(0,NREP):
        A = LearningAgent(114,15)
        # your solution will be tested with other environments
        with open("mapasgraph2.pickle", "rb") as fp:   #Unpickling
            AA = pickle.load(fp)

        T = AA[0]
        R = [-1]*114
        R[7] = 1
        R[1] = 0
        R[2] = 0
        R[3] = 0
        R[4] = 0

        runagent(A, T, R, I = 1, learningphase=True, nlearn = 500)

        Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
        val[0] += Jn

        printProgressBar(nrep + 1/20, NREP, exemplo)

        runagent(A, T, R, I = 1, learningphase=True, nlearn = 10000)

        Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
        val[1] += Jn

        printProgressBar(nrep + 1, NREP, exemplo)

exemplo = "Exemplo 2"
printProgressBar(0, NREP, exemplo)
for nrep in range(0,NREP):

        A = LearningAgent(114,15)

        T = AA[0]
        R = [-1]*114
        R[10] = 1

        runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000)

        Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
        val[2] += Jn

        printProgressBar(nrep + 1/10, NREP, exemplo)

        runagent(A, T, R, I = 1, learningphase=True, nlearn = 10000)

        Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
        val[3] += Jn

        printProgressBar(nrep + 1, NREP, exemplo)

exemplo = "Exemplo 3"
printProgressBar(0, NREP, exemplo)
for nrep in range(0,NREP):

        A = LearningAgent(114,15)

        T = AA[0]
        R = [0]*114
        R[40] = 10

        runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000)

        Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
        val[4] += Jn

        printProgressBar(nrep + 1/10, NREP, exemplo)

        runagent(A, T, R, I = 1, learningphase=True, nlearn = 10000)

        Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
        val[5] += Jn

        printProgressBar(nrep + 1, NREP, exemplo)


exemplo = "Exemplo 4"
printProgressBar(0, NREP, exemplo)
for nrep in range(0,NREP):

    A = LearningAgent(114,15)

    T = AA[0]

    runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000)

    Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
    val[6] += Jn

    printProgressBar(nrep + 1/10, NREP, exemplo)

    runagent(A, T, R, I = 1, learningphase=True, nlearn = 10000)

    Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
    val[7] += Jn

    printProgressBar(nrep + 1, NREP, exemplo)


exemplo = "Exemplo 5"
printProgressBar(0, NREP, exemplo)
for nrep in range(0,NREP):

    A = LearningAgent(114,15)

    T = AA[0]
    R = [i if i < 50 else -i for i in range(114)]

    runagent(A, T, R, I = 1, learningphase=True, nlearn = 1000)

    Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
    val[8] += Jn
    printProgressBar(nrep + 1/10, NREP, exemplo)
    runagent(A, T, R, I = 1, learningphase=True, nlearn = 10000)
    Jn = runagent(A, T, R, I = 1, learningphase=False, ntest = 10)
    val[9] += Jn
    printProgressBar(nrep + 1, NREP, exemplo)


val = list([round(ii/NREP, 2) for ii in val])
print(val)
min_res = [0.3, 0.3, -0.85, -0.6, 0.1, 0.6, 40, 43, 22.5, 24]
cor = [res >= min for res, min in zip(val, min_res)]
grading = [(i%2 + 1) * 40/3 / len(val) if corr else 0 for i, corr in enumerate(cor)]
score = round(sum([res/min for res, min in zip(val, min_res)]), 3)
grade = round(sum(grading), 2)
# these values are not the optimal, they include some slack
print(cor)
print("Grade:", grade)
print("Score:", score)
print("Elapsed Time: %.3fs" % (time() - start_time))
