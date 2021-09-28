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

        For a given state, this should return a list of triples,
         (action, stepCost, successor), where 'action' is the action
         required to get there, 'stepCost' is the incremental
         cost of expanding to that successor and 'successor' is a
         successor to the current state.
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

    actions=[]
    closed=[]
    fringe=util.Stack()
    fringe.push((problem.getStartState(),actions))
    while not fringe.isEmpty():
        curr_state,curr_action=fringe.pop()
        if problem.isGoalState(curr_state):
            return curr_action
        else:
            if not curr_state in closed:
                closed.append(curr_state)
                for nextstate in problem.getSuccessors(curr_state):
                    fringe.push((nextstate[2],curr_action+[nextstate[0]]))
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    actions=[]
    closed=[]
    fringe=util.Queue()
    fringe.push((problem.getStartState(),actions))
    while not fringe.isEmpty():
        curr_state,curr_action=fringe.pop()
        if problem.isGoalState(curr_state):
            return curr_action
        else:
            if not curr_state in closed:
                closed.append(curr_state)
                for nextstate in problem.getSuccessors(curr_state):
                    fringe.push((nextstate[2],curr_action+[nextstate[0]]))
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    actions=[]
    closed=[]
    totalcost=0

    fringe=util.PriorityQueue() #push(self, item, priority):
    fringe.push((problem.getStartState(),actions,totalcost),totalcost)
    while not fringe.isEmpty():
        curr_state,actions,totalcost=fringe.pop()
        if problem.isGoalState(curr_state):
            return actions
        else:
            if curr_state not in closed:
                closed.append(curr_state)
                for nextstate in problem.getSuccessors(curr_state): #( action, cost, nextState)
                    fringe.push((nextstate[2],actions+[nextstate[0]],totalcost+nextstate[1]),totalcost+nextstate[1])
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #Heuristics take two arguments:
    #a state in the search problem (the main argument), and the problem itself (for
    #reference information).
    actions=[]
    closed=[]
    heu=0 #h
    totalcost=0 #g
    fringe=util.PriorityQueue() #push(self, item, priority):
    fringe.push((problem.getStartState(),actions,totalcost),heu+totalcost)
    while not fringe.isEmpty():
        curr_state,curr_action,totalcost=fringe.pop()
        if problem.isGoalState(curr_state):
            return curr_action
        else:
            if curr_state not in closed:
                closed.append(curr_state)
                for nextstate in problem.getSuccessors(curr_state):
                    fringe.push((nextstate[2],curr_action+[nextstate[0]],totalcost+nextstate[1]),totalcost+nextstate[1]+heuristic(nextstate[2],problem))
    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
