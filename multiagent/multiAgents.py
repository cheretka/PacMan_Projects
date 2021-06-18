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
from util import manhattanDistance
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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        curFood = currentGameState.getFood()
        food_list = curFood.asList()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        new_food_list = newFood.asList()
        ghosts_positions = successorGameState.getGhostPositions()

        min_distance_to_ghost = float("inf")
        for ghost in ghosts_positions:
            min_distance_to_ghost = min(manhattanDistance(ghost, newPos), min_distance_to_ghost)

        min_distance_to_foot = float("inf")
        for food in new_food_list:
            min_distance_to_foot = min(manhattanDistance(food, newPos), min_distance_to_foot)

        count = len(new_food_list)

        if len(new_food_list) < len(food_list):
            count = 10000
        if count == 0:
            count = -1000

        if min_distance_to_ghost < 2:
            min_distance_to_ghost = -100000
        else:
            min_distance_to_ghost = 0

        if newScaredTimes[0] > 0:
            min_distance_to_ghost = 0

        return min_distance_to_ghost + 1.0 / min_distance_to_foot + count - successorGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        actions = gameState.getLegalActions(0)
        best_score = float("-inf")
        return_action = 0

        for action in actions:
            nextState = gameState.generateSuccessor(0, action)

            score = self.min_layer(nextState, 0, 1)

            if score > best_score:
                return_action = action
                best_score = score

        return return_action

    def max_layer(self, gameState, depth, agentIndex):

        depth += 1

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        return_value = float("-inf")
        actions = gameState.getLegalActions(0)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            return_value = max(return_value, self.min_layer(successor, depth, agentIndex + 1))

        return return_value

    def min_layer(self, gameState, depth, agentIndex):

        return_value = float("inf")
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == (gameState.getNumAgents() - 1):
                return_value = min(return_value, self.max_layer(successor, depth, 0))
            else:
                return_value = min(return_value, self.min_layer(successor, depth, agentIndex + 1))

        return return_value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        actions = gameState.getLegalActions(0)
        best_score = float("-inf")
        return_action = 0

        alpha = float("-inf")
        beta = float("inf")

        for action in actions:
            next_state = gameState.generateSuccessor(0, action)

            score = self.min_layer(next_state, 0, 1, alpha, beta)

            if score > best_score:
                return_action = action
                best_score = score

            if score > beta:
                return return_action

            alpha = max(alpha, score)

        return return_action

    def max_layer(self, gameState, depth, agentIndex, alpha, beta):

        depth += 1

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        return_value = float("-inf")
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:

            successor = gameState.generateSuccessor(agentIndex, action)
            return_value = max(return_value, self.min_layer(successor, depth, agentIndex + 1, alpha, beta))

            if return_value > beta:
                return return_value

            alpha = max(alpha, return_value)

        return return_value

    def min_layer(self, gameState, depth, agentIndex, alpha, beta):

        return_value = float("inf")
        if gameState.isWin() or gameState.isLose():  # Terminal Test
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)

            if agentIndex == (gameState.getNumAgents() - 1):
                return_value = min(return_value, self.max_layer(successor, depth, 0, alpha, beta))

                if return_value < alpha:
                    return return_value
                beta = min(beta, return_value)

            else:
                return_value = min(return_value, self.min_layer(successor, depth, agentIndex + 1, alpha, beta))

                if return_value < alpha:
                    return return_value
                beta = min(beta, return_value)

        return return_value


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

        actions = gameState.getLegalActions(0)
        best_score = float("-inf")
        return_action = ''

        for action in actions:
            next_state = gameState.generateSuccessor(0, action)

            score = self.expectLevel(next_state, 0, 1)

            if score > best_score:
                return_action = action
                best_score = score

        return return_action

    def maxLevel(self, gameState, depth):

        depth += 1

        if gameState.isWin() or gameState.isLose() or depth == self.depth:  # Terminal Test
            return self.evaluationFunction(gameState)

        return_value = float("-inf")
        actions = gameState.getLegalActions(0)

        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            return_value = max(return_value, self.expectLevel(successor, depth, 1))

        return return_value

    def expectLevel(self, gameState, depth, agentIndex):

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)
        expected_value = 0

        if len(actions) == 0:
            return 0

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)

            if agentIndex == (gameState.getNumAgents() - 1):
                expected_value += self.maxLevel(successor, depth)
            else:
                expected_value += self.expectLevel(successor, depth, agentIndex + 1)

        return float(expected_value) / float(len(actions))


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    ghost_scared_times_list = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    food_list = newFood.asList()

    distance_to_food_list = [0]
    for pos in food_list:
        distance_to_food_list.append(manhattanDistance(newPos, pos))

    ghost_pos = []
    for ghost in newGhostStates:
        ghost_pos.append(ghost.getPosition())

    distance_to_ghost_list = [0]
    for pos in ghost_pos:
        distance_to_ghost_list.append(manhattanDistance(newPos, pos))

    relative_food_distance = 0
    if sum(distance_to_food_list) > 0:
        relative_food_distance = 1.0 / sum(distance_to_food_list)

    score = currentGameState.getScore() + relative_food_distance + len(newFood.asList(False))

    if sum(ghost_scared_times_list) > 0:
        score += sum(ghost_scared_times_list) - len(currentGameState.getCapsules()) - sum(distance_to_ghost_list)
    else:
        score += sum(distance_to_ghost_list) + len(currentGameState.getCapsules())

    return score


# Abbreviation
better = betterEvaluationFunction
