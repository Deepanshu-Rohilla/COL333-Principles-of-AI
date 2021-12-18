import sys
# import pygame
import random
import numpy as np
from collections import defaultdict
import time
import pickle
random.seed(0)
'''
	Solving taxi problem with MDP
'''

# states:
# (i1,j1,i2,j2,isInTaxi) => taxi at i1,j1 and passenger at i2,j2, isin taxi?

# actions:
# actions = [(0,1), (0,-1), (1,0), (-1,0)] # north, south, east and west

# T(s,a,s') =
# transitionArray((1,1,1,1), (0,1), (1,2,1,2)   => 0.85
# transitionArray((1,1,1,1), (0,1), (1,2,1,2)

# reward function:
# R(s,a,s')

depots = [(0, 0), (0, 4), (3, 0), (4, 4)]
# actions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # north, south, east and west
actions = [(0, 1), (0, -1), (-1, 0), (1, 0), "pickup", "putdown"]
onlyActions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
# transition probability of state, action, next state
TransitionArray = defaultdict(int)
values = defaultdict(int)  # value of states
old_values = defaultdict(int)  # value of states

policy = defaultdict(int)  # policy of states
states = []


class state:
    def __init__(self, i1, j1, i2, j2, i3, j3, isInTaxi):
        self.taxi = (i1, j1)
        self.passenger = (i2, j2)
        self.destination = (i3, j3)
        self.isInTaxi = isInTaxi
    # printing

    def __str__(self):
        return str(self.taxi) + " " + str(self.passenger) + " " + str(self.destination) + " " + str(self.isInTaxi)

    def __eq__(self, other):
        return self.taxi == other.taxi and self.passenger == other.passenger and self.destination == other.destination and self.isInTaxi == other.isInTaxi

    def __hash__(self):
        return hash(str(self))


def reward_fuction(state, action):
    # action taken strictly

    if action == "putdown" and state.taxi == state.destination == state.passenger and state.isInTaxi == True:
        # if action == "putdwon" and state.taxi == state2.taxi and state.passenger == state2.passenger == state.destination and state2.isInTaxi == False and state.isInTaxi == True:
        return 20
    if (action == "pickup" or action == "putdown") and state.taxi != state.passenger:
        return -10
    return -1


def valueIteration(epsilon):  # TODO
    # implement value iteration
    global values, old_values, TransitionArray, states, policy
    discount = 0.1
    print("length of states", len(states))
    iter = 0
    max_iter = 10
    old_values = values.copy()
    valuesLossArr = []
    # convergence criteria: max-norm distance between two consecutive value functions
    while True and iter < max_iter:
        delta = 0
        valueLoss = 0

        for state in states:  # 1250
            newValue = -100000000
            for action in actions:
                currValue = 0
                for state2 in states:
                    if TransitionArray[state, action, state2] != 0:
                        currValue += TransitionArray[state, action, state2] * (
                            reward_fuction(state, action) + discount * old_values[state2])
                if currValue > newValue:
                    newValue = currValue
                    policy[state] = action
            values[state] = newValue
            valueLoss += pow(values[state]-old_values[state], 2)
            delta = max(delta, abs(values[state]-old_values[state]))
        print("---------------")
        old_values = values.copy()
        iter += 1
        print("iter", iter)
        print("delta:", delta)
        print("valueLoss:", valueLoss)
        valuesLossArr.append(pow(valueLoss, 0.5))
        # time.sleep(2)
        if delta < epsilon:
            break
    # save valueloss array to csv
    with open('valueLoss.csv', 'w') as f:
        for item in valuesLossArr:
            f.write("%s\n" % item)
    print("value loss:", valuesLossArr)


