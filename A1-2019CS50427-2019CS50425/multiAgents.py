# multiAgents.py
# --------------
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


'''-------------------------------------------------------------------------------
Submitted by: 
Deepanshu Rohilla       2019CS50427
Mrunmayi Bhalerao       2019CS50425

'''


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
        if(successorGameState.isWin()):
            return 1000000000

        for ghost in newGhostStates:
            if(ghost.scaredTimer==0 and manhattanDistance(ghost.getPosition(), newPos)<2):
                return -1000000000

        score = 0

        capsule = (0,0)
        if(len(currentGameState.getCapsules())>0):
            if(len(currentGameState.getCapsules()) ==len(successorGameState.getCapsules())):
                capsule = successorGameState.getCapsules()[0]
                dist = manhattanDistance(newPos,capsule)
                score = score + 300000.0/dist
            else:
                score = score + 1000000

        if(len(currentGameState.getFood().asList())!=len(successorGameState.getFood().asList())):
            score = score + 10000
        else:
            foodList = newFood.asList()
            minDistance = 1000000000
            for food in foodList:
                dist = manhattanDistance(newPos,food)
                if(dist<minDistance):
                    minDistance = dist
            score = score + 100.0/minDistance
        print(score)
        return score

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
        legalMoves = gameState.getLegalActions(0)
        maxVal = -1000000000
        maxAction = legalMoves[0]
        for move in legalMoves:
            val = self.minimaxSearch(gameState.generateSuccessor(0,move), 1)
            if(val>maxVal):
                maxVal = val
                maxAction = move
        return maxAction
    def minimaxSearch(self, gameState, turn):
        numAgents = gameState.getNumAgents()
        agentIndex = turn % numAgents
        depth = turn // numAgents
        if(gameState.isWin() or gameState.isLose() or depth==self.depth):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex) 
        values = []
        for move in legalMoves:
            val = self.minimaxSearch(gameState.generateSuccessor(agentIndex,move), turn+1)
            values.append(val)
        if(agentIndex>0):
            return min(values)
        return max(values)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha, beta = -1000000000, 1000000000 # Initialising alpha to min possible value
        legalMoves = gameState.getLegalActions(0)
        values = []
        for move in legalMoves:   
            v = self.alphaBetaSearch(gameState.generateSuccessor(0,move), 1, alpha, beta)
            alpha = max(alpha, v)
            values.append(v)
        for i in range(len(values)):
            if (values[i]==alpha):
                return legalMoves[i]
        util.raiseNotDefined()
    def alphaBetaSearch(self, gameState, turn, alpha, beta):
        numAgents = gameState.getNumAgents()
        agentIndex = turn % numAgents
        depth = turn // numAgents
        if(gameState.isWin() or gameState.isLose() or depth==self.depth):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)
        if(agentIndex==0):
            v = -1000000000
        else:
            v = 1000000000
        for move in legalMoves:
            successor = gameState.generateSuccessor(agentIndex, move)
            if(agentIndex>0):
                v = min(v, self.alphaBetaSearch(successor, turn + 1,alpha, beta))
                if(v<alpha):
                    return v
                beta = min(beta, v)
            else:
                v = max(v,self.alphaBetaSearch(successor,turn+1, alpha, beta))
                if(v>beta):
                    return v
                alpha = max(alpha, v)
        return v

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
        legalMoves = gameState.getLegalActions(0)
        maxVal = -1000000000
        maxAction = legalMoves[0]
        for move in legalMoves:
            val = self.expectimaxSearch(gameState.generateSuccessor(0,move), 1)
            if(val>maxVal):
                maxVal = val
                maxAction = move
        return maxAction
        util.raiseNotDefined()
    def expectimaxSearch(self, gameState, turn):
        numAgents = gameState.getNumAgents()
        agentIndex = turn % numAgents
        depth = turn // numAgents
        if(gameState.isWin() or gameState.isLose() or depth==self.depth):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex) 
        values = []
        for move in legalMoves:
            val = self.expectimaxSearch(gameState.generateSuccessor(agentIndex,move), turn+1)
            values.append(val)

        if(agentIndex>0):
            return sum(values) + 1.0/len(values)
        return max(values)

def betterEvaluationFunction(currentGameState):

    def bfs(currentGameState):
        queue = util.Queue()
        pacmanX,pacmanY = currentGameState.getPacmanPosition()
        queue.push((pacmanX,pacmanY))
        barrierWalls = currentGameState.getWalls()
        x, y = barrierWalls.height+1, barrierWalls.width+1

        mindistToFood =1000000000
        dist = []
        for i in range(y):
            l = [1000000000 for j in range(x)]
            dist.append(l)
        dist[pacmanX][pacmanY] = 0

        delta = [(0,1), (1,0), (0,-1), (-1,0)]

        while not queue.isEmpty():
            currentX, currentY = queue.pop()
            if currentGameState.hasFood(currentX, currentY):
                mindistToFood = min(mindistToFood, dist[currentX][currentY])
            for (dx, dy) in delta:
                nextX, nextY = currentX+dx, currentY+dy
                if barrierWalls[nextX][nextY] == False:
                    if dist[nextX][nextY] == 1000000000:
                        dist[nextX][nextY] = dist[currentX][currentY]+1
                        queue.push((nextX, nextY))

        return mindistToFood, dist
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if(currentGameState.isWin()):
        return 1000000000
    if(currentGameState.isLose()):
        return -1000000000


    currentFood = currentGameState.getFood()
    currentPos = currentGameState.getPacmanPosition()
    currentGhostStates = currentGameState.getGhostStates()

    a, b = bfs(currentGameState)
    foodList = currentFood.asList()
    minDistance = 1000000000
    for food in foodList:
        dist = b[int(food[0])][int(food[1])]
        if(dist<minDistance):
            minDistance = dist

    
    capsule = (0,0)
    capsuleDist = 0
    if(len(currentGameState.getCapsules())>0):
        capsule = currentGameState.getCapsules()[0]
        dist = b[int(capsule[0])][int(capsule[1])]
        capsuleDist = 300000.0/dist

    coverSum = 0
    scareSum = 0
    for ghost in currentGhostStates:
        ghostX, ghostY = ghost.getPosition()
        coverSum = coverSum + b[int(ghostX)][int(ghostY)]<3
        scareSum = scareSum + ghost.scaredTimer!=0


    return currentGameState.getScore()*10  +  1.0/minDistance + 1.0*coverSum + (scareSum)*10000 
    -len(currentGameState.getCapsules())*10000 + capsuleDist 
    util.raiseNotDefined()





# Abbreviation
better = betterEvaluationFunction
