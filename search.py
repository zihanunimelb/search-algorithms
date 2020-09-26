# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    visited = [start]
    stack = util.Stack()
    stack.push((start,[]))
    # while stack is not empty
    while not stack.isEmpty():
        (currentloc,actions) = stack.pop()
        visited.append(currentloc)
        if problem.isGoalState(currentloc):
            return actions
        else:
            successors = problem.getSuccessors(currentloc)
            for (location,action,cost) in successors:
                if location not in visited:
                    stack.push((location,actions+[action]))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    visited = [start]
    quene = util.Queue()
    quene.push((start,[]))
    while not quene.isEmpty():
        (currentloc,actions) = quene.pop()
        visited.append(currentloc)
        if problem.isGoalState(currentloc):
            return actions
        else:
            successors = problem.getSuccessors(currentloc)
            for (location,action,cost) in successors:
                if location not in visited:
                    quene.push((location, actions + [action]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# In both pratical task and Assignment 1
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE FOR TASK 3 ***"
    open = util.PriorityQueue()
    start =problem.getStartState()
    bestf = dict() ## a function to store optimal f value of grids
    open.push((start,[],0),heuristic(start,problem))
    while not open.isEmpty():
        curr = open.pop()
        currstate = curr[0]
        curract = curr[1]
        currfvalue = curr[2]
        currloc = currstate[0]
        foods = currstate[1]
        if currloc not in bestf or currfvalue < bestf[currloc]:
            bestf[currloc] = currfvalue
            if problem.isGoalState(currstate):
                return curract
            foodcount = foods.count()
            successors = problem.getSuccessors(currstate)
            for state, action, cost in successors:
                if state[1].count != foodcount: ## successors should have same food positions.
                    bestf.clear()
                if heuristic(state,problem)<999999:
                    open.push((state,curract+[action],cost+currfvalue),cost+heuristic(state,problem))
    return curract
    util.raiseNotDefined()
# Extensions Assignment 1
def iterativeDeepeningSearch(problem):
    """Search the deepest node in an iterative manner."""
    "*** YOUR CODE HERE FOR TASK 1 ***"
    from itertools import count
    start = problem.getStartState()
    for i in count(0):
        visited = [start]
        idfstack = util.Stack()
        idfstack.push((start,[]))
        # while stack is not empty
        while (not idfstack.isEmpty()):
            (currentloc,actions) = idfstack.pop()
            length = len(actions)
            visited.append(currentloc)
            if problem.isGoalState(currentloc):
                return actions
            else:
                if length <= i:
                    successors = problem.getSuccessors(currentloc)
                    for (location,action,cost) in successors:
                        if location not in visited:
                            idfstack.push((location,actions+[action]))
    util.raiseNotDefined()

def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second arguement (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    loc = problem.getStartState()
    actions = []
    while not problem.isGoalState(loc):
        ehcquene = util.Queue()
        ehcquene.push((loc,actions))
        visited = []
        while not ehcquene.isEmpty():
            currloc,curract = ehcquene.pop()
            if currloc not in visited:
                visited.append(currloc)
                if heuristic(loc,problem) > heuristic(currloc,problem):
                    loc, actions = currloc, curract
                    break
                else:
                    successors = problem.getSuccessors(currloc)
                    for location,action,cost in successors:
                        if location not in visited:
                            ehcquene.push((location,curract+[action]))
    return actions
    util.raiseNotDefined()           
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
ehc = enforcedHillClimbing