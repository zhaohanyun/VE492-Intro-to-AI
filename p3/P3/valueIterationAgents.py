import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for index in range(self.iterations):
            nextValue=self.values.copy() #the new value after one round of iteration
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    nextValue[state]=self.values[state]
                else:
                    #availAction=self.mdp.getPossibleActions(state)
                    nextValue[state]= max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
            self.values=nextValue



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transitionPair = self.mdp.getTransitionStatesAndProbs(state, action) # (nextState,prob) pair
        return sum([next[1] * (self.mdp.getReward(state,action,next[0]) + self.discount*self.getValue(next[0])) for next in transitionPair])

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        else:
            actions = self.mdp.getPossibleActions(state)
            bestAction = max([(self.computeQValueFromValues(state, action),action) for action in actions])
            return bestAction[1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
         #the new value after one round of iteration
        cnt=0
        while cnt!=self.iterations:
            for state in self.mdp.getStates():
                nextValue = self.values.copy()
                if self.mdp.isTerminal(state):
                    nextValue[state]=self.values[state]
                else:
                    #availAction=self.mdp.getPossibleActions(state)
                    nextValue[state]= max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
                cnt+=1
                self.values = nextValue
                if cnt==self.iterations:
                    break



class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors=dict()
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                possibleAction=self.mdp.getPossibleActions(state)
                for action in possibleAction:
                    fuck=(self.mdp.getTransitionStatesAndProbs(state, action)[0])
                    nextstate=fuck[0]
                    if nextstate not in predecessors.keys():
                        predecessors[nextstate]=set()
                    predecessors[nextstate].add(state)

        priorityState=util.PriorityQueue() # the pq used to decide who update first

        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                diff=abs(self.values[state]-max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)]))
                priorityState.push(state,-diff)

        for index in range(self.iterations):
            if priorityState.isEmpty():
                return
            state=priorityState.pop()
            if self.mdp.isTerminal(state):
                continue
            self.values[state]=max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
            for predecessorState in predecessors[state]:
                diff = abs(self.values[predecessorState] - max([self.getQValue(predecessorState, action) for action in self.mdp.getPossibleActions(predecessorState)]))
                if diff > self.theta:
                    priorityState.update(predecessorState,-diff)



