def policyIteration(epsilon):  # TODO
    # implement policy iteration
    global values, old_values, TransitionArray, states, policy
    discount = 0.1
    iter = 0
    max_iter = 10
    old_policy = policy.copy()
    policyLossArr = []
    # convergence criteria: max-norm distance between two consecutive value functions
    while True and iter < max_iter:
        delta = 0
        policyLoss = 0
        # Policy Evaluation
        old_values = values.copy()
        old_policy = policy.copy()
        for state in states:  # 1250
            newValue = -100000000
            action = old_policy[state]
            currValue = 0
            for state2 in states:
                if TransitionArray[state, action, state2] != 0:
                    currValue += TransitionArray[state, action, state2] * (
                        reward_fuction(state, action) + discount * old_values[state2])
            values[state] = currValue

        # old_values = values.copy()
        # Policy Improvement
        # delta = 0
        isConverged = True
        for state in states:
            newValue = -100000000
            for action in actions:
                currValue = 0
                for state2 in states:
                    if TransitionArray[state, action, state2] != 0:
                        currValue += TransitionArray[state, action, state2] * (
                            reward_fuction(state, action) + discount * values[state2])
                if currValue > newValue:
                    newValue = currValue
                    if policy[state] != action:
                        policy[state] = action
                        isConverged = False
            policyLoss += pow(values[state]-old_values[state], 2)
            delta = max(delta, abs(values[state]-old_values[state]))
        print("---------------")

        iter += 1
        print("iter", iter)
        print("delta:", delta)
        print("policyLoss:", policyLoss)
        policyLossArr.append(pow(policyLoss, 0.5))

        if delta < epsilon or isConverged:
            return
    # save policy loss array to csv
    with open('policyLoss.csv', 'w') as f:
        for item in policyLossArr:
            f.write("%s\n" % item)
    print("policy loss:", policyLossArr)


def isSafe(oldx, oldy, newx, newy):

    # walls between [(0,0),(0,1)], [(0,1),(1,1)], [(2,0),(3,1)],[(2,1),(3,1)], [(1,4),(2,4)], [(1,3),(2,3)]
    if (oldx, oldy) == (0, 0) and (newx, newy) == (0, 1):
        return False
    if (oldx, oldy) == (0, 1) and (newx, newy) == (1, 1):
        return False
    if (oldx, oldy) == (2, 0) and (newx, newy) == (3, 1):
        return False
    if (oldx, oldy) == (2, 1) and (newx, newy) == (3, 1):
        return False
    if (oldx, oldy) == (1, 4) and (newx, newy) == (2, 4):
        return False
    if (oldx, oldy) == (1, 3) and (newx, newy) == (2, 3):
        return False
    if(newx >= 0 and newx <= 4 and newy >= 0 and newy <= 4):
        return True
    return False


def addToTransitionArray(state0, desiredAction):
    if desiredAction == "pickup":  # TODO HERE
        state1 = state(state0.taxi[0], state0.taxi[1], state0.passenger[0],
                       state0.passenger[1], state0.destination[0], state0.destination[1], True)
        TransitionArray[state0, desiredAction, state1] = 1
        return
    if desiredAction == "putdown":
        state1 = state(state0.taxi[0], state0.taxi[1], state0.passenger[0],
                       state0.passenger[1], state0.destination[0], state0.destination[1], False)
        TransitionArray[state0, desiredAction, state1] = 1
        return

    for action in actions:
        if action != "pickup" and action != "putdown":

            newX, newY = state0.taxi[0]+action[0], state0.taxi[1]+action[1]
            if(isSafe(state0.taxi[0], state0.taxi[1], newX, newY)):
                state1 = state(newX, newY, state0.passenger[0], state0.passenger[1],
                               state0.destination[0], state0.destination[1], state0.isInTaxi)
                if(action == desiredAction):
                    TransitionArray[state0, action, state1] = 0.85
                else:
                    TransitionArray[state0, action, state1] = 0.05
            else:
                TransitionArray[state0, action, state0] = 1


# transition function
def initTransitionFunction(passengerDestination):
    global states, values, TransitionArray, policy
    global policy
    x = 0
    for i1 in range(5):
        for j1 in range(5):
            for i2 in range(5):
                for j2 in range(5):
                    for b in {True, False}:
                        mystate = state(
                            i1, j1, i2, j2, passengerDestination[0], passengerDestination[1], b)
                        states += [mystate]
                        policy[mystate] = random.choice(actions)
                        if (i1, j1, i2, j2, passengerDestination[0], passengerDestination[1], b) == (0, 2, 4, 4, 0, 4, False):
                            print("found!")
                            print(policy[mystate])
                            print(mystate)
                        values[mystate] = 0
                        for action in actions:
                            addToTransitionArray(mystate, action)
    print(policy[state(0, 2, 4, 4, 0, 4, False)])


