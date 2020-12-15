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
        return successorGameState.getScore()

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



        #initializing variables
        actions = gameState.getLegalActions(0) #valid actions for Pacman
        maxAction = actions[0]      #temporary assignment to the desired action
        actionUtil = float("-inf")   #initial utility of maxAction
        depth = 0                   #starting depth

        #loop through valid actions for Pacman's first move
        for a in actions:
            currentState = gameState.generateSuccessor(0,a) #The resulting state from action a
            value = self.minValue(currentState, 1, depth)  #calling minValue with index 1, because the agent is now a ghost
            if value > actionUtil:
                maxAction = a
                actionUtil = value 

        return maxAction


    def maxValue(self,gameState,depth):
        #Checking for terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif depth == self.depth: #When depth == self.depht, we are done
            return self.evaluationFunction(gameState)

        v = float("-inf")
        actions = gameState.getLegalActions(0)
        for a in actions:
            currentState = gameState.generateSuccessor(0, a) 
            v = max(v,self.minValue(currentState,1,depth))
        return v

        
    def minValue(self,gameState,agentIndex, depth):
        #Checking for terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)


        v = float("inf")
        actions = gameState.getLegalActions(agentIndex)
        for a in actions:
            currentState = gameState.generateSuccessor(agentIndex, a)
            if currentState.getNumAgents() > agentIndex + 1: #Equivalently: if there are ghosts that have not moved
                v = min(v,self.minValue(currentState,agentIndex+1,depth)) #We call minValue and increment agentIndex
            else:
                v = min(v,self.maxValue(currentState,depth + 1)) #This line runs when the ply is "done" and we increment the depth
                                                                #maxValue does not need the index, because we know that Pacman has index 0

        return v
  




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """


    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        #Initializing variables
        actions = gameState.getLegalActions(0)
        maxAction = actions[0]
        depth = 0
        alpha = float("-inf")
        beta = float("inf")


        #What follows is essentially a call to maxValue, but it is written explicitly in getAction so the maxAction is easier to extract
        #Since we have to explore every action from the first node, we do not need to check if  v > beta. 
        #Equivalently, we can not prune any of the first actions.
        v = float("-inf")
        actions = gameState.getLegalActions(0)
        for a in actions:
            currentState = gameState.generateSuccessor(0, a) 
            v = self.minValue(currentState, 1, depth, alpha, beta)

            if v > alpha:
                alpha=v
                maxAction = a
 
        return maxAction


    def maxValue(self, gameState, depth, alpha, beta): #The maxValue function is called recursively to simulate Pacman's move
        #Checking for terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif depth == self.depth :
            return self.evaluationFunction(gameState)

        v = float("-inf")
        actions = gameState.getLegalActions(0)
        if not actions:
            return self.evaluationFunction(gameState)
        for a in actions:
            currentState = gameState.generateSuccessor(0, a) 
            v = max(v,self.minValue(currentState,1,depth, alpha, beta))
            if v > beta: return v
            alpha  = max(alpha,v)
        return v


    def minValue(self,gameState,agentIndex, depth, alpha, beta):
        #Checking for terminal state
        #We do not need to check the depht in minValue, because the depth is never incremented here
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)


        v = float("inf")
        actions = gameState.getLegalActions(agentIndex)
        for a in actions:
            currentState = gameState.generateSuccessor(agentIndex, a)
            if currentState.getNumAgents() > agentIndex + 1:
                v = min(v,self.minValue(currentState,agentIndex+1,depth,alpha,beta))
                if v < alpha: return v
                beta = min(beta,v)
            else:
                v = min(v,self.maxValue(currentState,depth + 1,alpha, beta))
                if v < alpha : return v
                beta = min(beta,v)
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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
