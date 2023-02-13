from collections import deque
from datetime import timedelta, datetime
from gmpy2 import floor,fac,sqrt,is_integer
import sys

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

        if(not is_integer(currentNode.value) and currentNode.parent.operation != "floor"):
            currentFloor = queueNode(currentNode, floor(currentNode.value), "floor")
            queue.appendleft(currentFloor)
            list.append(currentFloor)
        
        if(currentNode.value <= 2000 and currentNode.value > 2 and is_integer(currentNode.value)):
            currentFactorial = queueNode(currentNode, fac(int(currentNode.value)), "factorial")
            queue.appendleft(currentFactorial)
            list.append(currentFactorial)
        
        if(currentNode.value >= 2):
            currentSqrt = queueNode(currentNode, sqrt(currentNode.value), "root")
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
            if(not is_integer(currentNode.value) and currentNode.parent.operation != "floor"):
                currentFloor = stackNode(currentNode, floor(currentNode.value), "floor", currentNode.level + 1)
                stack.append(currentFloor)
                list.append(currentFloor)

            if(currentNode.value >= 2):
                currentSqrt = stackNode(currentNode, sqrt(currentNode.value), "root", currentNode.level + 1)
                stack.append(currentSqrt)
                list.append(currentSqrt)

            if(currentNode.value <= 2000 and currentNode.value > 2 and is_integer(currentNode.value)):
                currentFactorial = stackNode(currentNode, fac(int(currentNode.value)), "factorial", currentNode.level + 1)
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

target = input("Enter target number ")
algorithm = input("Enter 0 for BFS or 1 for IDS ")

if target == "4":
    print("No operation needed for input = 4")
    sys.exit()

if algorithm == "0":
    solution, time = bfs(int(target))
    if solution:
        for node in solution:
            print(node)

        print("Time to find solution is", time, "seconds")
    else:
        print("No solution found in current time limit set")
else:
    solution, time = ids(int(target))
    if solution:
        for node in solution:
            print(node)
        print("Time to find solution is", time, "seconds")
    else:
        print("No solution found in current time limit set")