def takeAction(currState, policy):
    # given policy and start end position, simulate the taxi
    # return the end position
    isInTaxi = False
    global actions
    while True:
        if currState.passenger[0] == currState.destination[0] and currState.passenger[1] == currState.destination[1]:
            return "f"
        # render(currState.taxi, currState.passenger, currState.destination)
        print(currState.taxi, currState.passenger, currState.destination)
        action = policy[currState]
        print(action)
        if action == "pickup":
            if currState.taxi == currState.passenger:
                currState.isInTaxi = True
                continue
        elif action == "putdown":
            if currState.taxi == currState.passenger:
                currState.isInTaxi = False
                if currState.passenger == currState.destination:
                    return currState
                continue
        else:
            rand_choice = random.random()
            if(rand_choice < 0.85):
                action = action
            else:
                temp = policy[currState]

                onlyActions.remove(temp)
                action = random.choice(onlyActions)
                onlyActions.append(temp)
            newX, newY = currState.taxi[0] + \
                action[0], currState.taxi[1]+action[1]
            if(isSafe(currState.taxi[0], currState.taxi[1], newX, newY)):
                currState.taxi = (newX, newY)
                if currState.isInTaxi:
                    currState.passenger = currState.taxi
            else:
                continue

# simple renderer that renders x,y coordinates on grid display


# pygame.init()
# screen = pygame.display.set_mode((500, 500))
# pygame.display.set_caption("Taxi")
# background = pygame.Surface(screen.get_size())
# background = background.convert()
# background.fill((250, 250, 250))
# screen.blit(background, (0, 0))


def render(passengerLoc, passengerDestination, taxiLoc):
    # 5*5 grid game
    # passengerLoc = (x,y)
    # passengerDestination = (x,y)
    # taxiLoc = (x,y)
    # render the grid

    # draw grid
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(screen, (0, 0, 0),
                             [(i+1)*50, (j+1)*50, 50, 50])
    # draw passenger
    pygame.draw.rect(screen, (0, 0, 255),
                     [(passengerLoc[0]+1)*50, (passengerLoc[1]+1)*50, 50, 50])
    # draw destination
    pygame.draw.rect(screen, (255, 0, 0),
                     [(passengerDestination[0]+1)*50, (passengerDestination[1]+1)*50, 50, 50])
    # draw taxi
    pygame.draw.rect(screen, (0, 255, 0),
                     [(taxiLoc[0]+1)*50, (taxiLoc[1]+1)*50, 50, 50])
    pygame.display.flip()
    pygame.time.wait(5)


def eposide(question):

    # randomly generate starting depot for passenger, select different destination depot for passenger and starting location for taxi
    passengerStart = depots[random.randint(0, 3)]
    depots.remove(passengerStart)
    passengerDestination = depots[random.randint(0, 2)]
    taxiStart = (random.randint(0, 4), random.randint(0, 4))
    print(taxiStart, passengerStart, passengerDestination)
    depots.append(passengerStart)

    # initialize reward function
    print("initializing reward function")
    initTransitionFunction(passengerDestination)
    if question == "1":
        print("Starting value iteration")
        valueIteration(0.1)
    else:
        print("Starting policy iteration")
        policyIteration(0.1)
    iniState = state(taxiStart[0], taxiStart[1], passengerStart[0],
                     passengerStart[1], passengerDestination[0], passengerDestination[1], False)
    print("Starting simulation as per policy")

    # save the policy as pkl model
    with open('policy'+str(question)+'.pkl', 'wb') as f:
        pickle.dump(policy, f)
    return policy
    # taxi, passenger, destination
    # print(policy[iniState])

    # takeAction(iniState)
import csv
import matplotlib.pyplot as plt

def plotGraphs():
    # read csv file and plot graphs
    policyArray = []
    valueArray = []
    with open('policyLoss.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            policyArray.append(row)
    with open('valueLoss.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            valueArray.append(row)
    
    # plot
    x = np.arange(0, len(policyArray))
    plt.plot(x, policyArray, label='Policy')
    plt.xlabel('Iterations')
    plt.ylabel('Policy')
    plt.title('Policy Iteration')
    plt.legend()
    plt.savefig('policy1.png')

    x = np.arange(0, len(valueArray))
    plt.plot(x, valueArray, label='Value')
    plt.xlabel('Iterations')
    plt.ylabel('Value')
    plt.title('Value Iteration')
    plt.legend()
    plt.savefig('value1.png')

if __name__ == '__main__':
    question = sys.argv[1]
    eposide(question)
    # print(TransitionArray)
    # read the policy from pkl model
    with open('policy'+question+'.pkl', 'rb') as f:
        policy = pickle.load(f)
    # print(policy)
    # for p in policy:
    #     if p.taxi == (-1, 2)
    takeAction(state(0, 2, 4, 4, 0, 4, False), policy)
