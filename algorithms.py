import random
from collections import deque
import queue

class Algorithm:
    def get_path(self, state):
        pass


class ExampleAlgorithm(Algorithm):
    def get_path(self, state):
        path = []
        while not state.is_goal_state():
            possible_actions = state.get_legal_actions()
            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
            path.append(action)
            state = state.generate_successor_state(action)
        return path

#
class Blue(Algorithm):
    def get_path(self, state):
        stack = deque()
        visited = set()
        path = [] #putanja od startnog do finalnog stanja
        stack.append((state, path)) #pakujes stanja sa njihovim putanjama na stek

        while stack:
            currState, currPath = stack.pop()
            if currState.is_goal_state():
                return currPath

            if currState.get_state(kind='S') in visited:
                continue
            visited.add(currState.get_state(kind='S'))

            possible_actions = currState.get_legal_actions()
            prioritized_actions = possible_actions[::-1]
            for action in prioritized_actions:
                # if action not in currPath:
                stack.append((currState.generate_successor_state(action), currPath + [action]))
        return []

class Red(Algorithm):
    def get_path(self, state):
        queue = deque()
        visited = set()
        path = []  # putanja od startnog do finalnog stanja
        queue.append((state, path))  # pakujes stanja sa njihovim putanjama na stek

        while queue:
            currState, currPath = queue.popleft()
            if currState.is_goal_state():
                return currPath

            if currState.get_state(kind='S') in visited:
                continue
            visited.add(currState.get_state(kind='S'))

            possible_actions = currState.get_legal_actions()
            prioritized_actions = possible_actions[::-1]
            for action in prioritized_actions:
                queue.append((currState.generate_successor_state(action), currPath + [action]))
        return []
    
class Black(Algorithm):
    def calculateFieldNum(self, action):
        if (action[0][0] != action[1][0]):
            return abs(action[0][0] - action[1][0])
        else:
            return abs(action[0][1] - action[1][1])

    def calcSecondPriority(selfself, action):
        # west
        if (action[0][0] == action[1][0]) and (action[0][1] > action[1][1]):
            return 3
        # south
        elif (action[0][0] < action[1][0]) and (action[0][1] == action[1][1]):
            return 2
        # east
        elif (action[0][0] == action[1][0]) and (action[0][1] < action[1][1]):
            return 1
        # north
        else:
            return 0

    def get_path(self, state):
        priorityQueue = queue.PriorityQueue()
        counter = 0
        priorityQueue.put((0, 0, counter, state, []))

        visited = set()

        while not priorityQueue.empty():
            currentPriority, _, _, currentState, currentPath = priorityQueue.get()

            if currentState.is_goal_state():
                return currentPath

            if currentState.get_state(kind='S') in visited:
                continue
            visited.add(currentState.get_state(kind='S'))

            possibleActions = currentState.get_legal_actions()[::-1]
            for action in possibleActions:
                newPriority = currentPriority + self.calculateFieldNum(action)
                priorityQueue.put((newPriority, self.calcSecondPriority(action), counter, currentState.generate_successor_state(action), currentPath + [action]))
                counter += 1

        return []


class White(Algorithm):
    def calculateFieldNum(self, action):
        if (action[0][0] != action[1][0]):
            return abs(action[0][0] - action[1][0])
        else:
            return abs(action[0][1] - action[1][1])

    def manhattan_distances(self, action):
        return abs(action[0][0] - action[1][0]) + abs(action[0][1] - action[1][1])

    def get_path(self, state):
        priorityQueue = queue.PriorityQueue()
        counter = 0
        priorityQueue.put((0, 0, counter, state, []))

        visited = set()
        while not priorityQueue.empty():
            currentPriority, currentPrice, _, currentState, currentPath = priorityQueue.get()

            if currentState.is_goal_state():
                return currentPath

            if currentState.get_state(kind='S') in visited:
                continue
            visited.add(currentState.get_state(kind='S'))

            possibleActions = currentState.get_legal_actions()[::-1]
            for action in possibleActions:
                newPriority = currentPrice + self.calculateFieldNum(action) + self.manhattan_distances(action)
                priorityQueue.put((newPriority, currentPrice + self.calculateFieldNum(action), counter, currentState.generate_successor_state(action), currentPath + [action]))
                counter += 1

        return []