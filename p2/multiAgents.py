from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        totalFoodDis=0
        nearestGhost=float('inf')
        bebrave=1
        nearestFood=float('inf')
        foodcnt=0
        for index in range(newFood.width*newFood.height):
            x,y=newFood._cellIndexToPosition(index)
            x=int(x)
            y=int(y)
            if newFood[x][y] == True:
                foodcnt+=1
                totalFoodDis+=util.manhattanDistance((x,y),newPos)
                nearestFood=min(nearestFood,manhattanDistance((x,y),newPos))
        # for foodpos in newFood:
        #     print(foodpos)
        #     totalFoodDis+=util.manhattanDistance(foodpos,newPos)
        #     nearestFood=min(nearestFood,manhattanDistance(foodpos,newPos))
        for index,ghost in enumerate(newGhostStates):
            ghostPos=ghost.getPosition()
            nearestGhost=min(nearestGhost,manhattanDistance(newPos,ghostPos))
            if manhattanDistance(newPos,ghostPos)<=2 and newScaredTimes[index]==0:
                bebrave=0
        if bebrave==1:
            if action=='Stop':
                return 0
            return 3/(totalFoodDis+0.1)+newFood[newPos[0]][newPos[1]]+4/(nearestFood+0.1)+successorGameState.getScore()
        else:
            if nearestGhost<=1:
                return -float('inf')
            return 1/totalFoodDis-3/nearestGhost


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # legalMoves = gameState.getLegalActions()
        #
        # # Choose one of the best actions
        # scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #
        #return legalMoves[chosenIndex]

        legalMoves = gameState.getLegalActions(0)
        scores = [self.calValue(gameState.generateSuccessor(0,action),1,self.depth) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def calValue(self,gameState,agentIndex,depth):
        numAgent=gameState.getNumAgents()
        if gameState.isLose() or gameState.isWin() or depth==0:
            return self.evaluationFunction(gameState)
        nextAgent = 0 if agentIndex==(numAgent-1) else agentIndex+1
        legalMoves = gameState.getLegalActions(agentIndex)
        scores= [self.calValue(gameState.generateSuccessor(agentIndex,action),nextAgent,depth-1 if nextAgent==0 else depth) for action in legalMoves]
        if agentIndex==0:
            return max(scores)
        else:
            return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        #return v,action
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v=-float('inf')
        alpha=-float('inf')
        beta=float('inf')
        v,action=self.maxValue(gameState,alpha,beta,0,self.depth)
        return action

    def maxValue(self,gameState,alpha,beta,agentIndex,depth):
        if gameState.isLose() or gameState.isWin() or depth==0:
            return self.evaluationFunction(gameState),'Stop'
        v=-float('inf')
        legalMoves=gameState.getLegalActions(agentIndex)
        nextAgent = 0 if agentIndex==(gameState.getNumAgents()-1) else agentIndex+1
        Action='Stop'
        if nextAgent>0:#monster's move
            for action in legalMoves:
                #Action=action
                minvalue,_=self.minValue(gameState.generateSuccessor(agentIndex,action),alpha,beta,nextAgent,depth)
                v,Action=max((v,Action),(minvalue,action))
                if v>beta:
                    return v,Action
                alpha=max(alpha,v)
            return v,Action
        else:
            for action in legalMoves:
                #Action=action
                maxvalue,_=self.maxValue(gameState.generateSuccessor(agentIndex,action),alpha,beta,nextAgent,depth-1)
                v,Action=max((v,Action),(maxvalue,action))
                if v>beta:
                    return v,Action
                alpha=max(alpha,v)
            return v,Action

    def minValue(self,gameState,alpha,beta,agentIndex,depth):
        if gameState.isLose() or gameState.isWin() or depth==0:
            return self.evaluationFunction(gameState),'Stop'
        v=float('inf')
        legalMoves=gameState.getLegalActions(agentIndex)
        nextAgent = 0 if agentIndex==(gameState.getNumAgents()-1) else agentIndex+1
        Action='Stop'
        if nextAgent>0:
            for action in legalMoves:
                #Action=action
                minvalue,_=self.minValue(gameState.generateSuccessor(agentIndex,action),alpha,beta,nextAgent,depth)
                #v=min(v,minvalue)
                v,Action=min((v,Action),(minvalue,action))
                if v<alpha:
                    return v,Action
                beta=min(beta,v)
            return v,Action
        else:
            for action in legalMoves:
                #Action=action
                maxvalue,_=self.maxValue(gameState.generateSuccessor(agentIndex,action),alpha,beta,nextAgent,depth-1)
                #v=min(v,maxvalue)
                v,Action=min((v,Action),(maxvalue,action))
                if v<alpha:
                    return v,Action
                beta=min(beta,v)
            return v,Action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalMoves=gameState.getLegalActions(0)
        scores=[self.calValue(gameState.generateSuccessor(0, action), 1, self.depth) for action in legalMoves]
        return legalMoves[scores.index(max(scores))]

    def calValue(self,gameState,agentIndex,depth):
        if gameState.isLose() or gameState.isWin() or depth==0:
            return self.evaluationFunction(gameState)
           # return betterEvaluationFunction(gameState)
        legalMoves=gameState.getLegalActions(agentIndex)
        nextAgent = 0 if agentIndex==(gameState.getNumAgents()-1) else agentIndex+1
        scores= [self.calValue(gameState.generateSuccessor(agentIndex,action),nextAgent,depth-1 if nextAgent==0 else depth) for action in legalMoves]
        if agentIndex==0:
            return max(scores)
        else:
            return sum(scores)/len(scores)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    "*** YOUR CODE HERE ***"
    totalFoodDis=0
    nearestGhost=float('inf')
    bebrave=1
    nearestFood=float('inf')
    foodcnt=0
    for index in range(Food.width*Food.height):
        x,y=Food._cellIndexToPosition(index)
        x=int(x)
        y=int(y)
        if Food[x][y] == True:
            foodcnt+=1
            totalFoodDis+=util.manhattanDistance((x,y),Pos)
            nearestFood=min(nearestFood,manhattanDistance((x,y),Pos))
    # for foodpos in newFood:
    #     print(foodpos)
    #     totalFoodDis+=util.manhattanDistance(foodpos,newPos)
    #     nearestFood=min(nearestFood,manhattanDistance(foodpos,newPos))
    totalGhostDis=0
    for index,ghost in enumerate(GhostStates):
        ghostPos=ghost.getPosition()
        totalGhostDis+=manhattanDistance(Pos,ghostPos)
        nearestGhost=min(nearestGhost,manhattanDistance(Pos,ghostPos))
        if manhattanDistance(Pos,ghostPos)<=2 and ScaredTimes[index]==0:
            bebrave=0
    if bebrave==1:
        return 10/(nearestFood+0.1)+currentGameState.getScore()-10/(nearestGhost+max(ScaredTimes))
    else:
        if nearestGhost<=1:
            return -float('inf')
        return 10/(nearestFood+0.1)+currentGameState.getScore()-10/(totalGhostDis+0.1)
# Abbreviation
better = betterEvaluationFunction
