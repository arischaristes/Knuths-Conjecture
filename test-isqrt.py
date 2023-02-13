from collections import deque
from datetime import timedelta, datetime
from gmpy2 import fac,isqrt
from matplotlib import pyplot

class queueNode:
    def __init__(self, parent, value, operation):
        self.parent = parent
        self.value = value
        self.operation = operation

class stackNode:
    def __init__(self, parent, value, operation, level):
        self.parent = parent
        self.value = value
        self.operation = operation
        self.level = level

def bfs(target):

    currentNode = queueNode(None, 4, "start")

    queue = deque()
    list = []
    queue.appendleft(currentNode)
    list.append(currentNode)

    found = False
    timeOut = False
    timer = datetime.now() + timedelta(minutes = 1)
    start = datetime.now()
    while not timeOut and queue:

        currentNode = queue.pop()

        if currentNode.value == target:
            found = True
            break

        if timer < datetime.now():
            timeOut = True
        
        if(currentNode.value <= 10000 and currentNode.value > 2):
            currentFactorial = queueNode(currentNode, fac(currentNode.value), "factorial")
            queue.appendleft(currentFactorial)
            list.append(currentFactorial)
        
        if(currentNode.value >= 2):
            currentSqrt = queueNode(currentNode, isqrt(currentNode.value), "root")
            queue.appendleft(currentSqrt)
            list.append(currentSqrt)

    timeToSolve = (datetime.now() - start).total_seconds()

    results = []
    if found:
        while currentNode.parent != None:
            results.append(currentNode.operation)
            currentNode = currentNode.parent
        results.reverse()
        return results, timeToSolve
    else:
        return results, False

def dfs(target, maxDepth):

    currentNode = stackNode(None, 4, "start", 0)

    stack = deque()
    list = []
    stack.append(currentNode)
    list.append(currentNode)

    found = False
    while stack:
        currentNode = stack.pop()

        if currentNode.value == target:
            found = True
            break

        if currentNode.level + 1 > maxDepth:
            continue
        else:
            if(currentNode.value >= 2):
                currentSqrt = stackNode(currentNode, isqrt(currentNode.value), "root", currentNode.level + 1)
                stack.append(currentSqrt)
                list.append(currentSqrt)

            if(currentNode.value <= 10000 and currentNode.value > 2):
                currentFactorial = stackNode(currentNode, fac(currentNode.value), "factorial", currentNode.level + 1)
                stack.append(currentFactorial)
                list.append(currentFactorial)

    results = []
    if found:
        while currentNode.parent != None:
            results.append(currentNode.operation)
            currentNode = currentNode.parent
        results.reverse()
        
    return results

def ids(target):

    i = 0
    results = []
    
    timeOut = False
    timer = datetime.now() + timedelta(minutes = 1)
    start = datetime.now()
    while not timeOut:
        if results:
            break
        elif timer < datetime.now():
            timeOut = True
        else:
            results = dfs(target, i)
        i = i + 1

    timeToSolve = (datetime.now() - start).total_seconds()

    return results, timeToSolve

x1 = []
y1 = []
x2 = []
y2 = []
with open('fac10000num1-50isqrt.txt', 'w') as f:
    
    for i in range(1,51):
        if i == 4:
            continue
        bfsSolved, bfsTime = bfs(i)
        idsSolved, idsTime = ids(i)
        if bfsSolved and idsSolved:
            f.write("Time for " + str(i) + ":\n")
            f.write("BFS = " + str(bfsTime) + " seconds\n")
            f.write("IDS = " + str(idsTime) + " seconds\n")
            f.write("Solution:\n")
            f.write("BFS = ")
            f.writelines(bfsSolved)
            f.write("\n")
            f.write("IDS = ")
            f.writelines(idsSolved)
            f.write("\n")
            f.write("\n")
            x1.append(i)
            y1.append(bfsTime)
            x2.append(i)
            y2.append(idsTime)
        
        print(i)

    f.close()

pyplot.plot(x1, y1, label = "BFS")
pyplot.plot(x2, y2, label = "IDS")
pyplot.xlabel("target")
pyplot.ylabel("time(in seconds)")
pyplot.title("Breadth First Search - Iterative Deepening Search Time Comparison")
pyplot.legend()
pyplot.show()