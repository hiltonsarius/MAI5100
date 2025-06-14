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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        #return successorGameState.getScore()

        from util import manhattanDistance

        # Calculate the distance to the nearest food
        foodList = newFood.asList()
        if foodList:
            minFoodDistance = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            minFoodDistance = 0
        # Calculate the distance to the nearest ghost
        ghostDistances = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]
        minGhostDistance = min(ghostDistances)

        # Evaluate the score based on food distance, ghost distance, and scared times
        score = successorGameState.getScore()
        score += max(0, 10 - minFoodDistance) # Prefer closer food
        score -= max(0, 10 - minGhostDistance) # Avoid closer ghosts
        score += sum(newScaredTimes) # Prefer states where ghosts are scared

        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        def minimax(agentIndex, depth, gameState):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            num_agents = gameState.getNumAgents()
            next_agent = (agentIndex + 1) % num_agents

            if agentIndex == 0: # Maximizing agent (Pacman)
                max_eval = float('-inf')
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    eval = minimax(next_agent, depth, successor)
                    max_eval = max(max_eval, eval)
                return max_eval
            else: # Minimizing agents (Ghosts)
                min_eval = float('inf')
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    if next_agent == 0: # Next agent is Pacman, decrease depth
                        eval = minimax(next_agent, depth - 1, successor)
                    else:
                        eval = minimax(next_agent, depth, successor)
                    min_eval = min(min_eval, eval)
                return min_eval

        best_action = None
        max_eval = float('-inf')
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            eval = minimax(1, self.depth, successor)
            if eval > max_eval:
                max_eval = eval
                best_action = action

        return best_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimaxab(agentIndex, depth, gameState, alpha, beta):
            # Terminal state or depth limit
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            num_agents = gameState.getNumAgents()
            next_agent = (agentIndex + 1) % num_agents

            if agentIndex == 0: # Maximizing agent (Pacman)
                max_eval = float('-inf')
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    eval = minimaxab(next_agent, depth, successor, alpha, beta)
                    max_eval = max(max_eval, eval)
                    if max_eval > beta:
                        return max_eval # Beta cutoff
                    alpha = max(alpha, max_eval)
                return max_eval
            else: # Minimizing agents (Ghosts)
                min_eval = float('inf')
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)

                    if next_agent == 0: # Next agent is Pacman, decrease depth
                        eval = minimaxab(next_agent, depth - 1, successor, alpha, beta)
                    else:
                        eval = minimaxab(next_agent, depth, successor, alpha, beta)
                    # eval = minimaxab(next_agent, depth - 1, successor, alpha, beta)
                    min_eval = min(min_eval, eval)
                    if min_eval < alpha:
                        return min_eval# Alpha cutoff
                    beta = min(beta, min_eval)
                return min_eval

        max_eval = float('-inf')
        best_action = Directions.STOP
        alpha = float('-inf')
        beta = float('inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            eval = minimaxab(1, self.depth, successor, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                best_action = action

            alpha = max(alpha, max_eval)

        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(agentIndex, depth, gameState):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            num_agents = gameState.getNumAgents()
            next_agent = (agentIndex + 1) % num_agents

            if agentIndex == 0:  # Maximizing agent (Pacman)
                max_eval = float('-inf')
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    eval = expectimax(next_agent, depth, successor)
                    max_eval = max(max_eval, eval)
                return max_eval
            else:  # Chance nodes (Ghosts)
                total_eval = 0
                num_actions = len(gameState.getLegalActions(agentIndex))
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    if next_agent == 0:  # Next agent is Pacman, decrease depth
                        eval = expectimax(next_agent, depth - 1, successor)
                    else:
                        eval = expectimax(next_agent, depth, successor)
                    total_eval += eval
                return total_eval / num_actions if num_actions > 0 else 0

        best_action = None
        max_eval = float('-inf')
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            eval = expectimax(1, self.depth, successor)
            if eval > max_eval:
                max_eval = eval
                best_action = action

        return best_action


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
