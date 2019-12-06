import random

# Doubly Linked List Node
class DLLNode:
    def __init__(self, action, q):
        self.action = action
        self.q = q
        self.previous = None
        self.next = None

# Doubly Linked List
class DLL:
    def __init__(self):
        self.first = self.last = None
        self.length = 0
    
    def push(self, action, q):
        new = DLLNode(action, q)
        if self.last == None:
            self.first = self.last = new
        else:
            self.last.next = new
            new.previous = self.last
            self.last = new
        self.length += 1
    
    def pop(self):
        if self.length == 0:
            return None

        toRemove = self.last
        self.last = toRemove.previous
        
        if toRemove.previous: # Not first element
            toRemove.previous.next = None
        else:
            self.first = None

        self.length -= 1

        return (toRemove.action, toRemove.q)

    def reorder(self, node):
        if node.previous and node.q < node.previous.q:
            # Remove node from DLL
            node.previous.next = node.next
            if not node.next:
                self.last = node.previous
            else:
                node.next.previous = node.previous
            
            # Recalculate position
            current = node.previous.previous
            node.previous = node.next = None
            while current and node.q < current.q:
                current = current.previous
            
            if current: # Middle of list
                node.previous = current
                node.next = current.next
                current.next.previous = node
                current.next = node
            else: # First position of list
                self.first.previous = node
                node.next = self.first
                self.first = node
        
        elif node.next and node.q > node.next.q:
            # Remove node from DLL
            node.next.previous = node.previous
            if not node.previous:
                self.first = node.next
            else:
                node.previous.next = node.next
            

            # Recalculate position
            current = node.next.next
            node.next = node.previous = None  
            while current and node.q > current.q:
                current = current.next
            
            if current: # Middle of list
                node.next = current
                node.previous = current.previous
                current.previous.next = node
                current.previous = node
            else: # Last position of list
                self.last.next = node
                node.previous = self.last
                self.last = node


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
        self.THETA = 0.01
        self.EXPLORATION_RATE = 0.2
        self.MAX_UPDATES = 5

        self.visited = [False] * nS
        
        
        self.Q = [None for _ in range(nS)]
        self.N = [None for _ in range(nS)]
        self.model = [[] for _ in range(nS)]
        self.queue = []
        self.ancestors = [set() for _ in range(nS)]
        # define this function

        self.qNodes = [None for _ in range(nS)]
        self.qLists = [None for _ in range(nS)]
    
    
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
            #self.Q[st] = [0] * numActions
            self.N[st] = [0] * numActions

            self.qLists[st] = DLL()
            self.qNodes[st] = []   
            for action in range(numActions):
                self.model[st].append([])
                self.qLists[st].push(action, 0)
                self.qNodes[st].append(self.qLists[st].last)

            return random.randint(0, numActions - 1)

        if random.random() > self.EXPLORATION_RATE: # Exploit an action with max q
            current = self.qLists[st].last
            maxQ = current.q
            maxQActions = [current.action]
            while current.previous and current.previous.q == maxQ:
                current = current.previous 
                maxQActions.append(current.action)

            a = random.choice(maxQActions)

        else: # Explore
            a = random.randint(0, numActions - 1)
        
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
        
        current = self.qLists[st].last
        maxQ = current.q
        maxQActions = [current.action]
        while current.previous and current.previous.q == maxQ:
            current = current.previous 
            maxQActions.append(current.action)

        a = random.choice(maxQActions)

        return a


    # this function is called after every action
    # ost - original state
    # nst - next state
    # a - the index to the action taken
    # r - reward obtained
    def learn(self,ost,nst,a,r):
        # define this function
        #print("learn something from this data")

        self.ancestors[nst].add((ost, a)) # Note: "(ost, a)" is only added if it is not already in "ancestors"
        self.N[ost][a] += 1

        # Update model
        currentModel = self.model[ost][a]
        currentModel.append({'state': nst, 'reward': r})

        # Update Q-value
        oldQ = self.qNodes[ost][a].q
        totalReward = 0
        for outcome in currentModel: # Iterate over "memorized" (state, reward) outcomes and compute a weighted sum
            totalReward += outcome['reward'] + self.GAMMA * self.maxQ(outcome['state'])
        self.qNodes[ost][a].q = totalReward / self.N[ost][a]
        self.qLists[ost].reorder(self.qNodes[ost][a])

        # Determine priority
        priority = abs(self.qNodes[ost][a].q - oldQ)

        if priority >= self.THETA and self.maxQ(ost) in (oldQ, self.qNodes[ost][a].q):
            orderedInsert(self.queue, {'state': ost, 'priority': priority})
        
        updates = 1
        while len(self.queue) and updates < self.MAX_UPDATES:
            # Determine (state, action) with highest priority
            state = self.queue.pop()['state']
            for ancState, ancAction in self.ancestors[state]: # Iterate over (state, action) pairs that lead to current state
                # Update Q-value
                oldQ = self.qNodes[ancState][ancAction].q
                totalReward = 0
                for outcome in self.model[ancState][ancAction]:
                    totalReward += outcome['reward'] + self.GAMMA * self.maxQ(outcome['state'])
                self.qNodes[ancState][ancAction].q = totalReward / self.N[ancState][ancAction]
                self.qLists[ancState].reorder(self.qNodes[ancState][ancAction])

                # Determine priority
                priority = abs(self.qNodes[ancState][ancAction].q - oldQ)
                  
                if priority >= self.THETA:
                    updates += 1
                    if self.maxQ(ancState) in (oldQ, self.qNodes[ancState][ancAction].q):
                        orderedInsert(self.queue, {'state': ancState, 'priority': priority})
    
    def maxQ(self, st):
        return self.qLists[st].last.q if self.visited[st] else 0

def orderedInsert(queue, element):
    for i in range(len(queue)):
        if element['priority'] >= queue[i]['priority']:
            queue.insert(i, element)
            return
    queue.append(element)
    
